import asyncio
import json
import os
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from urllib.parse import quote
from collections import deque, defaultdict

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, PlainTextResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("RVG-Gateway")

app = FastAPI(title="RVG Gateway – codebox", docs_url=None, redoc_url=None)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": os.environ.get("SECRET_KEY", secrets.token_urlsafe(32)),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────── State (in-memory) ─────────
connections: dict = {}
stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}
error_logs: deque = deque(maxlen=50)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None

# لینک‌های ساخته‌شده توسط کاربران
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()

# ───────── Auth State ─────────
SESSION_COOKIE = "rvg_session"
SESSION_TTL = 60 * 60 * 24 * 7  # 7 روز

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {
    "password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "123456")),
}

SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()


async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token


async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True


async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)


async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token


# ───────── Startup / Shutdown ─────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True)
    logger.info(f"🚀 RVG Gateway started on port {CONFIG['port']}")


@app.on_event("shutdown")
async def shutdown():
    if http_client:
        await http_client.aclose()


# ───────── Helpers ─────────
def get_host() -> str:
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])


def generate_uuid(seed: str | None = None) -> str:
    if seed is None:
        return str(secrets.token_hex(16))[:8] + "-" + secrets.token_hex(2) + "-" + \
               secrets.token_hex(2) + "-" + secrets.token_hex(2) + "-" + secrets.token_hex(6)
    h = hashlib.sha256(f"{seed}{CONFIG['secret']}".encode()).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def generate_vless_link(uuid: str, host: str, remark: str = "RVG-Railway") -> str:
    path = f"/ws/{uuid}"
    params = {
        "encryption": "none",
        "security": "tls",
        "type": "ws",
        "host": host,
        "path": path,
        "sni": host,
        "fp": "chrome",
        "alpn": "http/1.1",
    }
    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    return f"vless://{uuid}@{host}:443?{query}#{quote(remark)}"


def generate_subscription_content(links: list, host: str) -> str:
    """Generate base64-encoded subscription content with all active links"""
    import base64
    lines = []
    for link_data in links:
        if link_data.get("active", True):
            lines.append(link_data["vless_link"])
    content = "\n".join(lines)
    return base64.b64encode(content.encode()).decode()


def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB":
        return int(value * 1024 * 1024 * 1024)
    if unit == "MB":
        return int(value * 1024 * 1024)
    if unit == "KB":
        return int(value * 1024)
    return int(value)


def is_link_expired(link: dict) -> bool:
    """Check if a link has passed its expiry date"""
    expires_at = link.get("expires_at")
    if not expires_at:
        return False
    try:
        exp = datetime.fromisoformat(expires_at)
        return datetime.now() > exp
    except Exception:
        return False


# ───────── Default link (auto-created on first request) ─────────
async def ensure_default_link():
    async with LINKS_LOCK:
        if not LINKS:
            uid = generate_uuid("default")
            LINKS[uid] = {
                "label": "لینک پیش‌فرض",
                "limit_bytes": 0,
                "used_bytes": 0,
                "created_at": datetime.now().isoformat(),
                "active": True,
                "expires_at": None,
                "tags": [],
                "note": "",
            }


# ───────── Basic endpoints ─────────
@app.get("/")
async def root():
    return {
        "service": "RVG Gateway – codebox",
        "version": "7.0",
        "status": "active",
        "channel": "https://t.me/CodeBoxo",
        "host": get_host(),
    }


@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}


# ───────── Subscription endpoint ─────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str):
    """Single-link subscription URL"""
    import base64
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not link.get("active") or is_link_expired(link):
        raise HTTPException(status_code=404, detail="link not found or inactive")
    host = get_host()
    vless = generate_vless_link(uuid, host, remark=f"RVG-{link['label']}")
    content = base64.b64encode(vless.encode()).decode()
    return Response(
        content=content,
        media_type="text/plain",
        headers={
            "Content-Disposition": f'attachment; filename="sub.txt"',
            "profile-title": link["label"],
            "support-url": "https://t.me/CodeBoxo",
        }
    )


@app.get("/sub-all")
async def subscription_all(_=Depends(require_auth)):
    """All active links as subscription (admin only)"""
    host = get_host()
    async with LINKS_LOCK:
        links_data = [
            {
                "vless_link": generate_vless_link(uid, host, remark=f"RVG-{d['label']}"),
                "active": d.get("active", True),
                "expired": is_link_expired(d),
            }
            for uid, d in LINKS.items()
        ]
    import base64
    lines = [l["vless_link"] for l in links_data if l["active"] and not l["expired"]]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")


# ───────── Auth Endpoints ─────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    password = str(body.get("password") or "")
    if hash_password(password) != AUTH["password_hash"]:
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")

    token = await create_session()
    resp = JSONResponse({"ok": True})
    resp.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_TTL,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return resp


@app.post("/api/logout")
async def api_logout(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    await destroy_session(token)
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp


@app.get("/api/me")
async def api_me(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    valid = await is_valid_session(token)
    return {"authenticated": valid}


@app.post("/api/change-password")
async def api_change_password(request: Request, _=Depends(require_auth)):
    body = await request.json()
    current = str(body.get("current_password") or "")
    new = str(body.get("new_password") or "")

    if hash_password(current) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")

    AUTH["password_hash"] = hash_password(new)

    current_token = request.cookies.get(SESSION_COOKIE)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        if current_token:
            SESSIONS[current_token] = time.time() + SESSION_TTL

    return {"ok": True}


# ───────── Stats ─────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    now = datetime.now()
    async with LINKS_LOCK:
        links_snapshot = dict(LINKS)

    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 * 1024), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": now.isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(LINKS),
        "active_links": sum(1 for l in links_snapshot.values() if l.get("active") and not is_link_expired(l)),
        "expired_links": sum(1 for l in links_snapshot.values() if is_link_expired(l)),
    }


# ───────── Link Management API ─────────
@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    label = (body.get("label") or "لینک جدید").strip()[:60]
    limit_value = float(body.get("limit_value") or 0)
    limit_unit = body.get("limit_unit") or "GB"
    expires_days = body.get("expires_days")  # None = no expiry
    note = (body.get("note") or "").strip()[:200]
    tags = body.get("tags") or []

    limit_bytes = 0 if limit_value <= 0 else parse_size_to_bytes(limit_value, limit_unit)

    # Calculate expiry date
    expires_at = None
    if expires_days and int(expires_days) > 0:
        expires_at = (datetime.now() + timedelta(days=int(expires_days))).isoformat()

    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": label,
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": note,
            "tags": tags[:5],
        }

    host = get_host()
    return {
        "uuid": uid,
        "label": label,
        "limit_bytes": limit_bytes,
        "used_bytes": 0,
        "active": True,
        "created_at": LINKS[uid]["created_at"],
        "expires_at": expires_at,
        "note": note,
        "tags": tags,
        "vless_link": generate_vless_link(uid, host, remark=f"RVG-{label}"),
        "sub_url": f"https://{host}/sub/{uid}",
    }


@app.get("/api/links")
async def list_links(_=Depends(require_auth)):
    host = get_host()
    result = []
    async with LINKS_LOCK:
        for uid, data in LINKS.items():
            result.append({
                "uuid": uid,
                "label": data["label"],
                "limit_bytes": data["limit_bytes"],
                "used_bytes": data["used_bytes"],
                "active": data["active"],
                "created_at": data["created_at"],
                "expires_at": data.get("expires_at"),
                "note": data.get("note", ""),
                "tags": data.get("tags", []),
                "expired": is_link_expired(data),
                "vless_link": generate_vless_link(uid, host, remark=f"RVG-{data['label']}"),
                "sub_url": f"https://{host}/sub/{uid}",
            })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}


@app.patch("/api/links/{uid}")
async def toggle_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        if "active" in body:
            LINKS[uid]["active"] = bool(body["active"])
        if "limit_value" in body:
            limit_value = float(body.get("limit_value") or 0)
            limit_unit = body.get("limit_unit") or "GB"
            LINKS[uid]["limit_bytes"] = 0 if limit_value <= 0 else parse_size_to_bytes(limit_value, limit_unit)
        if "reset_usage" in body and body["reset_usage"]:
            LINKS[uid]["used_bytes"] = 0
        if "label" in body:
            LINKS[uid]["label"] = str(body["label"])[:60]
        if "expires_at" in body:
            LINKS[uid]["expires_at"] = body["expires_at"]
        if "note" in body:
            LINKS[uid]["note"] = str(body["note"])[:200]
    return {"ok": True}


@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        del LINKS[uid]
    return {"ok": True, "deleted": uid}


# ───────── VLESS Protocol Relay ─────────
RELAY_BUF = 64 * 1024


async def parse_vless_header(first_chunk: bytes):
    if len(first_chunk) < 24:
        raise ValueError("chunk too small for VLESS header")

    pos = 0
    version = first_chunk[pos]; pos += 1
    req_uuid = first_chunk[pos:pos + 16]; pos += 16

    addon_len = first_chunk[pos]; pos += 1
    pos += addon_len

    command = first_chunk[pos]; pos += 1
    port = int.from_bytes(first_chunk[pos:pos + 2], "big"); pos += 2

    addr_type = first_chunk[pos]; pos += 1

    if addr_type == 1:
        addr_bytes = first_chunk[pos:pos + 4]; pos += 4
        address = ".".join(str(b) for b in addr_bytes)
    elif addr_type == 2:
        domain_len = first_chunk[pos]; pos += 1
        address = first_chunk[pos:pos + domain_len].decode("utf-8", errors="ignore")
        pos += domain_len
    elif addr_type == 3:
        addr_bytes = first_chunk[pos:pos + 16]; pos += 16
        address = ":".join(f"{addr_bytes[i]:02x}{addr_bytes[i+1]:02x}" for i in range(0, 16, 2))
    else:
        raise ValueError(f"unknown address type: {addr_type}")

    payload = first_chunk[pos:]
    return req_uuid, command, address, port, payload


def format_link_uuid(raw16: bytes) -> str:
    h = raw16.hex()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


async def check_quota(uid: str, extra_bytes: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return True  # unknown link → allow (backward compat)
        if not link["active"]:
            return False
        # FIX: Check expiry
        if is_link_expired(link):
            return False
        if link["limit_bytes"] == 0:
            return True
        return (link["used_bytes"] + extra_bytes) <= link["limit_bytes"]


async def add_usage(uid: str, n: int):
    async with LINKS_LOCK:
        if uid in LINKS:
            LINKS[uid]["used_bytes"] += n


async def ws_to_tcp(websocket: WebSocket, writer: asyncio.StreamWriter, conn_id: str, link_uid: str):
    try:
        while True:
            msg = await websocket.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes")
            if data is None and msg.get("text") is not None:
                data = msg["text"].encode()
            if not data:
                continue

            size = len(data)
            if not await check_quota(link_uid, size):
                await websocket.close(code=1008, reason="quota exceeded")
                break

            stats["total_bytes"] += size
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += size
            hourly_traffic[datetime.now().strftime("%H:00")] += size
            await add_usage(link_uid, size)

            writer.write(data)
            await writer.drain()
    except WebSocketDisconnect:
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass


async def tcp_to_ws(websocket: WebSocket, reader: asyncio.StreamReader, conn_id: str, link_uid: str):
    first = True
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break

            size = len(data)
            if not await check_quota(link_uid, size):
                await websocket.close(code=1008, reason="quota exceeded")
                break

            stats["total_bytes"] += size
            connections[conn_id]["bytes"] += size
            hourly_traffic[datetime.now().strftime("%H:00")] += size
            await add_usage(link_uid, size)

            if first:
                await websocket.send_bytes(b"\x00\x00" + data)
                first = False
            else:
                await websocket.send_bytes(data)
    except Exception:
        pass


@app.websocket("/ws/{uuid}")
async def websocket_tunnel(websocket: WebSocket, uuid: str):
    await ensure_default_link()
    await websocket.accept()
    conn_id = secrets.token_urlsafe(8)
    connections[conn_id] = {
        "uuid": uuid,
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    logger.info(f"✅ WS connected [{conn_id}] uuid={uuid}  active={len(connections)}")

    writer = None
    try:
        if not await check_quota(uuid, 0):
            await websocket.close(code=1008, reason="quota exceeded or link disabled")
            return

        first_msg = await asyncio.wait_for(websocket.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect":
            return

        first_chunk = first_msg.get("bytes")
        if first_chunk is None and first_msg.get("text") is not None:
            first_chunk = first_msg["text"].encode()
        if not first_chunk:
            return

        req_uuid_raw, command, address, port, initial_payload = await parse_vless_header(first_chunk)

        size = len(first_chunk)
        stats["total_bytes"] += size
        stats["total_requests"] += 1
        connections[conn_id]["bytes"] += size
        hourly_traffic[datetime.now().strftime("%H:00")] += size
        await add_usage(uuid, size)

        logger.info(f"➡️  [{conn_id}] CONNECT {address}:{port} (cmd={command}) link={uuid[:8]}")

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port), timeout=10.0
        )

        if initial_payload:
            writer.write(initial_payload)
            await writer.drain()

        task_up = asyncio.create_task(ws_to_tcp(websocket, writer, conn_id, uuid))
        task_down = asyncio.create_task(tcp_to_ws(websocket, reader, conn_id, uuid))

        done, pending = await asyncio.wait(
            {task_up, task_down}, return_when=asyncio.FIRST_COMPLETED
        )
        for t in pending:
            t.cancel()

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.error(f"WS error [{conn_id}]: {exc}")
    finally:
        if writer:
            try:
                writer.close()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info(f"🔌 WS closed [{conn_id}]  active={len(connections)}")


# ───────── HTTP Proxy ─────────
_HOP_HEADERS = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade",
    "content-encoding", "content-length",
}


@app.api_route("/proxy/{target_url:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    try:
        body = await request.body()
        headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in _HOP_HEADERS and k.lower() != "host"
        }

        resp = await http_client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
        )

        size = len(resp.content)
        stats["total_bytes"] += size
        stats["total_requests"] += 1
        hourly_traffic[datetime.now().strftime("%H:00")] += size

        resp_headers = {
            k: v for k, v in resp.headers.items()
            if k.lower() not in _HOP_HEADERS
        }
        return Response(content=resp.content, status_code=resp.status_code, headers=resp_headers)

    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")


# ───────── Login Page ─────────
LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · RVG Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg-deep:#030d1a;
  --bg-mid:#061527;
  --accent:#3B82F6;
  --accent-glow:rgba(59,130,246,0.4);
  --accent-dim:rgba(59,130,246,0.15);
  --text-bright:#E8F4FF;
  --text-mid:#7BAED4;
  --text-dim:#3D6B8E;
  --border:rgba(59,130,246,0.2);
  --border-focus:rgba(59,130,246,0.6);
  --card-bg:rgba(6,21,39,0.85);
  --input-bg:rgba(3,13,26,0.7);
  --red:#EF4444;
  --red-dim:rgba(239,68,68,0.1);
}
html,body{height:100%;overflow:hidden}
body{
  font-family:'Vazirmatn',sans-serif;
  background:var(--bg-deep);
  min-height:100vh;
  display:flex;align-items:center;justify-content:center;
  padding:20px;
  position:relative;
}

/* Animated bg */
.bg-canvas{
  position:fixed;inset:0;z-index:0;
  background:radial-gradient(ellipse 80% 60% at 50% -10%, rgba(59,130,246,0.12) 0%, transparent 70%),
             radial-gradient(ellipse 50% 40% at 80% 80%, rgba(16,185,129,0.05) 0%, transparent 60%),
             var(--bg-deep);
}
.grid-lines{
  position:fixed;inset:0;z-index:0;
  background-image:
    linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size:40px 40px;
}
.orb{
  position:fixed;border-radius:50%;filter:blur(80px);z-index:0;
  animation:float 8s ease-in-out infinite;
}
.orb-1{width:400px;height:400px;background:rgba(59,130,246,0.06);top:-100px;right:-100px;animation-delay:0s}
.orb-2{width:300px;height:300px;background:rgba(16,185,129,0.04);bottom:-50px;left:-50px;animation-delay:3s}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}

/* Card */
.login-wrap{position:relative;z-index:10;width:100%;max-width:400px}
.login-card{
  background:var(--card-bg);
  border:1px solid var(--border);
  border-radius:20px;
  padding:38px 34px 34px;
  backdrop-filter:blur(20px);
  box-shadow:
    0 0 0 1px rgba(59,130,246,0.05),
    0 20px 60px rgba(0,0,0,0.5),
    0 0 80px rgba(59,130,246,0.06);
}

/* Logo */
.brand{display:flex;align-items:center;gap:14px;margin-bottom:30px}
.brand-icon{
  width:50px;height:50px;border-radius:14px;overflow:hidden;
  border:1px solid var(--border);
  box-shadow:0 0 20px var(--accent-glow);
  flex-shrink:0;
}
.brand-icon img{width:100%;height:100%;object-fit:cover}
.brand-name{font-size:17px;font-weight:700;color:var(--text-bright);letter-spacing:.01em}
.brand-sub{font-size:11px;color:var(--text-dim);margin-top:3px;font-weight:400}

/* Title */
.login-heading{
  font-size:22px;font-weight:700;color:var(--text-bright);
  margin-bottom:6px;letter-spacing:-.02em;
}
.login-sub{font-size:12.5px;color:var(--text-mid);margin-bottom:26px;line-height:1.6}

/* Form */
.field{margin-bottom:18px}
.field-label{
  font-size:11.5px;font-weight:600;color:var(--text-mid);
  margin-bottom:8px;display:block;letter-spacing:.02em;text-transform:uppercase;
}
.field-input-wrap{position:relative}
.field-input{
  width:100%;padding:13px 44px 13px 16px;
  border-radius:12px;
  border:1px solid var(--border);
  background:var(--input-bg);
  color:var(--text-bright);
  font-family:inherit;font-size:14px;
  outline:none;
  transition:all .2s;
  letter-spacing:.05em;
}
.field-input::placeholder{color:var(--text-dim);letter-spacing:0}
.field-input:focus{border-color:var(--border-focus);background:rgba(3,13,26,0.9);box-shadow:0 0 0 3px rgba(59,130,246,0.1)}
.field-icon{
  position:absolute;left:14px;top:50%;transform:translateY(-50%);
  color:var(--text-dim);font-size:18px;pointer-events:none;transition:.2s;
}
.field-input:focus + .field-icon{color:var(--accent)}

/* Default password hint */
.default-hint{
  display:flex;align-items:center;gap:10px;
  background:rgba(59,130,246,0.06);
  border:1px solid rgba(59,130,246,0.15);
  border-radius:10px;
  padding:10px 14px;
  margin-bottom:20px;
}
.hint-label{font-size:11px;color:var(--text-dim);flex:1}
.hint-val{
  font-family:ui-monospace,monospace;
  font-size:13px;font-weight:700;
  color:var(--accent);
  background:rgba(59,130,246,0.1);
  border:1px solid rgba(59,130,246,0.2);
  padding:3px 10px;border-radius:6px;
  cursor:pointer;transition:.15s;letter-spacing:.1em;
}
.hint-val:hover{background:rgba(59,130,246,0.2);border-color:var(--accent)}

/* Button */
.btn-login{
  width:100%;padding:14px;
  border-radius:12px;border:none;cursor:pointer;
  background:linear-gradient(135deg,#2563EB 0%,#1D4ED8 100%);
  color:#fff;font-family:inherit;font-size:14px;font-weight:600;
  display:flex;align-items:center;justify-content:center;gap:8px;
  transition:all .2s;
  box-shadow:0 4px 20px rgba(37,99,235,0.4),0 0 0 1px rgba(255,255,255,0.05) inset;
  position:relative;overflow:hidden;
}
.btn-login::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.1) 0%,transparent 60%);
  opacity:0;transition:.2s;
}
.btn-login:hover::before{opacity:1}
.btn-login:hover{box-shadow:0 6px 28px rgba(37,99,235,0.5)}
.btn-login:disabled{opacity:.5;cursor:not-allowed}
.btn-login i{font-size:16px}

/* Error */
.error-box{
  display:none;
  background:var(--red-dim);
  border:1px solid rgba(239,68,68,0.2);
  border-radius:10px;
  padding:11px 14px;
  margin-bottom:16px;
  font-size:12.5px;color:var(--red);
  align-items:center;gap:8px;
}
.error-box.show{display:flex}

/* Footer */
.login-footer{
  margin-top:24px;
  padding-top:20px;
  border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  gap:8px;font-size:11.5px;color:var(--text-dim);
}
.login-footer a{
  color:var(--accent);text-decoration:none;font-weight:600;
  display:flex;align-items:center;gap:4px;transition:.15s;
}
.login-footer a:hover{color:var(--text-bright)}
</style>
</head>
<body>
  <div class="bg-canvas"></div>
  <div class="grid-lines"></div>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>

  <div class="login-wrap">
    <div class="login-card">
      <div class="brand">
        <div class="brand-icon">
          <img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="codebox">
        </div>
        <div>
          <div class="brand-name">codebox</div>
          <div class="brand-sub">RVG Gateway · v7.0</div>
        </div>
      </div>

      <div class="login-heading">ورود به پنل</div>
      <div class="login-sub">رمز عبور خود را برای دسترسی به داشبورد وارد کنید</div>

      <div class="error-box" id="err-box"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>

      <div class="default-hint">
        <span class="hint-label">رمز پیش‌فرض</span>
        <span class="hint-val" onclick="fillDefault()" title="کلیک برای پر کردن خودکار">123456</span>
      </div>

      <form id="login-form">
        <div class="field">
          <label class="field-label">رمز عبور</label>
          <div class="field-input-wrap">
            <input class="field-input" type="password" id="password" placeholder="رمز عبور خود را وارد کنید" autofocus required>
            <i class="ti ti-lock field-icon"></i>
          </div>
        </div>
        <button class="btn-login" type="submit" id="login-btn">
          <i class="ti ti-login-2"></i> ورود به داشبورد
        </button>
      </form>

      <div class="login-footer">
        کانال رسمی
        <a href="https://t.me/CodeBoxo" target="_blank" rel="noopener">
          <i class="ti ti-brand-telegram"></i> @CodeBoxo
        </a>
      </div>
    </div>
  </div>

<script>
function fillDefault(){
  document.getElementById('password').value='123456';
  document.getElementById('password').focus();
}

const form=document.getElementById('login-form');
const errBox=document.getElementById('err-box');
const errText=document.getElementById('err-text');
const btn=document.getElementById('login-btn');

form.addEventListener('submit', async(e)=>{
  e.preventDefault();
  errBox.classList.remove('show');
  btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  const password=document.getElementById('password').value;
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا در ورود');}
    location.href='/dashboard';
  }catch(err){
    errText.textContent=err.message;
    errBox.classList.add('show');
    btn.disabled=false;
    btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
<style>@keyframes spin{to{transform:rotate(360deg)}}</style>
</body>
</html>"""


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if await is_valid_session(token):
        return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)


# ───────── Dashboard (SPA) ─────────
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RVG Gateway · codebox</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#060f1d;
  --bg2:#0a1628;
  --bg3:#0e1e35;
  --card:#0d1b2e;
  --card-border:rgba(59,130,246,0.12);
  --card-border-hover:rgba(59,130,246,0.25);
  --accent:#3B82F6;
  --accent-2:#60A5FA;
  --accent-glow:rgba(59,130,246,0.3);
  --accent-dim:rgba(59,130,246,0.1);
  --green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-text:#34D399;
  --red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-text:#F87171;
  --amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-text:#FCD34D;
  --purple:#8B5CF6;--purple-bg:rgba(139,92,246,0.1);
  --text-1:#E8F4FF;--text-2:#7BAED4;--text-3:#3D6B8E;
  --sidebar-w:248px;
  --shadow:0 4px 24px rgba(0,0,0,0.3);
  --radius:14px;
}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--text-1);min-height:100vh;display:flex;font-size:14px;overflow-x:hidden}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}

/* ── SIDEBAR ── */
.sidebar{
  width:var(--sidebar-w);min-height:100vh;
  background:linear-gradient(180deg,var(--bg2) 0%,#071020 100%);
  border-left:1px solid var(--card-border);
  display:flex;flex-direction:column;flex-shrink:0;
  position:fixed;right:0;top:0;bottom:0;z-index:200;
  transition:transform .25s cubic-bezier(.4,0,.2,1);
}
.logo{
  display:flex;align-items:center;gap:12px;
  padding:22px 18px 18px;
  border-bottom:1px solid var(--card-border);
}
.logo-img{
  width:40px;height:40px;border-radius:11px;overflow:hidden;
  border:1px solid var(--card-border);
  box-shadow:0 0 16px var(--accent-glow);flex-shrink:0;
}
.logo-img img{width:100%;height:100%;object-fit:cover}
.logo-name{font-size:14px;font-weight:700;color:var(--text-1);letter-spacing:.01em}
.logo-sub{font-size:10.5px;color:var(--text-3);margin-top:2px}
.sidebar-close{display:none;position:absolute;left:14px;top:22px;background:var(--accent-dim);border:1px solid var(--card-border);color:var(--text-2);width:32px;height:32px;border-radius:9px;font-size:17px;align-items:center;justify-content:center;cursor:pointer}
.nav-scroll{flex:1;overflow-y:auto;padding:8px 0 10px}
.nav-section{padding:16px 16px 4px;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);font-weight:600}
.nav-item{
  display:flex;align-items:center;gap:10px;
  padding:9px 16px;
  color:var(--text-3);font-size:12.5px;cursor:pointer;
  border-right:2px solid transparent;
  transition:all .15s;user-select:none;margin:1px 8px;
  border-radius:10px;position:relative;
}
.nav-item i{font-size:17px;width:19px;text-align:center;flex-shrink:0}
.nav-item:hover{background:var(--accent-dim);color:var(--text-2)}
.nav-item.active{background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(59,130,246,0.05));color:var(--text-1);border-right-color:var(--accent)}
.nav-badge{margin-right:auto;background:rgba(59,130,246,0.15);color:var(--accent-2);font-size:9.5px;padding:1px 7px;border-radius:20px;font-weight:700}
.sidebar-footer{padding:14px 16px;border-top:1px solid var(--card-border)}
.tg-link{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#0098e6,#0077bb);color:#fff;border-radius:10px;padding:10px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:.15s;box-shadow:0 4px 14px rgba(0,136,204,0.25)}
.tg-link:hover{filter:brightness(1.1)}
.tg-link i{font-size:17px}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-text);border-radius:10px;padding:9px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:8px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}

/* MOBILE */
.mobile-topbar{display:none;position:fixed;top:0;right:0;left:0;height:54px;background:var(--bg2);border-bottom:1px solid var(--card-border);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mobile-topbar .mt-left{display:flex;align-items:center;gap:10px}
.mobile-topbar .mt-logo{width:30px;height:30px;border-radius:8px;overflow:hidden}
.mobile-topbar .mt-logo img{width:100%;height:100%;object-fit:cover}
.mobile-topbar .mt-title{color:var(--text-1);font-size:13.5px;font-weight:700}
.menu-btn{background:var(--accent-dim);border:1px solid var(--card-border);color:var(--text-2);width:36px;height:36px;border-radius:9px;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer}
.sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:190;backdrop-filter:blur(4px)}
.sidebar-overlay.show{display:block}

/* MAIN */
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0}
.page{display:none}
.page.active{display:block;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* TOPBAR */
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px}
.topbar-title{font-size:19px;font-weight:700;color:var(--text-1);display:flex;align-items:center;gap:9px;letter-spacing:-.02em}
.topbar-title i{color:var(--accent);font-size:21px}
.topbar-sub{font-size:11.5px;color:var(--text-3);margin-top:5px}
.topbar-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}

/* BADGES */
.badge{font-size:10.5px;padding:4px 11px;border-radius:20px;font-weight:600;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.badge-green{background:var(--green-bg);color:var(--green-text)}
.badge-blue{background:var(--accent-dim);color:var(--accent-2)}
.badge-amber{background:var(--amber-bg);color:var(--amber-text)}
.badge-red{background:var(--red-bg);color:var(--red-text)}
.badge-purple{background:var(--purple-bg);color:#A78BFA}
.dot{width:6px;height:6px;border-radius:50%;display:inline-block;flex-shrink:0}
.dot-green{background:var(--green)}
.dot-red{background:var(--red)}
.dot-amber{background:var(--amber)}
.dot-blue{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}

/* METRIC CARDS */
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:20px}
.metric{
  background:var(--card);
  border:1px solid var(--card-border);
  border-radius:var(--radius);
  padding:18px 18px 16px;
  transition:all .2s;
  position:relative;overflow:hidden;
}
.metric::before{content:'';position:absolute;top:0;right:0;width:2px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-border-hover);transform:translateY(-2px)}
.metric:hover::before{opacity:1}
.metric-icon{width:36px;height:36px;border-radius:9px;background:var(--accent-dim);display:flex;align-items:center;justify-content:center;margin-bottom:12px;color:var(--accent);font-size:18px}
.metric-label{font-size:10.5px;color:var(--text-3);margin-bottom:5px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.metric-val{font-size:26px;font-weight:700;color:var(--text-1);line-height:1;letter-spacing:-.02em}
.metric-unit{font-size:12px;font-weight:500;color:var(--text-3);margin-right:2px}
.metric-sub{font-size:10.5px;color:var(--text-3);margin-top:7px;display:flex;align-items:center;gap:4px}
.metric.danger .metric-icon{background:var(--red-bg);color:var(--red)}
.metric.danger::before{background:var(--red)}
.metric.success .metric-icon{background:var(--green-bg);color:var(--green)}
.metric.success::before{background:var(--green)}

/* VLESS BOX */
.vless-box{
  background:linear-gradient(135deg,#0a1e3d 0%,#061527 100%);
  border:1px solid rgba(59,130,246,0.2);
  border-radius:16px;padding:22px 24px;margin-bottom:20px;
  box-shadow:0 8px 32px rgba(0,0,0,0.3),0 0 0 1px rgba(59,130,246,0.05);
  position:relative;overflow:hidden;
}
.vless-box::before{
  content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;
  background:radial-gradient(circle,rgba(59,130,246,0.08) 0%,transparent 70%);
  pointer-events:none;
}
.vless-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.vless-title{color:var(--text-2);font-size:11.5px;display:flex;align-items:center;gap:7px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}
.vless-title i{font-size:16px;color:var(--accent)}
.vless-link-wrap{
  background:rgba(0,0,0,0.25);
  border:1px solid rgba(59,130,246,0.15);
  border-radius:10px;padding:14px 16px;
}
.vless-link{color:var(--accent-2);font-size:11px;font-family:ui-monospace,monospace;word-break:break-all;line-height:1.8;opacity:.9}
.vless-actions{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}

/* BUTTONS */
.btn{
  font-family:inherit;font-size:12.5px;font-weight:500;
  border-radius:9px;padding:9px 15px;cursor:pointer;
  display:inline-flex;align-items:center;gap:6px;border:none;
  transition:all .15s;white-space:nowrap;
}
.btn i{font-size:14px}
.btn:disabled{opacity:.45;cursor:not-allowed}
.btn-primary{background:var(--accent);color:#fff;box-shadow:0 2px 12px rgba(59,130,246,0.3)}
.btn-primary:hover{background:#2563EB;box-shadow:0 4px 18px rgba(59,130,246,0.4)}
.btn-outline{background:transparent;border:1px solid var(--card-border);color:var(--text-2)}
.btn-outline:hover{background:var(--accent-dim);border-color:rgba(59,130,246,0.3)}
.btn-ghost{background:var(--accent-dim);color:var(--accent-2);border:1px solid rgba(59,130,246,0.15)}
.btn-ghost:hover{background:rgba(59,130,246,0.2)}
.btn-danger{background:var(--red-bg);color:var(--red-text);border:1px solid rgba(239,68,68,0.2)}
.btn-danger:hover{background:rgba(239,68,68,0.2)}
.btn-success{background:var(--green-bg);color:var(--green-text);border:1px solid rgba(16,185,129,0.2)}
.btn-sm{padding:6px 10px;font-size:11px;border-radius:7px;gap:4px}
.btn-sm i{font-size:12px}

/* CARDS */
.card{background:var(--card);border:1px solid var(--card-border);border-radius:var(--radius);padding:20px 22px;transition:border-color .2s}
.card:hover{border-color:var(--card-border-hover)}
.card-title{font-size:13px;font-weight:700;color:var(--text-1);margin-bottom:16px;display:flex;align-items:center;gap:8px}
.card-title i{font-size:17px;color:var(--accent)}
.ml-auto{margin-right:auto}

/* GRID */
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px}
.grid3{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:18px}
.gap-18{margin-bottom:18px}

/* STATUS ROWS */
.status-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid rgba(59,130,246,0.06);font-size:12.5px}
.status-row:last-child{border-bottom:none}
.status-key{color:var(--text-2);display:flex;align-items:center;gap:7px}
.status-key i{font-size:14px;color:var(--text-3)}
.status-val{color:var(--text-1);font-weight:600;font-size:12px}

/* CHART */
.chart-wrap{position:relative;height:220px;width:100%}
.chart-wrap-lg{position:relative;height:320px;width:100%}
.chart-wrap-sm{position:relative;height:170px;width:100%}

/* LINKS TABLE */
.links-table{width:100%;border-collapse:collapse}
.links-table th{text-align:right;font-size:10px;color:var(--text-3);font-weight:600;padding:10px 10px;border-bottom:1px solid var(--card-border);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.links-table td{padding:12px 10px;border-bottom:1px solid rgba(59,130,246,0.05);font-size:12.5px;vertical-align:middle}
.links-table tr:last-child td{border-bottom:none}
.links-table tbody tr{transition:.15s}
.links-table tbody tr:hover td{background:rgba(59,130,246,0.03)}
.link-uuid{font-family:ui-monospace,monospace;font-size:10px;color:var(--accent-2);background:var(--accent-dim);padding:3px 7px;border-radius:6px;display:inline-block;letter-spacing:.03em}
.usage-bar{height:6px;border-radius:4px;background:rgba(59,130,246,0.1);overflow:hidden;margin-bottom:4px}
.usage-bar-fill{height:100%;border-radius:4px;transition:width .3s}
.usage-text{font-size:10px;color:var(--text-3)}
.link-label{font-weight:600;color:var(--text-1)}
.link-meta{font-size:10px;color:var(--text-3);margin-top:2px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.expiry-badge{font-size:9.5px;padding:2px 7px;border-radius:5px;font-weight:600;display:inline-flex;align-items:center;gap:3px}
.expiry-ok{background:rgba(16,185,129,0.1);color:var(--green-text)}
.expiry-warn{background:var(--amber-bg);color:var(--amber-text)}
.expiry-exp{background:var(--red-bg);color:var(--red-text)}
.expiry-none{background:var(--accent-dim);color:var(--accent-2)}

/* TOGGLE */
.toggle{width:36px;height:20px;border-radius:20px;background:rgba(59,130,246,0.15);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:1px solid var(--card-border)}
.toggle::after{content:'';position:absolute;width:14px;height:14px;border-radius:50%;background:var(--text-3);top:2px;right:2px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.toggle.on{background:var(--green);border-color:var(--green)}
.toggle.on::after{right:18px;background:#fff}

/* FORM */
.form-row{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
.form-group{display:flex;flex-direction:column;gap:6px}
.form-label{font-size:10.5px;color:var(--text-3);font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.form-input,.form-select{
  padding:10px 13px;border-radius:9px;
  border:1px solid var(--card-border);
  background:rgba(0,0,0,0.25);
  color:var(--text-1);font-family:inherit;font-size:12.5px;outline:none;
  transition:all .15s;min-width:110px;
}
.form-input::placeholder{color:var(--text-3)}
.form-input:focus,.form-select:focus{border-color:rgba(59,130,246,0.4);background:rgba(0,0,0,0.35);box-shadow:0 0 0 3px rgba(59,130,246,0.08)}
.form-select option{background:var(--bg2)}

/* CALLOUT */
.callout{
  background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);
  border-radius:11px;padding:13px 15px;font-size:11.5px;color:var(--text-2);
  display:flex;gap:10px;align-items:flex-start;line-height:1.8;margin-top:14px;
}
.callout i{font-size:16px;color:var(--accent);margin-top:1px;flex-shrink:0}
.callout.amber{background:var(--amber-bg);border-color:rgba(245,158,11,0.2);color:var(--amber-text)}
.callout.amber i{color:var(--amber)}
.callout.red{background:var(--red-bg);border-color:rgba(239,68,68,0.2);color:var(--red-text)}
.callout.red i{color:var(--red)}

/* SUB BOX */
.sub-box{
  background:linear-gradient(135deg,rgba(139,92,246,0.08) 0%,rgba(59,130,246,0.05) 100%);
  border:1px solid rgba(139,92,246,0.2);
  border-radius:12px;padding:16px 18px;
  display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
  margin-top:12px;
}
.sub-url{font-family:ui-monospace,monospace;font-size:11px;color:#A78BFA;word-break:break-all;flex:1}
.sub-actions{display:flex;gap:7px;flex-shrink:0}

/* ERRORS */
.err-row{padding:10px 0;border-bottom:1px solid rgba(59,130,246,0.06)}
.err-row:last-child{border-bottom:none}
.err-time{color:var(--text-3);font-size:10px;margin-bottom:3px;display:flex;align-items:center;gap:5px}
.err-msg{color:var(--red-text);font-family:ui-monospace,monospace;background:var(--red-bg);padding:7px 10px;border-radius:7px;word-break:break-all;font-size:11px}

/* BWBAR */
.speed-bar{height:5px;border-radius:3px;background:rgba(59,130,246,0.1);overflow:hidden;margin-top:5px}
.speed-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent-2));transition:width 1s}

/* EMPTY STATE */
.empty-state{text-align:center;padding:50px 20px;color:var(--text-3)}
.empty-state i{font-size:40px;color:var(--text-3);margin-bottom:12px;display:block;opacity:.5}
.empty-state p{font-size:12.5px;margin-top:6px}

/* IDEA CARDS */
.idea-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.idea-card{background:var(--card);border:1px solid var(--card-border);border-radius:14px;padding:18px;transition:.2s}
.idea-card:hover{border-color:var(--card-border-hover);transform:translateY(-2px)}
.idea-icon{width:38px;height:38px;border-radius:10px;background:var(--accent-dim);display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:19px;margin-bottom:12px}
.idea-title{font-size:13px;font-weight:700;color:var(--text-1);margin-bottom:6px}
.idea-desc{font-size:11px;color:var(--text-3);line-height:1.8}
.idea-badge{display:inline-block;margin-top:10px;font-size:9.5px;padding:2px 9px;border-radius:20px;font-weight:600}
.idea-badge.done{background:var(--green-bg);color:var(--green-text)}
.idea-badge.suggest{background:var(--accent-dim);color:var(--accent-2)}

/* TOAST */
.toast{
  position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(40px);
  background:var(--card);border:1px solid var(--card-border);
  color:var(--text-1);border-radius:11px;padding:11px 20px;font-size:13px;
  opacity:0;transition:all .25s;z-index:999;pointer-events:none;
  display:flex;align-items:center;gap:9px;box-shadow:0 8px 30px rgba(0,0,0,.4);
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.err{border-color:rgba(239,68,68,0.3);background:rgba(239,68,68,0.1);color:var(--red-text)}
.toast.ok{border-color:rgba(16,185,129,0.3);background:rgba(16,185,129,0.1);color:var(--green-text)}

/* FOOTER */
.dash-footer{border-top:1px solid var(--card-border);margin-top:16px;padding-top:16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
.footer-text{font-size:10.5px;color:var(--text-3)}
.footer-link{font-size:12px;color:var(--accent-2);display:flex;align-items:center;gap:5px;font-weight:500}
.footer-link:hover{color:var(--text-1)}

/* CONN ITEM */
.conn-item{padding:12px 14px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.12);border-radius:10px;margin-bottom:8px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.conn-dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);flex-shrink:0}

@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,.5)}
  .sidebar-close{display:flex}
  .main{margin-right:0;padding-top:72px}
  .mobile-topbar{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .grid2,.grid3{grid-template-columns:1fr}
  .idea-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:520px){
  .metrics{grid-template-columns:1fr}
  .main{padding:64px 14px 50px}
  .idea-grid{grid-template-columns:1fr}
  .links-table th:nth-child(2),.links-table td:nth-child(2){display:none}
}
</style>
</head>
<body>

<div class="toast" id="toast"></div>

<div class="mobile-topbar">
  <div class="mt-left">
    <div class="mt-logo"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="codebox"></div>
    <span class="mt-title">RVG Gateway</span>
  </div>
  <button class="menu-btn" id="open-sidebar-btn"><i class="ti ti-menu-2"></i></button>
</div>

<div class="sidebar-overlay" id="sidebar-overlay"></div>

<aside class="sidebar" id="sidebar">
  <button class="sidebar-close" id="close-sidebar-btn"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="logo-img"><img src="https://yt3.googleusercontent.com/vA6bYj1V386YmibpWRNFJtsRRqwfY_U9wnb7gmW90eRVXyNB7gAfjj1XPs5UX0cdKdQprrI=s160-c-k-c0x00ffffff-no-rj" alt="codebox"></div>
    <div>
      <div class="logo-name">codebox</div>
      <div class="logo-sub">RVG Gateway · v7.0</div>
    </div>
  </div>

  <div class="nav-scroll">
    <div class="nav-section">پنل</div>
    <div class="nav-item active" data-page="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-item" data-page="links"><i class="ti ti-link-plus"></i> مدیریت لینک‌ها <span class="nav-badge" id="links-count-badge">0</span></div>
    <div class="nav-item" data-page="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-item" data-page="traffic"><i class="ti ti-chart-area"></i> آمار ترافیک</div>
    <div class="nav-item" data-page="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-count-badge">0</span></div>
    <div class="nav-section">سیستم</div>
    <div class="nav-item" data-page="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-item" data-page="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-item" data-page="ideas"><i class="ti ti-bulb"></i> ایده‌ها</div>
    <div class="nav-item" data-page="testws"><i class="ti ti-wifi"></i> تست WebSocket</div>
    <div class="nav-item" data-page="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>

  <div class="sidebar-footer">
    <a class="tg-link" href="https://t.me/CodeBoxo" target="_blank" rel="noopener">
      <i class="ti ti-brand-telegram"></i> @CodeBoxo
    </a>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج از حساب</button>
  </div>
</aside>

<main class="main">

  <!-- ═══ OVERVIEW ═══ -->
  <section class="page active" id="page-overview">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
        <div class="topbar-sub" id="last-update">در حال بارگذاری...</div>
      </div>
      <div class="topbar-right">
        <span class="badge badge-green"><span class="dot dot-green pulse"></span> سرور فعال</span>
        <span class="badge badge-blue" id="uptime-badge">—</span>
        <button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
      </div>
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="metric-icon"><i class="ti ti-plug-connected"></i></div>
        <div class="metric-label">اتصالات فعال</div>
        <div class="metric-val" id="m-conns">—</div>
        <div class="metric-sub"><span class="dot dot-green" style="animation:pulse 2s infinite"></span> WebSocket زنده</div>
      </div>
      <div class="metric">
        <div class="metric-icon"><i class="ti ti-transfer"></i></div>
        <div class="metric-label">کل ترافیک</div>
        <div class="metric-val" id="m-traffic">—<span class="metric-unit">MB</span></div>
        <div class="metric-sub">از راه‌اندازی سرویس</div>
      </div>
      <div class="metric success">
        <div class="metric-icon"><i class="ti ti-link"></i></div>
        <div class="metric-label">لینک‌های فعال</div>
        <div class="metric-val" id="m-active-links">—</div>
        <div class="metric-sub" id="m-links-sub">از کل لینک‌ها</div>
      </div>
      <div class="metric danger">
        <div class="metric-icon"><i class="ti ti-alert-circle"></i></div>
        <div class="metric-label">خطاها</div>
        <div class="metric-val" id="m-errors">—</div>
        <div class="metric-sub">ثبت شده</div>
      </div>
    </div>

    <div class="vless-box">
      <div class="vless-header">
        <div class="vless-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
        <span class="badge badge-blue"><span class="dot dot-blue" style="margin-left:4px"></span>TLS 443 · WS</span>
      </div>
      <div class="vless-link-wrap">
        <div class="vless-link" id="vless-link-overview">در حال دریافت...</div>
      </div>
      <div class="vless-actions">
        <button class="btn btn-primary" onclick="copyText('vless-link-overview')"><i class="ti ti-copy"></i> کپی لینک</button>
        <button class="btn btn-ghost" onclick="qrFor('vless-link-overview')"><i class="ti ti-qrcode"></i> QR کد</button>
        <button class="btn btn-outline" onclick="switchPage('links')"><i class="ti ti-link-plus"></i> ساخت لینک محدود</button>
        <button class="btn btn-outline" onclick="switchPage('subscriptions')"><i class="ti ti-rss"></i> سابسکریپشن</button>
      </div>
    </div>

    <div class="grid3">
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div>
        <div class="chart-wrap"><canvas id="trafficChart"></canvas></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-chart-donut"></i> توزیع ترافیک</div>
        <div class="chart-wrap-sm"><canvas id="donutChart"></canvas></div>
      </div>
    </div>

    <div class="grid2">
      <div class="card">
        <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس‌ها</div>
        <div class="status-row"><span class="status-key"><i class="ti ti-circle-check"></i> VLESS / WebSocket</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-circle-check"></i> HTTP Proxy</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-rss"></i> Subscription API</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-clock"></i> آپتایم</span><span class="status-val" id="uptime-inline">—</span></div>
        <div class="status-row" style="flex-direction:column;align-items:flex-start;gap:5px">
          <div style="width:100%;display:flex;justify-content:space-between">
            <span class="status-key"><i class="ti ti-gauge"></i> بار نسبی</span>
            <span class="status-val" id="bw-pct">—%</span>
          </div>
          <div class="speed-bar" style="width:100%"><div class="speed-fill" id="bw-bar" style="width:0%"></div></div>
        </div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-list"></i> خلاصه لینک‌ها <span class="ml-auto badge badge-blue" id="links-summary-badge">۰</span></div>
        <div id="links-summary-list"><div class="empty-state"><i class="ti ti-link-off"></i><p>هنوز لینکی وجود ندارد</p></div></div>
      </div>
    </div>

    <div class="dash-footer">
      <span class="footer-text">codebox RVG Gateway v7.0 · Railway · 2025</span>
      <a class="footer-link" href="https://t.me/CodeBoxo" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i> t.me/CodeBoxo</a>
    </div>
  </section>

  <!-- ═══ LINKS ═══ -->
  <section class="page" id="page-links">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-link-plus"></i> مدیریت لینک‌ها</div>
        <div class="topbar-sub">ساخت لینک رندوم با محدودیت ترافیک و تاریخ انقضا</div>
      </div>
      <div class="topbar-right">
        <span class="badge badge-blue" id="links-page-count">۰ لینک</span>
      </div>
    </div>

    <div class="card gap-18">
      <div class="card-title"><i class="ti ti-plus"></i> ساخت لینک جدید</div>
      <div class="form-row">
        <div class="form-group" style="flex:1;min-width:160px">
          <label class="form-label">عنوان لینک</label>
          <input class="form-input" id="new-link-label" placeholder="مثلاً: کاربر علی" style="width:100%">
        </div>
        <div class="form-group">
          <label class="form-label">سهمیه ترافیک</label>
          <input class="form-input" id="new-link-value" type="number" min="0" step="0.1" placeholder="0 = بی‌نهایت" style="width:130px">
        </div>
        <div class="form-group">
          <label class="form-label">واحد</label>
          <select class="form-select" id="new-link-unit">
            <option value="GB">گیگابایت (GB)</option>
            <option value="MB" selected>مگابایت (MB)</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">انقضا (روز)</label>
          <input class="form-input" id="new-link-expires" type="number" min="0" step="1" placeholder="0 = بی‌نهایت" style="width:110px">
        </div>
        <div class="form-group" style="flex:1;min-width:140px">
          <label class="form-label">یادداشت (اختیاری)</label>
          <input class="form-input" id="new-link-note" placeholder="توضیح برای خودتان" style="width:100%">
        </div>
        <button class="btn btn-primary" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت لینک</button>
      </div>
      <div class="callout">
        <i class="ti ti-info-circle"></i>
        <span>هر لینک دارای UUID رندوم و یکتا است. سهمیه یا انقضای ۰ یعنی بی‌نهایت. پس از اتمام سهمیه یا تاریخ انقضا، اتصال لینک به‌صورت خودکار مسدود می‌شود.</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> لینک‌های ساخته‌شده</div>
      <div style="overflow-x:auto">
        <table class="links-table">
          <thead>
            <tr>
              <th>عنوان / یادداشت</th>
              <th>UUID</th>
              <th>مصرف / سهمیه</th>
              <th>انقضا</th>
              <th>وضعیت</th>
              <th>عملیات</th>
            </tr>
          </thead>
          <tbody id="links-tbody"></tbody>
        </table>
      </div>
      <div class="empty-state" id="links-empty" style="display:none">
        <i class="ti ti-link-off"></i>
        <p>هنوز هیچ لینکی ساخته نشده. از فرم بالا لینک جدید بسازید.</p>
      </div>
    </div>
  </section>

  <!-- ═══ SUBSCRIPTIONS ═══ -->
  <section class="page" id="page-subscriptions">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-rss"></i> سابسکریپشن</div>
        <div class="topbar-sub">مدیریت و اشتراک‌گذاری لینک‌های سابسکریپشن</div>
      </div>
    </div>

    <div class="grid2">
      <div class="card">
        <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر لینک)</div>
        <p style="font-size:12px;color:var(--text-3);margin-bottom:14px;line-height:1.8">
          هر لینک یک آدرس سابسکریپشن اختصاصی دارد. کاربر می‌تواند این آدرس را در اپلیکیشن v2ray، هیدیفای، استریسند و غیره اضافه کند تا کانفیگ به‌صورت خودکار آپدیت شود.
        </p>
        <div class="callout">
          <i class="ti ti-info-circle"></i>
          <span>آدرس سابسکریپشن برای هر لینک در جدول <b>مدیریت لینک‌ها</b> موجود است. روی آیکون <i class="ti ti-rss"></i> کنار هر لینک کلیک کنید.</span>
        </div>
        <div style="margin-top:14px">
          <div class="status-row"><span class="status-key"><i class="ti ti-world"></i> فرمت</span><span class="status-val">Base64 / VLESS</span></div>
          <div class="status-row"><span class="status-key"><i class="ti ti-shield"></i> احراز هویت</span><span class="status-val">UUID در مسیر URL</span></div>
          <div class="status-row"><span class="status-key"><i class="ti ti-refresh"></i> آپدیت خودکار</span><span class="status-val">پشتیبانی اپ‌های معیار</span></div>
        </div>
      </div>

      <div class="card">
        <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (همه لینک‌های فعال)</div>
        <p style="font-size:12px;color:var(--text-3);margin-bottom:14px;line-height:1.8">
          این آدرس شامل تمام لینک‌های فعال و منقضی‌نشده است. مخصوص استفاده شخصی یا مدیریتی — فقط برای کسانی که به پنل دسترسی دارند.
        </p>
        <div class="sub-box" id="sub-all-box">
          <span class="sub-url" id="sub-all-url">در حال دریافت...</span>
          <div class="sub-actions">
            <button class="btn btn-sm btn-ghost" onclick="copySubAll()"><i class="ti ti-copy"></i></button>
            <button class="btn btn-sm btn-ghost" onclick="openSubAll()"><i class="ti ti-external-link"></i></button>
          </div>
        </div>
        <div class="callout amber" style="margin-top:14px">
          <i class="ti ti-alert-triangle"></i>
          <span>این آدرس نیاز به احراز هویت دارد (سشن کوکی). فقط در مرورگر لاگین‌شده کار می‌کند.</span>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> لینک‌های فعال با آدرس سابسکریپشن</div>
      <div id="sub-links-list" style="font-size:12px;color:var(--text-3)">در حال بارگذاری...</div>
    </div>

    <div class="card" style="margin-top:14px">
      <div class="card-title"><i class="ti ti-device-mobile"></i> اپلیکیشن‌های سازگار</div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-top:4px">
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-brand-android" style="color:var(--accent)"></i> Hiddify (Android)</div>
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-brand-apple" style="color:var(--accent)"></i> Shadowrocket (iOS)</div>
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-device-desktop" style="color:var(--accent)"></i> v2rayN (Windows)</div>
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-apple" style="color:var(--accent)"></i> v2rayU (macOS)</div>
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-device-mobile" style="color:var(--accent)"></i> NekoBox</div>
        <div style="padding:12px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.15);border-radius:10px;font-size:11.5px;color:var(--text-2);display:flex;align-items:center;gap:8px"><i class="ti ti-brand-android" style="color:var(--accent)"></i> V2RayNG</div>
      </div>
    </div>
  </section>

  <!-- ═══ TRAFFIC ═══ -->
  <section class="page" id="page-traffic">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-chart-area"></i> آمار ترافیک</div>
        <div class="topbar-sub">نمایش لحظه‌ای ترافیک Gateway</div>
      </div>
      <div class="topbar-right">
        <button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
      </div>
    </div>
    <div class="metrics" style="grid-template-columns:repeat(3,1fr)">
      <div class="metric">
        <div class="metric-icon"><i class="ti ti-database"></i></div>
        <div class="metric-label">کل ترافیک</div>
        <div class="metric-val" id="t-traffic">—<span class="metric-unit">MB</span></div>
        <div class="metric-sub">آپلود + دانلود</div>
      </div>
      <div class="metric">
        <div class="metric-icon"><i class="ti ti-arrow-up"></i></div>
        <div class="metric-label">میانگین ساعتی</div>
        <div class="metric-val" id="t-avg">—<span class="metric-unit">MB</span></div>
        <div class="metric-sub">بر اساس داده‌های امروز</div>
      </div>
      <div class="metric">
        <div class="metric-icon"><i class="ti ti-chart-bar"></i></div>
        <div class="metric-label">پیک ساعتی</div>
        <div class="metric-val" id="t-peak">—<span class="metric-unit">MB</span></div>
        <div class="metric-sub">بالاترین مصرف</div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-chart-area"></i> نمودار ترافیک ساعتی</div>
      <div class="chart-wrap-lg"><canvas id="trafficChartBig"></canvas></div>
    </div>
  </section>

  <!-- ═══ CONNECTIONS ═══ -->
  <section class="page" id="page-connections">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-plug-connected"></i> اتصالات فعال</div>
        <div class="topbar-sub">WebSocket‌های باز در همین لحظه</div>
      </div>
      <div class="topbar-right">
        <span class="badge badge-green" id="conns-live-badge"><span class="dot dot-green pulse"></span> ۰ اتصال</span>
        <button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> جزئیات</div>
      <div id="conns-list"></div>
      <div class="empty-state" id="conns-empty" style="display:none">
        <i class="ti ti-plug-off"></i>
        <p>هیچ اتصال فعالی وجود ندارد</p>
      </div>
    </div>
  </section>

  <!-- ═══ SECURITY ═══ -->
  <section class="page" id="page-security">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-shield-lock"></i> امنیت</div>
        <div class="topbar-sub">وضعیت امنیتی و دسترسی‌های Gateway</div>
      </div>
    </div>
    <div class="grid2">
      <div class="card">
        <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
        <div class="status-row"><span class="status-key"><i class="ti ti-certificate"></i> TLS / HTTPS</span><span class="status-val" style="color:var(--green-text)">● فعال (443)</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="status-val">Chrome Spoofing</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-network"></i> پروتکل</span><span class="status-val">VLESS over WebSocket</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-key"></i> هش رمز عبور</span><span class="status-val">SHA-256 + Salt</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-cookie"></i> سشن</span><span class="status-val">HttpOnly Cookie · 7 روز</span></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
        <div class="status-row"><span class="status-key"><i class="ti ti-toggle-right"></i> فعال/غیرفعال لینک</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-ban"></i> قطع خودکار</span><span class="status-val" style="color:var(--green-text)">● فعال</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-eye-off"></i> ذخیره محتوا</span><span class="status-val" style="color:var(--green-text)">● خیر</span></div>
      </div>
    </div>
    <div class="callout amber">
      <i class="ti ti-alert-triangle"></i>
      <span>تمام اطلاعات <b>in-memory</b> ذخیره می‌شوند. با ری‌استارت Railway همه لینک‌ها و آمارها حذف خواهند شد. برای ذخیره دائمی، Redis یا PostgreSQL اضافه کنید.</span>
    </div>
  </section>

  <!-- ═══ ERRORS ═══ -->
  <section class="page" id="page-errors">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-alert-triangle"></i> خطاها</div>
        <div class="topbar-sub">آخرین خطاهای ثبت‌شده</div>
      </div>
      <div class="topbar-right">
        <span class="badge badge-red" id="errors-count-badge">۰ خطا</span>
        <button class="btn btn-primary btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div>
      <div id="errors-list-full">در حال بارگذاری...</div>
    </div>
  </section>

  <!-- ═══ IDEAS ═══ -->
  <section class="page" id="page-ideas">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-bulb"></i> ایده‌ها و قابلیت‌ها</div>
        <div class="topbar-sub">قابلیت‌های فعال و پیشنهادی Gateway</div>
      </div>
    </div>
    <div class="idea-grid">
      <div class="idea-card">
        <div class="idea-icon" style="background:var(--green-bg);color:var(--green)"><i class="ti ti-rss"></i></div>
        <div class="idea-title">سابسکریپشن اختصاصی</div>
        <div class="idea-desc">هر لینک دارای URL سابسکریپشن مستقل است. کاربر می‌تواند در هر اپلیکیشن سازگار، کانفیگ را آپدیت خودکار کند.</div>
        <span class="idea-badge done">آماده در v7</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon" style="background:var(--green-bg);color:var(--green)"><i class="ti ti-calendar-x"></i></div>
        <div class="idea-title">تاریخ انقضا برای لینک</div>
        <div class="idea-desc">امکان تعیین روز انقضا برای هر لینک. پس از پایان مدت، اتصال به‌صورت خودکار مسدود می‌شود.</div>
        <span class="idea-badge done">آماده در v7</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon" style="background:var(--green-bg);color:var(--green)"><i class="ti ti-lock-access"></i></div>
        <div class="idea-title">پنل ادمین امن</div>
        <div class="idea-desc">ورود با رمز عبور، سشن HttpOnly، تغییر رمز از داخل پنل و باطل‌شدن سشن‌های قدیمی.</div>
        <span class="idea-badge done">آماده</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-database"></i></div>
        <div class="idea-title">ذخیره‌سازی دائمی با Redis</div>
        <div class="idea-desc">اتصال لینک‌ها، آمار و رمز عبور به Redis تا با ری‌استارت Railway حذف نشوند.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-brand-telegram"></i></div>
        <div class="idea-title">اعلان تلگرامی مصرف</div>
        <div class="idea-desc">ارسال پیام هنگام رسیدن مصرف هر لینک به ۸۰٪ و ۱۰۰٪ سهمیه از طریق Bot API تلگرام.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-calendar-time"></i></div>
        <div class="idea-title">تمدید خودکار لینک</div>
        <div class="idea-desc">ریست خودکار سهمیه در ابتدای هر ماه یا دوره تعیین‌شده برای کاربران ماهانه.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-users"></i></div>
        <div class="idea-title">پروفایل کاربران</div>
        <div class="idea-desc">گروه‌بندی لینک‌ها زیر نام کاربران مختلف با گزارش مصرف جداگانه و مدیریت تیمی.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-route"></i></div>
        <div class="idea-title">Multi-Outbound (چند خروجی)</div>
        <div class="idea-desc">اضافه‌کردن چند سرور خروجی و انتخاب هوشمند بر اساس کمترین تأخیر برای هر کاربر.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
      <div class="idea-card">
        <div class="idea-icon"><i class="ti ti-chart-pie-2"></i></div>
        <div class="idea-title">گزارش روزانه / ماهانه</div>
        <div class="idea-desc">نمودار تجمعی مصرف هر لینک به تفکیک روز و ماه با امکان export CSV.</div>
        <span class="idea-badge suggest">پیشنهادی</span>
      </div>
    </div>
  </section>

  <!-- ═══ TEST WS ═══ -->
  <section class="page" id="page-testws">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-wifi"></i> تست WebSocket</div>
        <div class="topbar-sub">بررسی سریع اتصال WebSocket</div>
      </div>
    </div>
    <div class="card" style="max-width:680px">
      <div class="form-row" style="margin-bottom:13px">
        <div class="form-group" style="flex:1">
          <label class="form-label">UUID</label>
          <input class="form-input" id="ws-uuid" placeholder="UUID لینک (خالی = رندوم)" style="width:100%">
        </div>
        <button class="btn btn-primary" onclick="wsConnect()"><i class="ti ti-plug-connected"></i> اتصال</button>
        <button class="btn btn-danger" onclick="wsDisconnect()"><i class="ti ti-plug-x"></i> قطع</button>
      </div>
      <div class="form-row" style="margin-bottom:13px">
        <input class="form-input" id="ws-msg" placeholder="پیام تست..." style="flex:1">
        <button class="btn btn-outline" onclick="wsSend()"><i class="ti ti-send"></i> ارسال</button>
      </div>
      <div style="background:rgba(0,0,0,0.4);border:1px solid var(--card-border);border-radius:11px;padding:16px;height:260px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:11px;line-height:1.9" id="ws-log">
        <p style="color:var(--text-3)">منتظر اتصال...</p>
      </div>
    </div>
  </section>

  <!-- ═══ SETTINGS ═══ -->
  <section class="page" id="page-settings">
    <div class="topbar">
      <div>
        <div class="topbar-title"><i class="ti ti-settings"></i> تنظیمات</div>
        <div class="topbar-sub">اطلاعات سرور و مدیریت دسترسی</div>
      </div>
    </div>
    <div class="grid2">
      <div class="card">
        <div class="card-title"><i class="ti ti-server"></i> اطلاعات سرور</div>
        <div class="status-row"><span class="status-key"><i class="ti ti-world"></i> دامنه</span><span class="status-val" id="set-host">—</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-route"></i> پورت</span><span class="status-val">443 (TLS)</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-versions"></i> نسخه</span><span class="status-val">RVG Gateway v7.0</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-brand-fastapi"></i> فریم‌ورک</span><span class="status-val">FastAPI + Uvicorn</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-cloud"></i> پلتفرم</span><span class="status-val">Railway</span></div>
        <div class="status-row"><span class="status-key"><i class="ti ti-rss"></i> Sub (همه لینک‌ها)</span><span class="status-val"><code style="font-size:10px;color:var(--accent-2)">/sub-all</code></span></div>
      </div>
      <div class="card">
        <div class="card-title"><i class="ti ti-key"></i> تغییر رمز عبور</div>
        <div class="form-group" style="margin-bottom:12px">
          <label class="form-label">رمز فعلی</label>
          <input class="form-input" type="password" id="cp-current" placeholder="رمز فعلی" style="width:100%">
        </div>
        <div class="form-group" style="margin-bottom:12px">
          <label class="form-label">رمز جدید</label>
          <input class="form-input" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" style="width:100%">
        </div>
        <div class="form-group" style="margin-bottom:16px">
          <label class="form-label">تکرار رمز جدید</label>
          <input class="form-input" type="password" id="cp-confirm" placeholder="تکرار رمز جدید" style="width:100%">
        </div>
        <button class="btn btn-primary" onclick="changePassword()" style="width:100%;justify-content:center"><i class="ti ti-key"></i> تغییر رمز</button>
        <div class="callout" style="margin-top:13px">
          <i class="ti ti-info-circle"></i>
          <span>پس از تغییر رمز، تمام سشن‌های دیگر باطل می‌شوند. رمز پیش‌فرض: <b>123456</b></span>
        </div>
      </div>
    </div>
  </section>

</main>

<script>
let trafficChart, donutChart, trafficChartBig;
let prevTraffic = 0;
let ws;
let currentHost = location.host;

/* ── Toast ── */
function toast(msg, type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2400);
}

/* ── Utils ── */
function fmt(n){return n>=1000?`${(n/1000).toFixed(1)}k`:n}
function fmtBytes(b){
  if(b===0)return '0 B';
  if(b<1024)return b+' B';
  if(b<1024*1024)return (b/1024).toFixed(1)+' KB';
  if(b<1024*1024*1024)return (b/(1024*1024)).toFixed(2)+' MB';
  return (b/(1024*1024*1024)).toFixed(2)+' GB';
}
function toFa(n){return n.toString().replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}

function daysLeft(expiresAt){
  if(!expiresAt) return null;
  const diff = new Date(expiresAt) - new Date();
  return Math.ceil(diff / (1000*60*60*24));
}
function expiryBadge(expiresAt, expired){
  if(expired) return `<span class="expiry-badge expiry-exp"><i class="ti ti-calendar-x"></i> منقضی</span>`;
  if(!expiresAt) return `<span class="expiry-badge expiry-none"><i class="ti ti-infinity"></i> بی‌نهایت</span>`;
  const d = daysLeft(expiresAt);
  if(d<=3) return `<span class="expiry-badge expiry-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)} روز</span>`;
  const date = new Date(expiresAt).toLocaleDateString('fa-IR');
  return `<span class="expiry-badge expiry-ok"><i class="ti ti-calendar-check"></i> ${date}</span>`;
}

/* ── Auth ── */
async function checkAuth(){
  try{
    const r=await fetch('/api/me');
    const d=await r.json();
    if(!d.authenticated) location.href='/login';
  }catch(e){location.href='/login'}
}
async function logout(){
  try{await fetch('/api/logout',{method:'POST'})}catch(e){}
  location.href='/login';
}
document.getElementById('logout-btn').addEventListener('click',logout);

/* ── Change Password ── */
async function changePassword(){
  const cur=document.getElementById('cp-current').value;
  const nw=document.getElementById('cp-new').value;
  const cf=document.getElementById('cp-confirm').value;
  if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}
  if(nw.length<4){toast('رمز جدید حداقل ۴ کاراکتر','err');return}
  if(nw!==cf){toast('تکرار رمز اشتباه است','err');return}
  try{
    const r=await authFetch('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok) throw new Error(d.detail||'خطا');
    toast('رمز عبور تغییر کرد','ok');
    ['cp-current','cp-new','cp-confirm'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast('✗ '+e.message,'err')}
}

/* ── Mobile Sidebar ── */
const sidebar=document.getElementById('sidebar');
const overlay=document.getElementById('sidebar-overlay');
function openSidebar(){sidebar.classList.add('open');overlay.classList.add('show')}
function closeSidebar(){sidebar.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sidebar-btn').addEventListener('click',openSidebar);
document.getElementById('close-sidebar-btn').addEventListener('click',closeSidebar);
overlay.addEventListener('click',closeSidebar);

/* ── Navigation ── */
function switchPage(name){
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.dataset.page===name));
  document.querySelectorAll('.page').forEach(p=>p.classList.toggle('active',p.id==='page-'+name));
  if(name==='links') loadLinks();
  if(name==='connections') loadConnections();
  if(name==='errors') loadErrorsFull();
  if(name==='subscriptions') loadSubscriptions();
  closeSidebar();
  window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-item').forEach(item=>{
  item.addEventListener('click',()=>switchPage(item.dataset.page));
});

/* ── Fetch with auth ── */
async function authFetch(url,opts){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}

/* ── Stats ── */
async function fetchStats(){
  try{
    const r=await authFetch('/stats');
    const d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-count-badge').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=`${d.total_traffic_mb.toFixed(1)}<span class="metric-unit">MB</span>`;
    document.getElementById('m-active-links').textContent=d.active_links||'—';
    document.getElementById('m-links-sub').textContent=`از ${d.links_count||0} لینک کل`;
    document.getElementById('m-errors').textContent=d.total_errors;
    document.getElementById('errors-count-badge').textContent=`${d.total_errors} خطا`;
    document.getElementById('uptime-inline').textContent=d.uptime||'—';
    document.getElementById('uptime-badge').textContent=`Railway · ${d.uptime||'—'}`;
    document.getElementById('last-update').textContent=`آخرین بروزرسانی: ${new Date().toLocaleTimeString('fa-IR')}`;
    document.getElementById('conns-live-badge').innerHTML=`<span class="dot dot-green pulse"></span> ${d.active_connections} اتصال`;
    document.getElementById('t-traffic').innerHTML=`${d.total_traffic_mb.toFixed(1)}<span class="metric-unit">MB</span>`;

    const delta=d.total_traffic_mb-prevTraffic;
    const pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=`${pct}%`;
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraffic=d.total_traffic_mb;

    if(d.hourly){
      const labels=Object.keys(d.hourly).sort();
      const vals=labels.map(k=>+(d.hourly[k]/(1024*1024)).toFixed(2));
      [trafficChart,trafficChartBig].forEach(ch=>{
        if(!ch)return;
        ch.data.labels=labels;
        ch.data.datasets[0].data=vals;
        ch.update();
      });
      if(vals.length){
        const avg=vals.reduce((a,b)=>a+b,0)/vals.length;
        const peak=Math.max(...vals);
        document.getElementById('t-avg').innerHTML=`${avg.toFixed(2)}<span class="metric-unit">MB</span>`;
        document.getElementById('t-peak').innerHTML=`${peak.toFixed(2)}<span class="metric-unit">MB</span>`;
      }
    }
    renderErrors(d.recent_errors||[]);
  }catch(e){console.error(e)}
}

function renderErrors(errors){
  const el=document.getElementById('errors-list-full');
  if(errors.length){
    if(el) el.innerHTML=errors.slice().reverse().map(e=>`
      <div class="err-row">
        <div class="err-time"><i class="ti ti-clock"></i> ${new Date(e.time).toLocaleString('fa-IR')}</div>
        <div class="err-msg">${escapeHtml(e.error)}${e.url?' — '+escapeHtml(e.url):''}</div>
      </div>`).join('');
  } else {
    const ok='<div style="color:var(--green-text);padding:12px;display:flex;align-items:center;gap:6px;font-size:12.5px"><i class="ti ti-circle-check"></i> هیچ خطایی ثبت نشده</div>';
    if(el) el.innerHTML=ok;
  }
}

/* ── Links ── */
async function loadLinks(){
  try{
    const r=await authFetch('/api/links');
    const d=await r.json();
    const tbody=document.getElementById('links-tbody');
    const empty=document.getElementById('links-empty');
    const links=d.links||[];

    document.getElementById('links-count-badge').textContent=links.length;
    document.getElementById('links-page-count').textContent=`${toFa(links.length)} لینک`;
    document.getElementById('links-summary-badge').textContent=toFa(links.length);

    if(!links.length){
      tbody.innerHTML='';
      empty.style.display='block';
    } else {
      empty.style.display='none';
      tbody.innerHTML=links.map(l=>{
        const limitTxt = l.limit_bytes===0 ? 'بی‌نهایت' : fmtBytes(l.limit_bytes);
        const pct = l.limit_bytes===0 ? 0 : Math.min(100,(l.used_bytes/l.limit_bytes)*100);
        const barColor = pct>90 ? 'var(--red)' : pct>70 ? 'var(--amber)' : 'var(--accent)';
        const statusIcon = l.expired ? 'ti-calendar-x' : (l.active ? 'ti-circle-check' : 'ti-circle-x');
        const statusColor = l.expired ? 'var(--amber)' : (l.active ? 'var(--green)' : 'var(--red)');
        return `
        <tr>
          <td>
            <div class="link-label">${escapeHtml(l.label)}</div>
            <div class="link-meta">
              <span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span>
              ${l.note ? `<span title="${escapeHtml(l.note)}"><i class="ti ti-note"></i> ${escapeHtml(l.note.slice(0,30))}${l.note.length>30?'...':''}</span>` : ''}
            </div>
          </td>
          <td><span class="link-uuid">${l.uuid.slice(0,13)}...</span></td>
          <td>
            <div style="width:130px">
              <div class="usage-bar"><div class="usage-bar-fill" style="width:${pct}%;background:${barColor}"></div></div>
              <div class="usage-text">${fmtBytes(l.used_bytes)} / ${limitTxt}</div>
            </div>
          </td>
          <td>${expiryBadge(l.expires_at, l.expired)}</td>
          <td>
            <button class="toggle ${l.active&&!l.expired?'on':''}" onclick="toggleActive('${l.uuid}',${!l.active})" title="${l.active?'غیرفعال کن':'فعال کن'}"></button>
          </td>
          <td>
            <div style="display:flex;gap:5px;flex-wrap:nowrap">
              <button class="btn btn-sm btn-ghost" onclick="copyVless('${escapeHtml(l.vless_link).replace(/'/g,"\\'")}')"><i class="ti ti-copy"></i></button>
              <button class="btn btn-sm btn-ghost" onclick="copySubUrl('${escapeHtml(l.sub_url)}')" title="کپی لینک سابسکریپشن"><i class="ti ti-rss"></i></button>
              <button class="btn btn-sm btn-ghost" onclick="qrForText('${l.vless_link.replace(/'/g,"\\'")}')"><i class="ti ti-qrcode"></i></button>
              <button class="btn btn-sm btn-ghost" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
              <button class="btn btn-sm btn-danger" onclick="deleteLink('${l.uuid}')"><i class="ti ti-trash"></i></button>
            </div>
          </td>
        </tr>`;
      }).join('');
    }

    // Overview summary
    const sumEl=document.getElementById('links-summary-list');
    if(!links.length){
      sumEl.innerHTML='<div class="empty-state"><i class="ti ti-link-off"></i><p>لینکی وجود ندارد</p></div>';
    } else {
      sumEl.innerHTML=links.slice(0,6).map(l=>{
        const limitTxt = l.limit_bytes===0 ? 'بی‌نهایت' : fmtBytes(l.limit_bytes);
        const color = l.expired ? 'var(--amber)' : (l.active ? 'var(--green)' : 'var(--red)');
        return `<div class="status-row">
          <span class="status-key" style="gap:6px">
            <i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${color}"></i>
            ${escapeHtml(l.label)}
          </span>
          <span class="status-val" style="font-size:11px">${fmtBytes(l.used_bytes)} / ${limitTxt}</span>
        </div>`;
      }).join('');
    }
  }catch(e){console.error(e)}
}

async function createLink(){
  const label=document.getElementById('new-link-label').value.trim()||'لینک جدید';
  const value=document.getElementById('new-link-value').value;
  const unit=document.getElementById('new-link-unit').value;
  const expires=document.getElementById('new-link-expires').value;
  const note=document.getElementById('new-link-note').value.trim();
  try{
    const r=await authFetch('/api/links',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({label,limit_value:value||0,limit_unit:unit,expires_days:expires||0,note})
    });
    if(!r.ok) throw new Error('failed');
    ['new-link-label','new-link-value','new-link-expires','new-link-note'].forEach(id=>document.getElementById(id).value='');
    toast('لینک جدید ساخته شد','ok');
    loadLinks();
  }catch(e){toast('خطا در ساخت لینک','err')}
}

async function toggleActive(uuid, newState){
  try{
    await authFetch(`/api/links/${uuid}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});
    toast(newState?'لینک فعال شد':'لینک غیرفعال شد','ok');
    loadLinks();
  }catch(e){toast('خطا','err')}
}

async function resetUsage(uuid){
  try{
    await authFetch(`/api/links/${uuid}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});
    toast('مصرف ریست شد','ok');
    loadLinks();
  }catch(e){toast('خطا','err')}
}

async function deleteLink(uuid){
  if(!confirm('آیا از حذف این لینک مطمئن هستید؟')) return;
  try{
    const r=await authFetch(`/api/links/${uuid}`,{method:'DELETE'});
    if(!r.ok) throw new Error('failed');
    toast('لینک حذف شد','ok');
    loadLinks();
  }catch(e){toast('خطا در حذف لینک','err')}
}

function copyVless(text){
  navigator.clipboard.writeText(text).then(()=>toast('لینک VLESS کپی شد','ok'));
}
function copySubUrl(url){
  navigator.clipboard.writeText(url).then(()=>toast('لینک سابسکریپشن کپی شد','ok'));
}
function qrForText(text){
  window.open(`https://api.qrserver.com/v1/create-qr-code/?size=280x280&data=${encodeURIComponent(text)}`,'_blank');
}

/* ── Subscriptions Page ── */
async function loadSubscriptions(){
  const subAllUrl = `${location.protocol}//${location.host}/sub-all`;
  document.getElementById('sub-all-url').textContent = subAllUrl;

  try{
    const r=await authFetch('/api/links');
    const d=await r.json();
    const links=(d.links||[]).filter(l=>l.active && !l.expired);
    const el=document.getElementById('sub-links-list');
    if(!links.length){
      el.innerHTML='<div class="empty-state"><i class="ti ti-rss-off"></i><p>هیچ لینک فعالی وجود ندارد</p></div>';
      return;
    }
    el.innerHTML=links.map(l=>`
      <div style="padding:14px;background:var(--accent-dim);border:1px solid rgba(59,130,246,0.12);border-radius:10px;margin-bottom:8px">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
          <div>
            <div style="font-weight:600;color:var(--text-1);font-size:12.5px;margin-bottom:4px">${escapeHtml(l.label)}</div>
            <div class="sub-url">${escapeHtml(l.sub_url)}</div>
          </div>
          <div style="display:flex;gap:6px">
            <button class="btn btn-sm btn-ghost" onclick="copySubUrl('${escapeHtml(l.sub_url)}')"><i class="ti ti-copy"></i> کپی</button>
            <button class="btn btn-sm btn-ghost" onclick="qrForText('${escapeHtml(l.sub_url)}')"><i class="ti ti-qrcode"></i></button>
          </div>
        </div>
      </div>`).join('');
  }catch(e){console.error(e)}
}

function copySubAll(){
  const url=`${location.protocol}//${location.host}/sub-all`;
  navigator.clipboard.writeText(url).then(()=>toast('آدرس سابسکریپشن کپی شد','ok'));
}
function openSubAll(){
  window.open(`${location.protocol}//${location.host}/sub-all`,'_blank');
}

/* ── Connections ── */
async function loadConnections(){
  try{
    const r=await authFetch('/stats');
    const d=await r.json();
    const list=document.getElementById('conns-list');
    const empty=document.getElementById('conns-empty');
    if(d.active_connections===0){
      list.innerHTML='';
      empty.style.display='block';
    } else {
      empty.style.display='none';
      list.innerHTML=`<div class="conn-item">
        <div class="conn-dot"></div>
        <div style="flex:1;font-size:12px;color:var(--text-2)">${d.active_connections} اتصال فعال در حال انتقال داده</div>
        <span class="badge badge-green">${d.total_traffic_mb.toFixed(1)} MB کل</span>
      </div>`;
    }
  }catch(e){console.error(e)}
}

async function loadErrorsFull(){
  try{
    const r=await authFetch('/stats');
    const d=await r.json();
    renderErrors(d.recent_errors||[]);
  }catch(e){}
}

/* ── VLESS overview ── */
async function fetchOverviewVless(){
  try{
    const r=await authFetch('/api/links');
    const d=await r.json();
    const links=d.links||[];
    const def=links.find(l=>l.limit_bytes===0&&!l.expired&&l.active)||links[0];
    if(def){
      document.getElementById('vless-link-overview').textContent=def.vless_link;
    } else {
      document.getElementById('vless-link-overview').textContent='رفرش کنید یا لینک جدید بسازید...';
    }
  }catch(e){console.error(e)}
}

function copyText(elId){
  const text=document.getElementById(elId).textContent;
  navigator.clipboard.writeText(text).then(()=>toast('لینک کپی شد','ok'));
}
function qrFor(elId){
  const text=document.getElementById(elId).textContent;
  window.open(`https://api.qrserver.com/v1/create-qr-code/?size=280x280&data=${encodeURIComponent(text)}`,'_blank');
}

function refreshAll(){
  fetchStats();
  fetchOverviewVless();
  loadLinks();
  if(document.getElementById('page-subscriptions').classList.contains('active')) loadSubscriptions();
  toast('در حال رفرش...','');
}

/* ── WebSocket Test ── */
function wsLog(cls,msg){
  const log=document.getElementById('ws-log');
  const p=document.createElement('p');
  const colors={ok:'#34D399',err:'#F87171',info:'#7BAED4',sent:'#FCD34D'};
  p.style.color=colors[cls]||'#fff';
  p.textContent=`[${new Date().toLocaleTimeString('fa-IR')}] ${msg}`;
  log.appendChild(p);log.scrollTop=log.scrollHeight;
}
function wsConnect(){
  let uuid=document.getElementById('ws-uuid').value.trim()||crypto.randomUUID();
  const url=`${location.protocol==='https:'?'wss':'ws'}://${location.host}/ws/${uuid}`;
  wsLog('info',`اتصال: ${url}`);
  ws=new WebSocket(url);
  ws.onopen=()=>wsLog('ok','✓ اتصال برقرار');
  ws.onerror=()=>wsLog('err','✗ خطا');
  ws.onmessage=m=>wsLog('info','دریافت ('+(m.data.size||m.data.length)+' byte)');
  ws.onclose=e=>wsLog('err',`قطع (code: ${e.code})`);
}
function wsSend(){
  const m=document.getElementById('ws-msg').value;
  if(!m){wsLog('err','پیام خالی');return}
  if(!ws||ws.readyState!==1){wsLog('err','ابتدا متصل شوید');return}
  ws.send(m);wsLog('sent','ارسال: '+m);
  document.getElementById('ws-msg').value='';
}
function wsDisconnect(){if(ws)ws.close()}

/* ── Charts ── */
function initCharts(){
  const chartDefaults={
    responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:v=>`${v.parsed.y.toFixed(2)} MB`},backgroundColor:'rgba(13,27,46,0.95)',borderColor:'rgba(59,130,246,0.2)',borderWidth:1,titleColor:'#E8F4FF',bodyColor:'#7BAED4'}},
    scales:{
      x:{grid:{color:'rgba(59,130,246,0.04)'},ticks:{color:'#3D6B8E',font:{size:10,family:'Vazirmatn'}}},
      y:{grid:{color:'rgba(59,130,246,0.04)'},ticks:{color:'#3D6B8E',font:{size:10},callback:v=>`${v}MB`}}
    }
  };
  const ds={
    label:'MB',data:[],
    borderColor:'rgba(59,130,246,0.8)',
    backgroundColor:'rgba(59,130,246,0.06)',
    fill:true,tension:0.45,
    pointRadius:3,pointHoverRadius:5,
    pointBackgroundColor:'rgba(59,130,246,0.8)',
    pointBorderColor:'rgba(59,130,246,0.3)',
    borderWidth:2,
  };
  trafficChart=new Chart(document.getElementById('trafficChart'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:chartDefaults});
  trafficChartBig=new Chart(document.getElementById('trafficChartBig'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:chartDefaults});
  donutChart=new Chart(document.getElementById('donutChart'),{
    type:'doughnut',
    data:{
      labels:['VLESS / WS','HTTP Proxy','سایر'],
      datasets:[{data:[70,25,5],backgroundColor:['rgba(59,130,246,0.8)','rgba(16,185,129,0.7)','rgba(139,92,246,0.7)'],borderColor:'rgba(0,0,0,0)',borderWidth:3,hoverOffset:8}]
    },
    options:{
      responsive:true,maintainAspectRatio:false,cutout:'70%',
      plugins:{
        legend:{position:'bottom',labels:{color:'#7BAED4',font:{size:10,family:'Vazirmatn'},padding:12,usePointStyle:true,pointStyleWidth:8}},
        tooltip:{backgroundColor:'rgba(13,27,46,0.95)',borderColor:'rgba(59,130,246,0.2)',borderWidth:1}
      }
    }
  });
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  fetchStats();
  fetchOverviewVless();
  loadLinks();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('page-links').classList.contains('active')) loadLinks();
    if(document.getElementById('page-subscriptions').classList.contains('active')) loadSubscriptions();
  },5000);
});
</script>
</body>
</html>"""


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    await ensure_default_link()
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        return RedirectResponse(url="/login")
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/test-ws", response_class=HTMLResponse)
async def test_ws_redirect():
    return HTMLResponse(content="<script>location.href='/dashboard';</script>")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=CONFIG["port"],
        log_level="info",
        workers=1,
    )
