# pages.py  –  B2 Gateway v9.0
# Developer: tg_khalili  |  Channel: @timazadi

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · B2 Gateway</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--glass:rgba(255,255,255,0.05);--glass-border:rgba(255,255,255,0.08);--glass-hover:rgba(255,255,255,0.1);--glass-shadow:0 8px 50px rgba(0,0,0,0.5);--accent:#7c3aed;--accent2:#6d28d9;--accent3:#a78bfa;--accent-glow:rgba(124,58,237,0.3);--pink:#ec4899;--pink-glow:rgba(236,72,153,0.2);--blue:#3b82f6;--blue-glow:rgba(59,130,246,0.2);--green:#10b981;--text:#f1f5f9;--text2:#94a3b8;--bg1:#0c0a1a;--bg2:#1a1435;--bg3:#241b4a}
body{font-family:'Vazirmatn',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));background-attachment:fixed;overflow:hidden}
.bg-animation{position:fixed;inset:0;z-index:0;overflow:hidden}
.bg-animation .orb{position:absolute;border-radius:50%;filter:blur(130px);animation:float 20s ease-in-out infinite}
.bg-animation .orb:nth-child(1){width:600px;height:600px;background:rgba(124,58,237,0.12);top:-250px;right:-200px;animation-delay:0s}
.bg-animation .orb:nth-child(2){width:450px;height:450px;background:rgba(236,72,153,0.08);bottom:-150px;left:-150px;animation-delay:6s}
.bg-animation .orb:nth-child(3){width:350px;height:350px;background:rgba(59,130,246,0.08);top:50%;left:50%;transform:translate(-50%,-50%);animation-delay:12s}
@keyframes float{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(40px,-50px) scale(1.1)}66%{transform:translate(-40px,40px) scale(0.9)}}
.wrap{position:relative;z-index:10;width:100%;max-width:420px}
.card{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:28px;padding:44px 40px 38px;box-shadow:var(--glass-shadow);transition:all 0.5s ease;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:-50%;right:-50%;width:100%;height:100%;background:radial-gradient(circle,rgba(124,58,237,0.05),transparent 70%);pointer-events:none}
.card::after{content:'';position:absolute;bottom:-50%;left:-50%;width:100%;height:100%;background:radial-gradient(circle,rgba(236,72,153,0.03),transparent 70%);pointer-events:none}
.card:hover{border-color:rgba(255,255,255,0.15);box-shadow:0 8px 60px rgba(0,0,0,0.6);transform:translateY(-2px)}
.brand{display:flex;align-items:center;gap:16px;margin-bottom:30px;position:relative;z-index:1}
.brand-icon{width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--pink));display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900;color:#fff;box-shadow:0 4px 30px var(--accent-glow);flex-shrink:0;position:relative}
.brand-icon::after{content:'';position:absolute;inset:-3px;border-radius:18px;background:linear-gradient(135deg,var(--accent),var(--pink));z-index:-1;filter:blur(15px);opacity:0.5}
.brand-name{font-size:22px;font-weight:800;color:var(--text);letter-spacing:-0.5px;background:linear-gradient(135deg,#fff,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.brand-sub{font-size:11px;color:var(--text2);margin-top:2px;-webkit-text-fill-color:var(--text2)}
h1{font-size:24px;font-weight:800;color:var(--text);margin-bottom:4px;position:relative;z-index:1}
.sub{font-size:13px;color:var(--text2);margin-bottom:26px;line-height:1.7;position:relative;z-index:1}
.hint{display:flex;align-items:center;gap:12px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:10px 18px;margin-bottom:22px;position:relative;z-index:1;transition:0.3s}
.hint:hover{background:rgba(255,255,255,0.06)}
.hint-label{font-size:11px;color:var(--text2);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:16px;font-weight:700;color:var(--accent);background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(236,72,153,0.1));border:1px solid rgba(124,58,237,0.15);padding:4px 16px;border-radius:10px;cursor:pointer;transition:0.3s;letter-spacing:0.08em}
.hint-val:hover{background:linear-gradient(135deg,rgba(124,58,237,0.25),rgba(236,72,153,0.15));transform:scale(1.05);box-shadow:0 0 20px var(--accent-glow)}
.field{margin-bottom:20px;position:relative;z-index:1}
.field label{display:block;font-size:10.5px;font-weight:700;color:var(--text2);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.08em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:15px 48px 15px 18px;border-radius:14px;border:1px solid rgba(255,255,255,0.06);background:rgba(0,0,0,0.25);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:0.4s}
input[type=password]:focus{border-color:rgba(124,58,237,0.3);background:rgba(0,0,0,0.35);box-shadow:0 0 0 4px rgba(124,58,237,0.05),inset 0 0 30px rgba(124,58,237,0.02)}
.ic{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--text2);font-size:18px;pointer-events:none;transition:0.4s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.1);border-radius:14px;padding:12px 16px;margin-bottom:16px;font-size:12px;color:#f87171;align-items:center;gap:10px;position:relative;z-index:1}
.err.show{display:flex}
.btn{width:100%;padding:15px;border-radius:14px;border:none;cursor:pointer;background:linear-gradient(135deg,var(--accent),var(--pink));color:#fff;font-family:inherit;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:0 4px 30px var(--accent-glow);transition:0.4s;position:relative;overflow:hidden;z-index:1}
.btn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.1),transparent);opacity:0;transition:0.4s}
.btn:hover::before{opacity:1}
.btn:hover{transform:translateY(-3px);box-shadow:0 8px 40px var(--accent-glow)}
.btn:disabled{opacity:0.5;cursor:not-allowed;transform:none}
.footer{margin-top:24px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.04);display:flex;align-items:center;justify-content:center;gap:10px;font-size:11px;color:var(--text2);position:relative;z-index:1}
.footer a{color:var(--accent);font-weight:600;text-decoration:none;display:flex;align-items:center;gap:5px;transition:0.3s}
.footer a:hover{color:var(--pink)}
@keyframes spin{to{transform:rotate(360deg)}
</style>
</head>
<body>
<div class="bg-animation"><div class="orb"></div><div class="orb"></div><div class="orb"></div></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-icon">B2</div>
      <div><div class="brand-name">B2 Gateway</div><div class="brand-sub">نسخه ۹ · قدرتمند و سریع</div></div>
    </div>
    <h1>ورود به پنل</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">کانال رسمی <a href="https://t.me/timazadi" target="_blank"><i class="ti ti-brand-telegram"></i>@timazadi</a></div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>B2 Gateway · tg_khalili</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --glass:rgba(255,255,255,0.04);
  --glass-hover:rgba(255,255,255,0.08);
  --glass-border:rgba(255,255,255,0.06);
  --glass-border-hover:rgba(255,255,255,0.15);
  --glass-shadow:0 8px 50px rgba(0,0,0,0.5);
  --accent:#7c3aed;
  --accent2:#6d28d9;
  --accent3:#a78bfa;
  --accent-glow:rgba(124,58,237,0.25);
  --pink:#ec4899;
  --pink-glow:rgba(236,72,153,0.15);
  --blue:#3b82f6;
  --blue-glow:rgba(59,130,246,0.15);
  --green:#10b981;
  --green-glow:rgba(16,185,129,0.12);
  --red:#ef4444;
  --amber:#f59e0b;
  --purple:#8b5cf6;
  --text:#f1f5f9;
  --text2:#94a3b8;
  --text3:#64748b;
  --bg1:#0c0a1a;
  --bg2:#1a1435;
  --bg3:#241b4a;
  --sidebar-w:250px;
  --radius:18px;
}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));background-attachment:fixed;color:var(--text);min-height:100vh;display:flex;font-size:14px}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02)}
::-webkit-scrollbar-thumb{background:linear-gradient(135deg,var(--accent),var(--pink));border-radius:10px}
a{color:inherit;text-decoration:none}
.glass{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);box-shadow:var(--glass-shadow);transition:all 0.4s ease}
.glass:hover{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border-left:1px solid var(--glass-border);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform 0.4s cubic-bezier(0.4,0,0.2,1)}
.sidebar:hover{border-color:var(--glass-border-hover)}
.logo{display:flex;align-items:center;gap:14px;padding:24px 20px 18px;border-bottom:1px solid var(--glass-border)}
.logo-icon{width:44px;height:44px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--pink));display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#fff;box-shadow:0 4px 30px var(--accent-glow);flex-shrink:0;position:relative}
.logo-icon::after{content:'';position:absolute;inset:-3px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--pink));z-index:-1;filter:blur(12px);opacity:0.4}
.logo-name{font-size:16px;font-weight:800;color:var(--text);letter-spacing:-0.3px;background:linear-gradient(135deg,#fff,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo-sub{font-size:10px;color:var(--text2);margin-top:1px;-webkit-text-fill-color:var(--text2)}
.sb-close{display:none;position:absolute;left:14px;top:20px;background:rgba(255,255,255,0.04);border:1px solid var(--glass-border);color:var(--text2);width:34px;height:34px;border-radius:12px;font-size:18px;align-items:center;justify-content:center;cursor:pointer;transition:0.3s}
.sb-close:hover{background:rgba(255,255,255,0.08);color:var(--text)}
.nav-wrap{flex:1;overflow-y:auto;padding:10px 0 10px}
.nav-sec{padding:18px 20px 8px;font-size:9px;letter-spacing:0.16em;text-transform:uppercase;color:var(--text3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:12px;padding:12px 18px;margin:3px 12px;color:var(--text2);font-size:12.5px;cursor:pointer;border-radius:14px;transition:all 0.3s ease}
.nav-it i{font-size:18px;width:22px;text-align:center;flex-shrink:0}
.nav-it:hover{background:rgba(255,255,255,0.05);color:var(--text)}
.nav-it.on{background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(236,72,153,0.08));color:var(--text);box-shadow:inset 0 0 40px rgba(124,58,237,0.03),0 0 20px rgba(124,58,237,0.02)}
.nav-badge{margin-right:auto;background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(236,72,153,0.1));color:var(--accent3);font-size:9px;padding:2px 10px;border-radius:20px;font-weight:700}
.sb-foot{padding:16px 18px;border-top:1px solid var(--glass-border)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:rgba(255,255,255,0.04);color:var(--text2);border-radius:14px;padding:10px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--glass-border);cursor:pointer;width:100%;transition:0.3s;margin-bottom:8px}
.theme-btn:hover{background:rgba(255,255,255,0.08);color:var(--text)}
.tg-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,#1da1f2,#1a8cd8);color:#fff;border-radius:14px;padding:11px;font-size:12.5px;font-weight:600;font-family:inherit;border:none;cursor:pointer;width:100%;transition:0.3s;box-shadow:0 4px 20px rgba(29,161,242,0.2)}
.tg-btn:hover{filter:brightness(1.1);transform:translateY(-2px);box-shadow:0 6px 30px rgba(29,161,242,0.3)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:8px;background:rgba(239,68,68,0.05);color:#f87171;border-radius:14px;padding:10px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.06);cursor:pointer;width:100%;transition:0.3s;margin-top:8px}
.logout-btn:hover{background:rgba(239,68,68,0.1)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:60px;background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border-bottom:1px solid var(--glass-border);z-index:150;align-items:center;justify-content:space-between;padding:0 16px}
.mob-top .ml{display:flex;align-items:center;gap:12px}
.mob-logo{width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,var(--accent),var(--pink));display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:900;color:#fff;flex-shrink:0}
.mob-title{color:var(--text);font-size:15px;font-weight:700}
.mob-right{display:flex;gap:8px}
.menu-btn,.theme-mob{background:rgba(255,255,255,0.04);border:1px solid var(--glass-border);color:var(--text2);width:38px;height:38px;border-radius:12px;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:0.3s}
.menu-btn:hover,.theme-mob:hover{background:rgba(255,255,255,0.08);color:var(--text)}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:190;backdrop-filter:blur(6px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:32px 32px 60px;min-width:0;transition:margin 0.4s}
.pg{display:none;animation:fadeIn 0.5s ease}
.pg.on{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:28px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:22px;font-weight:800;color:var(--text);display:flex;align-items:center;gap:12px;letter-spacing:-0.5px}
.tb-title i{color:var(--accent);font-size:24px;background:linear-gradient(135deg,var(--accent),var(--pink));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tb-sub{font-size:11px;color:var(--text2);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.badge{font-size:10px;padding:5px 14px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;background:rgba(255,255,255,0.04);border:1px solid var(--glass-border)}
.bg-green{background:rgba(16,185,129,0.12);color:#34d399;border-color:rgba(16,185,129,0.08)}
.bg-blue{background:rgba(124,58,237,0.12);color:var(--accent3);border-color:rgba(124,58,237,0.08)}
.bg-amber{background:rgba(245,158,11,0.12);color:#fcd34d;border-color:rgba(245,158,11,0.08)}
.bg-red{background:rgba(239,68,68,0.12);color:#f87171;border-color:rgba(239,68,68,0.08)}
.bg-purple{background:rgba(139,92,246,0.12);color:var(--accent3);border-color:rgba(139,92,246,0.08)}
.bg-pink{background:rgba(236,72,153,0.12);color:#f472b6;border-color:rgba(236,72,153,0.08)}
.dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green);box-shadow:0 0 20px var(--green-glow)}
.dr{background:var(--red);box-shadow:0 0 20px rgba(239,68,68,0.12)}
.da{background:var(--amber);box-shadow:0 0 20px rgba(245,158,11,0.12)}
.db{background:var(--accent);box-shadow:0 0 20px var(--accent-glow)}
.dp{background:var(--purple);box-shadow:0 0 20px rgba(139,92,246,0.12)}
.dpink{background:var(--pink);box-shadow:0 0 20px var(--pink-glow)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.3}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:22px}
.metric{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:20px 20px 16px;transition:all 0.4s ease;position:relative;overflow:hidden;cursor:default;box-shadow:var(--glass-shadow)}
.metric::before{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:linear-gradient(180deg,var(--accent),var(--pink));opacity:0;transition:0.4s}
.metric::after{content:'';position:absolute;top:-50%;right:-50%;width:100%;height:100%;background:radial-gradient(circle,rgba(124,58,237,0.03),transparent 70%);pointer-events:none}
.metric:hover{border-color:var(--glass-border-hover);transform:translateY(-4px);background:var(--glass-hover);box-shadow:0 12px 60px rgba(0,0,0,0.5)}
.metric:hover::before{opacity:1}
.metric.suc::before{background:linear-gradient(180deg,var(--green),#059669)}
.metric.dan::before{background:linear-gradient(180deg,var(--red),#dc2626)}
.metric.pur::before{background:linear-gradient(180deg,var(--purple),#7c3aed)}
.metric.pink::before{background:linear-gradient(180deg,var(--pink),#db2777)}
.m-icon{width:42px;height:42px;border-radius:12px;background:rgba(124,58,237,0.08);display:flex;align-items:center;justify-content:center;margin-bottom:14px;color:var(--accent);font-size:20px;border:1px solid rgba(124,58,237,0.04);transition:0.3s}
.metric:hover .m-icon{background:rgba(124,58,237,0.15)}
.m-icon.suc{background:rgba(16,185,129,0.08);color:var(--green);border-color:rgba(16,185,129,0.04)}
.metric:hover .m-icon.suc{background:rgba(16,185,129,0.15)}
.m-icon.dan{background:rgba(239,68,68,0.08);color:var(--red);border-color:rgba(239,68,68,0.04)}
.metric:hover .m-icon.dan{background:rgba(239,68,68,0.15)}
.m-icon.pur{background:rgba(139,92,246,0.08);color:var(--purple);border-color:rgba(139,92,246,0.04)}
.metric:hover .m-icon.pur{background:rgba(139,92,246,0.15)}
.m-icon.pink{background:rgba(236,72,153,0.08);color:var(--pink);border-color:rgba(236,72,153,0.04)}
.metric:hover .m-icon.pink{background:rgba(236,72,153,0.15)}
.m-label{font-size:10px;color:var(--text2);margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:0.06em}
.m-val{font-size:28px;font-weight:800;color:var(--text);line-height:1;letter-spacing:-0.5px}
.m-unit{font-size:12px;font-weight:400;color:var(--text2)}
.m-sub{font-size:10px;color:var(--text2);margin-top:6px;display:flex;align-items:center;gap:4px}
.vless-box{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:24px 26px;margin-bottom:22px;box-shadow:var(--glass-shadow);transition:all 0.4s ease;position:relative;overflow:hidden}
.vless-box::before{content:'';position:absolute;top:-30%;right:-20%;width:60%;height:60%;background:radial-gradient(circle,rgba(124,58,237,0.04),transparent 70%);pointer-events:none}
.vless-box:hover{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px;position:relative;z-index:1}
.vl-title{color:var(--text2);font-size:11px;display:flex;align-items:center;gap:8px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em}
.vl-title i{color:var(--accent);font-size:18px}
.vl-code{background:rgba(0,0,0,0.2);border:1px solid var(--glass-border);border-radius:12px;padding:16px 18px;font-size:11px;font-family:ui-monospace,monospace;color:var(--accent3);word-break:break-all;line-height:1.8;letter-spacing:0.02em;position:relative;z-index:1}
.vl-actions{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;position:relative;z-index:1}
.btn{font-family:inherit;font-size:12px;font-weight:600;border-radius:12px;padding:9px 18px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;border:none;transition:all 0.3s ease;white-space:nowrap}
.btn i{font-size:14px}
.btn:disabled{opacity:0.4;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,var(--accent),var(--pink));color:#fff;box-shadow:0 4px 25px var(--accent-glow)}
.btn-p:hover{transform:translateY(-3px);box-shadow:0 8px 35px var(--accent-glow)}
.btn-o{background:rgba(255,255,255,0.04);border:1px solid var(--glass-border);color:var(--text2)}
.btn-o:hover{background:rgba(255,255,255,0.08);border-color:var(--glass-border-hover);color:var(--text);transform:translateY(-2px)}
.btn-g{background:rgba(124,58,237,0.06);color:var(--accent3);border:1px solid rgba(124,58,237,0.06)}
.btn-g:hover{background:rgba(124,58,237,0.12);border-color:rgba(124,58,237,0.12);transform:translateY(-2px)}
.btn-d{background:rgba(239,68,68,0.06);color:#f87171;border:1px solid rgba(239,68,68,0.06)}
.btn-d:hover{background:rgba(239,68,68,0.12);border-color:rgba(239,68,68,0.12);transform:translateY(-2px)}
.btn-pur{background:rgba(139,92,246,0.06);color:var(--accent3);border:1px solid rgba(139,92,246,0.06)}
.btn-pur:hover{background:rgba(139,92,246,0.12);border-color:rgba(139,92,246,0.12);transform:translateY(-2px)}
.btn-pink{background:linear-gradient(135deg,var(--pink),#db2777);color:#fff;box-shadow:0 4px 25px var(--pink-glow)}
.btn-pink:hover{transform:translateY(-3px);box-shadow:0 8px 35px var(--pink-glow)}
.btn-sm{padding:6px 12px;font-size:10.5px;border-radius:10px}
.card{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:22px 24px;transition:all 0.4s ease;box-shadow:var(--glass-shadow);position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:-30%;right:-20%;width:60%;height:60%;background:radial-gradient(circle,rgba(124,58,237,0.02),transparent 70%);pointer-events:none}
.card:hover{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}
.card-title{font-size:13px;font-weight:700;color:var(--text);margin-bottom:18px;display:flex;align-items:center;gap:10px;position:relative;z-index:1}
.card-title i{font-size:18px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:18px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:18px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.03);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--text2);display:flex;align-items:center;gap:8px}
.sr-k i{font-size:15px;color:var(--text3)}
.sr-v{color:var(--text);font-weight:600;font-size:11.5px}
.ch{position:relative;height:210px}
.ch-lg{position:relative;height:310px}
.ch-sm{position:relative;height:165px}
.tbl{width:100%;border-collapse:collapse}
.tbl th{text-align:right;font-size:9.5px;color:var(--text2);font-weight:700;padding:12px 12px;border-bottom:1px solid var(--glass-border);text-transform:uppercase;letter-spacing:0.08em;white-space:nowrap}
.tbl td{padding:14px 12px;border-bottom:1px solid rgba(255,255,255,0.02);font-size:12px;vertical-align:middle}
.tbl tr:last-child td{border-bottom:none}
.tbl tbody tr{transition:0.2s}
.tbl tbody tr:hover td{background:rgba(255,255,255,0.02)}
.uuid-chip{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent3);background:rgba(124,58,237,0.06);padding:4px 10px;border-radius:8px;display:inline-block;letter-spacing:0.02em;cursor:pointer;transition:0.3s;border:1px solid rgba(124,58,237,0.04)}
.uuid-chip:hover{background:rgba(124,58,237,0.12);transform:scale(1.05)}
.sub-chip{font-family:ui-monospace,monospace;font-size:9px;color:#34d399;background:rgba(16,185,129,0.06);padding:3px 10px;border-radius:8px;display:inline-block;border:1px solid rgba(16,185,129,0.04);cursor:pointer;transition:0.3s;max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sub-chip:hover{background:rgba(16,185,129,0.12);transform:scale(1.05)}
.game-tag{font-size:8px;padding:3px 10px;border-radius:6px;background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;font-weight:700;display:inline-flex;align-items:center;gap:4px;margin-right:6px;animation:pulse 2s infinite}
.ubar{height:6px;border-radius:6px;background:rgba(255,255,255,0.03);overflow:hidden;margin-bottom:4px}
.ubar-f{height:100%;border-radius:6px;transition:width 0.6s ease}
.utxt{font-size:9.5px;color:var(--text2)}
.ll{font-weight:600;color:var(--text);font-size:12.5px}
.lm{font-size:9.5px;color:var(--text2);margin-top:4px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.exp-chip{font-size:9px;padding:3px 10px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:4px}
.ec-ok{background:rgba(16,185,129,0.08);color:#34d399}
.ec-warn{background:rgba(245,158,11,0.08);color:#fcd34d}
.ec-exp{background:rgba(239,68,68,0.08);color:#f87171}
.ec-inf{background:rgba(124,58,237,0.08);color:var(--accent3)}
.tog{width:38px;height:22px;border-radius:22px;background:rgba(255,255,255,0.04);position:relative;cursor:pointer;transition:0.4s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:15px;height:15px;border-radius:50%;background:#fff;top:3.5px;right:3.5px;transition:0.4s;box-shadow:0 2px 10px rgba(0,0,0,0.3)}
.tog.on{background:linear-gradient(135deg,var(--green),#059669)}
.tog.on::after{right:20px}
.form-row{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:6px}
.fg label{font-size:10px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:0.07em}
.fi,.fs{padding:11px 16px;border-radius:12px;border:1px solid var(--glass-border);background:rgba(0,0,0,0.15);color:var(--text);font-family:inherit;font-size:12px;outline:none;transition:0.3s;min-width:100px}
.fi::placeholder{color:var(--text3)}
.fi:focus,.fs:focus{border-color:rgba(124,58,237,0.25);background:rgba(0,0,0,0.25);box-shadow:0 0 0 4px rgba(124,58,237,0.04)}
.fs option{background:#1a1435}
.cl{background:rgba(124,58,237,0.03);border:1px solid rgba(124,58,237,0.04);border-radius:12px;padding:14px 16px;font-size:11px;color:var(--text2);display:flex;gap:12px;align-items:flex-start;line-height:1.8;margin-top:14px}
.cl i{font-size:18px;color:var(--accent);margin-top:2px;flex-shrink:0}
.cl.amber{background:rgba(245,158,11,0.03);border-color:rgba(245,158,11,0.04);color:#fcd34d}
.cl.amber i{color:var(--amber)}
.sub-box{background:rgba(139,92,246,0.03);border:1px solid rgba(139,92,246,0.04);border-radius:12px;padding:16px 18px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:14px}
.sub-url{font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent3);word-break:break-all;flex:1}
.erow{padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.02)}
.erow:last-child{border-bottom:none}
.etime{color:var(--text2);font-size:9.5px;margin-bottom:4px;display:flex;align-items:center;gap:5px}
.emsg{color:#f87171;font-family:ui-monospace,monospace;background:rgba(239,68,68,0.03);padding:8px 12px;border-radius:8px;word-break:break-all;font-size:10.5px;border:1px solid rgba(239,68,68,0.03)}
.spbar{height:4px;border-radius:4px;background:rgba(255,255,255,0.02);margin-top:6px;overflow:hidden}
.spfill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--accent),var(--pink));transition:width 1s ease}
.empty{text-align:center;padding:50px 20px;color:var(--text2)}
.empty i{font-size:44px;opacity:0.3;margin-bottom:14px;display:block}
.empty p{font-size:12px;margin-top:4px}
.sub-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-bottom:18px}
.sub-card{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:22px 24px;transition:all 0.4s ease;position:relative;overflow:hidden;box-shadow:var(--glass-shadow)}
.sub-card::before{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:linear-gradient(180deg,var(--purple),var(--pink));opacity:0.3}
.sub-card::after{content:'';position:absolute;top:-30%;right:-20%;width:60%;height:60%;background:radial-gradient(circle,rgba(139,92,246,0.02),transparent 70%);pointer-events:none}
.sub-card:hover{border-color:var(--glass-border-hover);transform:translateY(-4px);background:var(--glass-hover);box-shadow:0 12px 60px rgba(0,0,0,0.5)}
.sub-card-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:14px}
.sub-card-name{font-size:16px;font-weight:700;color:var(--text)}
.sub-card-desc{font-size:11px;color:var(--text2);margin-top:4px;line-height:1.6}
.sub-card-meta{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}
.sub-meta-item{display:flex;align-items:center;gap:5px;font-size:10px;color:var(--text2)}
.sub-meta-item i{font-size:12px}
.sub-card-footer{display:flex;gap:8px;flex-wrap:wrap;padding-top:14px;border-top:1px solid var(--glass-border)}
.pub-url-box{background:rgba(139,92,246,0.02);border:1px solid rgba(139,92,246,0.04);border-radius:10px;padding:12px 16px;display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.pub-url-text{font-family:ui-monospace,monospace;font-size:10px;color:var(--accent3);word-break:break-all;flex:1}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(10px)}
.modal-bg.open{display:flex}
.modal{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:22px;padding:32px 30px;max-width:540px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fadeIn 0.4s ease;box-shadow:var(--glass-shadow)}
.modal-close{position:absolute;top:16px;left:16px;background:rgba(255,255,255,0.04);border:1px solid var(--glass-border);color:var(--text2);width:34px;height:34px;border-radius:12px;font-size:18px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:0.3s;border:none}
.modal-close:hover{background:rgba(255,255,255,0.08);color:var(--text)}
.modal-title{font-size:18px;font-weight:700;color:var(--text);margin-bottom:20px;display:flex;align-items:center;gap:10px}
.modal-title i{color:var(--accent);font-size:22px}
.lrow{display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.02)}
.lrow:last-child{border-bottom:none}
.lrow-check{width:19px;height:19px;border-radius:6px;cursor:pointer;accent-color:var(--accent)}
.lrow-label{flex:1;font-size:12px;color:var(--text)}
.lrow-badge{font-size:9px;padding:3px 10px;border-radius:6px;background:rgba(16,185,129,0.08);color:#34d399;font-weight:700}
.toast{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(50px);background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);color:var(--text);border-radius:14px;padding:14px 26px;font-size:13px;opacity:0;transition:all 0.4s ease;z-index:999;pointer-events:none;display:flex;align-items:center;gap:10px;box-shadow:var(--glass-shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,0.12);background:rgba(16,185,129,0.04);color:#34d399}
.toast.err{border-color:rgba(239,68,68,0.12);background:rgba(239,68,68,0.04);color:#f87171}
.dash-footer{border-top:1px solid var(--glass-border);margin-top:18px;padding-top:18px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
.df-text{font-size:10px;color:var(--text2)}
.df-link{font-size:11.5px;color:var(--accent3);display:flex;align-items:center;gap:6px;font-weight:600;transition:0.3s}
.df-link:hover{color:var(--pink)}
@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:var(--glass-shadow)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:78px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:70px 14px 50px}
  .tbl th:nth-child(2),.tbl td:nth-child(2){display:none}
  .sub-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
<div class="toast" id="toast"></div>

<!-- مودال تغییر لینک ساب -->
<div class="modal-bg" id="modal-sub-link">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-sub-link')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-pencil"></i> تغییر لینک ساب</div>
    <div class="fg" style="margin-bottom:14px">
      <label>لینک ساب جدید (اختیاری)</label>
      <input class="fi" id="sub-link-input" placeholder="لینک دلخواه خود را وارد کنید" style="width:100%">
      <div class="cl" style="margin-top:10px"><i class="ti ti-info-circle"></i><span>اگر خالی بگذارید، لینک تصادفی جدید ساخته می‌شود.</span></div>
    </div>
    <input type="hidden" id="sub-link-uuid">
    <div style="margin-top:18px;display:flex;gap:10px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-sub-link')">انصراف</button>
      <button class="btn btn-p" onclick="saveSubLink()"><i class="ti ti-check"></i> ذخیره</button>
    </div>
  </div>
</div>

<!-- مودال ساخت کانفیگ گیم -->
<div class="modal-bg" id="modal-game-config">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-game-config')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-sword"></i> ساخت کانفیگ مخصوص گیم</div>
    <div class="cl amber" style="margin-top:0;margin-bottom:18px"><i class="ti ti-info-circle"></i><span>کانفیگ بهینه برای بازی‌های آنلاین با پینگ پایین و پورت‌های مخصوص</span></div>
    <div class="fg" style="margin-bottom:14px"><label>عنوان کانفیگ</label><input class="fi" id="game-label" placeholder="مثلاً: گیم - کاربر علی" style="width:100%"></div>
    <div class="fg" style="margin-bottom:14px"><label>سهمیه ترافیک</label><input class="fi" id="game-val" type="number" min="0" step="0.1" placeholder="مثلاً: 5" style="width:100%"></div>
    <div class="fg" style="margin-bottom:14px"><label>واحد</label><select class="fs" id="game-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div>
    <div class="fg" style="margin-bottom:18px"><label>پورت اختصاصی گیم (اختیاری)</label><input class="fi" id="game-port" type="number" placeholder="مثلاً: 8080" style="width:100%"></div>
    <div style="margin-top:18px;display:flex;gap:10px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-game-config')">انصراف</button>
      <button class="btn btn-pink" onclick="createGameConfig()"><i class="ti ti-sword"></i> ساخت کانفیگ گیم</button>
    </div>
  </div>
</div>

<!-- مودال مدیریت لینک‌های گروه -->
<div class="modal-bg" id="modal-links">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌های <span id="modal-sub-name" style="color:var(--accent)">—</span></div>
    <div id="modal-links-body">در حال بارگذاری...</div>
    <div style="margin-top:20px;display:flex;gap:10px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-links')">بستن</button>
      <button class="btn btn-p" id="modal-save-btn" onclick="saveSubLinks()"><i class="ti ti-check"></i> ذخیره</button>
    </div>
  </div>
</div>

<!-- مودال ساخت گروه -->
<div class="modal-bg" id="modal-create-sub">
  <div class="modal">
    <button class="modal-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button>
    <div class="modal-title"><i class="ti ti-folder-plus"></i> ساخت گروه جدید</div>
    <div class="fg" style="margin-bottom:14px"><label>نام گروه</label><input class="fi" id="ns-name" placeholder="مثلاً: کانال تلگرام" style="width:100%"></div>
    <div class="fg" style="margin-bottom:14px"><label>توضیحات (اختیاری)</label><input class="fi" id="ns-desc" placeholder="توضیح کوتاه" style="width:100%"></div>
    <div class="fg" style="margin-bottom:18px"><label>رمز صفحه پابلیک (اختیاری)</label><input class="fi" id="ns-pw" type="password" placeholder="خالی = بدون رمز" style="width:100%"></div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>صفحه پابلیک با لینک UUID-based در اینترنت قابل دسترس خواهد بود.</span></div>
    <div style="margin-top:18px;display:flex;gap:10px;justify-content:flex-end">
      <button class="btn btn-o" onclick="closeModal('modal-create-sub')">انصراف</button>
      <button class="btn btn-p" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت</button>
    </div>
  </div>
</div>

<div class="mob-top">
  <div class="ml">
    <div class="mob-logo">B2</div>
    <span class="mob-title">B2 Gateway</span>
  </div>
  <div class="mob-right">
    <button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button>
    <button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button>
  </div>
</div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb">
  <button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button>
  <div class="logo">
    <div class="logo-icon">B2</div>
    <div><div class="logo-name">B2 Gateway</div><div class="logo-sub">نسخه ۹ · قدرتمند و سریع</div></div>
  </div>
  <div class="nav-wrap">
    <div class="nav-sec">پنل</div>
    <div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div>
    <div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div>
    <div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div>
    <div class="nav-it" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div>
    <div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div>
    <div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div>
    <div class="nav-sec">سیستم</div>
    <div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div>
    <div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div>
    <div class="nav-it" data-pg="testws"><i class="ti ti-wifi"></i> تست WebSocket</div>
    <div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div>
  </div>
  <div class="sb-foot">
    <button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button>
    <a class="tg-btn" href="https://t.me/timazadi" target="_blank" rel="noopener"><i class="ti ti-brand-telegram"></i> @timazadi</a>
    <button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج</button>
  </div>
</aside>
<main class="main">
<section class="pg on" id="pg-overview">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد B2</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div>
    <div class="tb-right">
      <span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span>
      <span class="badge bg-blue" id="uptime-badge">—</span>
      <button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button>
    </div>
  </div>
  <div class="metrics">
    <div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div><div class="m-sub"><span class="dot dg pulse"></span> WebSocket زنده</div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div><div class="m-sub">از راه‌اندازی</div></div>
    <div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div><div class="m-sub" id="m-lsub">از کل</div></div>
    <div class="metric pink"><div class="m-icon pink"><i class="ti ti-sword"></i></div><div class="m-label">کانفیگ گیم</div><div class="m-val" id="m-game">—</div><div class="m-sub"><span class="dot dpink pulse"></span> پینگ پایین</div></div>
  </div>
  <div class="vless-box">
    <div class="vl-header">
      <div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض (بدون محدودیت)</div>
      <span class="badge bg-blue"><span class="dot db"></span> TLS 443 · WS</span>
    </div>
    <div class="vl-code" id="vless-main">در حال دریافت...</div>
    <div class="vl-actions">
      <button class="btn btn-p" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button>
      <button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button>
      <button class="btn btn-o" onclick="navTo('links')"><i class="ti ti-link-plus"></i> کانفیگ محدود</button>
      <button class="btn btn-pink" onclick="openModal('modal-game-config')"><i class="ti ti-sword"></i> کانفیگ گیم</button>
    </div>
  </div>
  <div class="g3">
    <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی (MB)</div><div class="ch"><canvas id="ch1"></canvas></div></div>
    <div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:#34d399">● فعال · سخت‌گیرانه</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS / WS Tunnel</span><span class="sr-v" style="color:#34d399">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-sword"></i> Game Mode</span><span class="sr-v" style="color:#fcd34d">● فعال · پورت اختصاصی</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription API</span><span class="sr-v" style="color:#34d399">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div>
      <div class="sr" style="flex-direction:column;align-items:flex-start;gap:4px">
        <div style="width:100%;display:flex;justify-content:space-between"><span class="sr-k"><i class="ti ti-gauge"></i> بار نسبی</span><span class="sr-v" id="bw-pct">—%</span></div>
        <div class="spbar" style="width:100%"><div class="spfill" id="bw-bar" style="width:0%"></div></div>
      </div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto badge bg-blue" id="lsummary-badge">۰</span></div>
      <div id="lsummary">—</div>
    </div>
  </div>
  <div class="dash-footer">
    <span class="df-text">B2 Gateway v9.0 · طراحی توسط tg_khalili · 2025</span>
    <a class="df-link" href="https://t.me/timazadi" target="_blank"><i class="ti ti-brand-telegram"></i> @timazadi</a>
  </div>
</section>

<section class="pg" id="pg-links">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ با سهمیه، انقضا و گروه‌بندی</div></div>
    <div class="tb-right">
      <span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span>
      <button class="btn btn-pink btn-sm" onclick="openModal('modal-game-config')"><i class="ti ti-sword"></i> کانفیگ گیم</button>
    </div>
  </div>
  <div class="card mb16">
    <div class="card-title"><i class="ti ti-plus"></i> ساخت کانفیگ جدید</div>
    <div class="form-row">
      <div class="fg" style="flex:1;min-width:140px"><label>عنوان</label><input class="fi" id="nl-label" placeholder="مثلاً: کاربر علی" style="width:100%"></div>
      <div class="fg"><label>سهمیه</label><input class="fi" id="nl-val" type="number" min="0" step="0.1" placeholder="0=∞" style="width:110px"></div>
      <div class="fg"><label>واحد</label><select class="fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div>
      <div class="fg"><label>انقضا (روز)</label><input class="fi" id="nl-exp" type="number" min="0" step="1" placeholder="0=∞" style="width:100px"></div>
      <div class="fg"><label>گروه ساب</label><select class="fs" id="nl-sub"><option value="">— بدون گروه —</option></select></div>
      <div class="fg" style="flex:1;min-width:120px"><label>یادداشت</label><input class="fi" id="nl-note" placeholder="اختیاری" style="width:100%"></div>
      <button class="btn btn-p" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت</button>
    </div>
    <div class="cl"><i class="ti ti-info-circle"></i><span>UUID کاملاً رندوم · فقط UUID‌های ثبت‌شده می‌توانند اتصال برقرار کنند · می‌توانید بعداً گروه را تغییر دهید.</span></div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-list"></i> لیست کانفیگ‌ها</div>
    <div style="overflow-x:auto">
      <table class="tbl">
        <thead><tr><th>عنوان / یادداشت</th><th>UUID</th><th>مصرف / سهمیه</th><th>گروه</th><th>انقضا</th><th>وضعیت</th><th>عملیات</th></tr></thead>
        <tbody id="links-tb"></tbody>
      </table>
    </div>
    <div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>
  </div>
</section>

<section class="pg" id="pg-subgroups">
  <div class="topbar">
    <div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div><div class="tb-sub">هر گروه یک صفحه پابلیک دارد</div></div>
    <div class="tb-right">
      <span class="badge bg-purple" id="subs-pg-cnt">۰ گروه</span>
      <button class="btn btn-pur" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button>
    </div>
  </div>
  <div class="sub-grid" id="subs-grid">
    <div class="empty" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>
  </div>
</section>

<section class="pg" id="pg-subscriptions">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی (هر کانفیگ)</div>
      <p style="font-size:11.5px;color:var(--text2);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد. از جدول کانفیگ‌ها روی آیکون <i class="ti ti-rss"></i> کلیک کنید.</p>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل (ادمین)</div>
      <p style="font-size:11.5px;color:var(--text2);line-height:1.8;margin-bottom:4px">شامل تمام کانفیگ‌های فعال.</p>
      <div class="sub-box"><span class="sub-url" id="sub-all-url">در حال دریافت...</span><div style="display:flex;gap:6px"><button class="btn btn-sm btn-g" onclick="cpSubAll()"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button></div></div>
      <div class="cl amber"><i class="ti ti-alert-triangle"></i><span>این آدرس فقط در مرورگری که به پنل وارد شده کار می‌کند (نیاز به کوکی سشن).</span></div>
    </div>
  </div>
  <div class="card">
    <div class="card-title"><i class="ti ti-folders"></i> لینک سابسکریپشن گروه‌ها</div>
    <div id="sub-groups-list">در حال بارگذاری...</div>
  </div>
</section>

<section class="pg" id="pg-traffic">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="metrics" style="grid-template-columns:repeat(3,1fr)">
    <div class="metric"><div class="m-icon"><i class="ti ti-database"></i></div><div class="m-label">کل</div><div class="m-val" id="t-traffic">—<span class="m-unit">MB</span></div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-arrow-up"></i></div><div class="m-label">میانگین ساعتی</div><div class="m-val" id="t-avg">—<span class="m-unit">MB</span></div></div>
    <div class="metric"><div class="m-icon"><i class="ti ti-chart-bar"></i></div><div class="m-label">پیک ساعتی</div><div class="m-val" id="t-peak">—<span class="m-unit">MB</span></div></div>
  </div>
  <div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> نمودار ترافیک ساعتی</div><div class="ch-lg"><canvas id="ch3"></canvas></div></div>
</section>

<section class="pg" id="pg-connections">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات</div></div><div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-list"></i> جزئیات</div><div id="conns-list"></div><div class="empty" id="conns-empty" style="display:none"><i class="ti ti-plug-off"></i><p>هیچ اتصال فعالی نیست</p></div></div>
</section>

<section class="pg" id="pg-security">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:#34d399">● فعال (443)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-network"></i> پروتکل</span><span class="sr-v">VLESS/WS</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cookie"></i> سشن</span><span class="sr-v">HttpOnly · 7 روز</span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> UUID Auth سخت‌گیرانه</span><span class="sr-v" style="color:#34d399">● فعال v9</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> فعال/غیرفعال کانفیگ</span><span class="sr-v" style="color:#34d399">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-v" style="color:#34d399">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-calendar-x"></i> تاریخ انقضا</span><span class="sr-v" style="color:#34d399">● فعال</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-sword"></i> حالت گیم</span><span class="sr-v" style="color:#fcd34d">● فعال · پورت اختصاصی</span></div>
    </div>
  </div>
</section>

<section class="pg" id="pg-errors">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">۰</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i></button></div></div>
  <div class="card"><div class="card-title"><i class="ti ti-bug"></i> لاگ خطاها</div><div id="errs-full">—</div></div>
</section>

<section class="pg" id="pg-testws">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-wifi"></i> تست WebSocket</div></div></div>
  <div class="card" style="max-width:660px">
    <div class="cl amber"><i class="ti ti-alert-triangle"></i><span>فقط UUID‌های ثبت‌شده و فعال اتصال برقرار می‌کنند.</span></div>
    <div class="form-row" style="margin-bottom:12px">
      <div class="fg" style="flex:1"><label>UUID (باید در کانفیگ‌ها وجود داشته باشد)</label><input class="fi" id="ws-uuid" placeholder="UUID یک کانفیگ فعال" style="width:100%"></div>
      <button class="btn btn-p" onclick="wsConn()"><i class="ti ti-plug-connected"></i> اتصال</button>
      <button class="btn btn-d" onclick="wsDisc()"><i class="ti ti-plug-x"></i> قطع</button>
    </div>
    <div class="form-row" style="margin-bottom:12px">
      <input class="fi" id="ws-msg" placeholder="پیام تست..." style="flex:1">
      <button class="btn btn-o" onclick="wsSend()"><i class="ti ti-send"></i> ارسال</button>
    </div>
    <div style="background:rgba(0,0,0,0.12);border:1px solid var(--glass-border);border-radius:12px;padding:16px;height:250px;overflow-y:auto;font-family:ui-monospace,monospace;font-size:10.5px;line-height:1.9" id="ws-log">
      <p style="color:var(--text2)">منتظر اتصال...</p>
    </div>
  </div>
</section>

<section class="pg" id="pg-settings">
  <div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div>
  <div class="g2">
    <div class="card">
      <div class="card-title"><i class="ti ti-server"></i> اطلاعات سرور</div>
      <div class="sr"><span class="sr-k"><i class="ti ti-world"></i> دامنه</span><span class="sr-v" id="set-host">—</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-route"></i> پورت</span><span class="sr-v">443 (TLS)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-versions"></i> نسخه</span><span class="sr-v">v9.0</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-brand-fastapi"></i> فریم‌ورک</span><span class="sr-v">FastAPI + Uvicorn</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-cloud"></i> پلتفرم</span><span class="sr-v">Railway</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-device-floppy"></i> ذخیره‌سازی</span><span class="sr-v">JSON File (/data)</span></div>
      <div class="sr"><span class="sr-k"><i class="ti ti-brand-telegram"></i> کانال</span><span class="sr-v"><a href="https://t.me/timazadi" target="_blank" style="color:var(--accent3)">@timazadi</a></span></div>
    </div>
    <div class="card">
      <div class="card-title"><i class="ti ti-key"></i> تغییر رمز عبور</div>
      <div class="fg" style="margin-bottom:12px"><label>رمز فعلی</label><input class="fi" type="password" id="cp-cur" placeholder="رمز فعلی" style="width:100%"></div>
      <div class="fg" style="margin-bottom:12px"><label>رمز جدید</label><input class="fi" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر" style="width:100%"></div>
      <div class="fg" style="margin-bottom:16px"><label>تکرار رمز جدید</label><input class="fi" type="password" id="cp-cf" placeholder="تکرار رمز جدید" style="width:100%"></div>
      <button class="btn btn-p" onclick="changePw()" style="width:100%;justify-content:center"><i class="ti ti-key"></i> تغییر رمز</button>
    </div>
  </div>
</section>
</main>

<script>
// ============== توابع اصلی ==============
let isDark=localStorage.getItem('b2-theme')!=='light';
function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  const icon=dark?'ti-sun':'ti-moon',label=dark?'تم روشن':'تم تاریک';
  const el=document.getElementById('theme-icon');if(el){el.className='ti '+icon}
  const el2=document.getElementById('theme-label');if(el2){el2.textContent=label}
  const mobI=document.getElementById('theme-mob-icon');if(mobI){mobI.className='ti '+icon}
}
function toggleTheme(){isDark=!isDark;localStorage.setItem('b2-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);

function toast(msg,type=''){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2600);
}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5))}
function expChip(exp,expired){
  if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> ∞</span>';
  const d=daysLeft(exp);
  if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';
  if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)}ر</span>`;
  return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)}ر</span>`;
}

async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){
  const r=await fetch(url,opts);
  if(r.status===401){location.href='/login';throw new Error('unauthorized')}
  return r;
}

const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);

function navTo(name){
  document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));
  document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));
  const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs};
  if(loaders[name])loaders[name]();
  closeSb();window.scrollTo({top:0,behavior:'smooth'});
}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}

let prevTraf=0,ch1,ch2,ch3;

// ============== دریافت آمار ==============
async function fetchStats(){
  try{
    const r=await authF('/stats'),d=await r.json();
    document.getElementById('m-conns').textContent=d.active_connections;
    document.getElementById('conns-nb').textContent=d.active_connections;
    document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    document.getElementById('m-alinks').textContent=d.active_links??'—';
    document.getElementById('m-lsub').textContent='از '+d.links_count+' کانفیگ';
    document.getElementById('m-subs').textContent=d.subs_count??'—';
    document.getElementById('m-game').textContent=d.game_links??'—';
    document.getElementById('errs-badge').textContent=d.total_errors+' خطا';
    document.getElementById('uptime-inline').textContent=d.uptime;
    document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;
    document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');
    document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';
    document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';
    const delta=d.total_traffic_mb-prevTraf,pct=Math.min(100,Math.round((delta/50)*100));
    document.getElementById('bw-pct').textContent=pct+'%';
    document.getElementById('bw-bar').style.width=pct+'%';
    prevTraf=d.total_traffic_mb;
    if(d.hourly){
      const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));
      [ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});
      if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}
    }
    renderErrs(d.recent_errors||[]);
  }catch(e){console.error(e)}
}

function renderErrs(errs){
  const el=document.getElementById('errs-full');if(!el)return;
  if(!errs.length){el.innerHTML='<div style="color:#34d399;padding:12px;font-size:12px;display:flex;align-items:center;gap:6px"><i class="ti ti-circle-check"></i> هیچ خطایی نیست</div>';return}
  el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');
}

// ============== بارگذاری کانفیگ‌ها ==============
let allSubsList=[];
async function loadLinks(){
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    allSubsList=subs;
    const nlSub=document.getElementById('nl-sub');
    nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');
    document.getElementById('links-nb').textContent=links.length;
    document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';
    document.getElementById('lsummary-badge').textContent=toFa(links.length);
    const tb=document.getElementById('links-tb'),empty=document.getElementById('links-empty');
    if(!links.length){tb.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
    empty.style.display='none';
    tb.innerHTML=links.map(l=>{
      const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);
      const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);
      const bc=pct>90?'#ef4444':pct>70?'#f59e0b':'#7c3aed';
      const allowed=l.active&&!l.expired;
      const isGame=l.game_mode||false;
      const subOpts='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}"${l.sub_id===s.sub_id?' selected':''}>${esc(s.name)}</option>`).join('');
      return `<tr>
        <td>
          <div class="ll">
            ${esc(l.label)}
            ${isGame ? '<span class="game-tag"><i class="ti ti-sword"></i> گیم</span>' : ''}
          </div>
          <div class="lm">
            <span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span>
            ${l.note?`<span title="${esc(l.note)}"><i class="ti ti-note"></i>${esc(l.note.slice(0,20))}${l.note.length>20?'…':''}</span>`:''}
            ${l.sub_link ? `<span class="sub-chip" onclick="navigator.clipboard.writeText('${esc(l.sub_link)}').then(()=>toast('لینک ساب کپی شد','ok'))" title="${esc(l.sub_link)}"><i class="ti ti-link"></i>${esc(l.sub_link)}</span>` : ''}
          </div>
        </td>
        <td><span class="uuid-chip" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}">${l.uuid.slice(0,13)}…</span></td>
        <td><div style="width:115px"><div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc};box-shadow:0 0 12px ${bc}33"></div></div><div class="utxt">${fmtB(l.used_bytes)} / ${lim}</div></div></td>
        <td><select class="fs" style="font-size:10px;padding:4px 8px;min-width:90px" onchange="moveLinkSub('${l.uuid}',this.value)">${subOpts}</select></td>
        <td>${expChip(l.expires_at,l.expired)}</td>
        <td><button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})"></button></td>
        <td><div style="display:flex;gap:4px;flex-wrap:wrap">
          <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(l.vless_link)}').then(()=>toast('VLESS کپی شد','ok'))" title="کپی VLESS"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-g" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))" title="Sub URL"><i class="ti ti-rss"></i></button>
          <button class="btn btn-sm btn-pur" onclick="openSubLinkModal('${l.uuid}','${esc(l.sub_link||'')}')" title="تغییر لینک ساب"><i class="ti ti-pencil"></i></button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(l.vless_link)}')" title="QR"><i class="ti ti-qrcode"></i></button>
          <button class="btn btn-sm btn-g" onclick="resetUsage('${l.uuid}')" title="ریست مصرف"><i class="ti ti-rotate"></i></button>
          <button class="btn btn-sm btn-d" onclick="deleteLink('${l.uuid}')" title="حذف"><i class="ti ti-trash"></i></button>
        </div></td>
      </tr>`;
    }).join('');
    document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k" style="gap:5px"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'#f59e0b':l.active?'#10b981':'#ef4444'}"></i>${esc(l.label)}${l.game_mode?' 🎮':''}</span><span class="sr-v" style="font-size:10px">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');
  }catch(e){console.error(e)}
}

// ============== ساخت کانفیگ گیم ==============
async function createGameConfig(){
  const label=document.getElementById('game-label').value.trim()||'کانفیگ گیم';
  const val=document.getElementById('game-val').value;
  const unit=document.getElementById('game-unit').value;
  const port=document.getElementById('game-port').value.trim();
  try{
    const r=await authF('/api/links/game',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,game_port:port||null})
    });
    if(!r.ok)throw new Error('failed');
    closeModal('modal-game-config');
    ['game-label','game-val','game-port'].forEach(id=>document.getElementById(id).value='');
    toast('کانفیگ گیم ساخته شد 🎮✓','ok');
    loadLinks();fetchStats();
  }catch(e){toast('خطا در ساخت کانفیگ گیم','err')}
}

// ============== تغییر لینک ساب ==============
function openSubLinkModal(uuid,currentLink){
  document.getElementById('sub-link-uuid').value = uuid;
  document.getElementById('sub-link-input').value = currentLink || '';
  openModal('modal-sub-link');
}
async function saveSubLink(){
  const uuid=document.getElementById('sub-link-uuid').value;
  const newLink=document.getElementById('sub-link-input').value.trim();
  if(!uuid){toast('خطا: UUID مشخص نیست','err');return}
  try{
    const r=await authF('/api/links/'+uuid+'/sub-link',{
      method:'PATCH',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({sub_link:newLink||null})
    });
    if(!r.ok)throw new Error();
    closeModal('modal-sub-link');
    toast('لینک ساب تغییر کرد ✓','ok');
    loadLinks();
  }catch(e){toast('خطا در تغییر لینک ساب','err')}
}

// ============== سایر توابع کانفیگ ==============
async function createLink(){
  const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';
  const val=document.getElementById('nl-val').value;
  const unit=document.getElementById('nl-unit').value;
  const exp=document.getElementById('nl-exp').value;
  const note=document.getElementById('nl-note').value.trim();
  const sub_id=document.getElementById('nl-sub').value||null;
  try{
    const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,sub_id})});
    if(!r.ok)throw new Error('failed');
    ['nl-label','nl-val','nl-exp','nl-note'].forEach(id=>document.getElementById(id).value='');
    toast('کانفیگ ساخته شد ✓','ok');loadLinks();
  }catch(e){toast('خطا در ساخت','err')}
}
async function moveLinkSub(uuid,newSubId){
  try{
    const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:newSubId||null})});
    if(!r.ok)throw new Error();
    toast('گروه تغییر کرد ✓','ok');loadLinks();
  }catch(e){toast('خطا','err')}
}
async function toggleActive(uuid,newState){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'فعال شد ✓':'غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function resetUsage(uuid){
  try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('مصرف ریست شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
async function deleteLink(uuid){
  if(!confirm('حذف این کانفیگ؟'))return;
  try{const r=await authF('/api/links/'+uuid,{method:'DELETE'});if(!r.ok)throw new Error();toast('حذف شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}
}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}

// ============== گروه‌های ساب ==============
let currentSubId=null;
async function loadSubs(){
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    document.getElementById('subs-nb').textContent=subs.length;
    document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';
    const grid=document.getElementById('subs-grid');
    if(!subs.length){grid.innerHTML='<div class="empty" style="grid-column:1/-1"><i class="ti ti-folders"></i><p>هنوز گروهی وجود ندارد</p></div>';return}
    grid.innerHTML=subs.map(s=>`
      <div class="sub-card">
        <div class="sub-card-head">
          <div><div class="sub-card-name">${esc(s.name)}</div>${s.desc?`<div class="sub-card-desc">${esc(s.desc)}</div>`:''}</div>
          <div style="display:flex;gap:5px;flex-shrink:0">${s.has_password?'<span class="badge bg-amber"><i class="ti ti-lock"></i> رمز</span>':'<span class="badge bg-green"><i class="ti ti-globe"></i> پابلیک</span>'}</div>
        </div>
        <div class="sub-card-meta">
          <span class="sub-meta-item"><i class="ti ti-link"></i> ${toFa(s.links_count)} کانفیگ</span>
          <span class="sub-meta-item"><i class="ti ti-circle-check" style="color:#10b981"></i> ${toFa(s.active_count)} فعال</span>
          <span class="sub-meta-item"><i class="ti ti-database"></i> ${esc(s.total_used_fmt)} مصرف</span>
          <span class="sub-meta-item"><i class="ti ti-calendar"></i> ${new Date(s.created_at).toLocaleDateString('fa-IR')}</span>
        </div>
        <div class="pub-url-box">
          <span class="pub-url-text">${esc(s.public_url)}</span>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('لینک پابلیک کپی شد','ok'))"><i class="ti ti-copy"></i></button>
          <button class="btn btn-sm btn-pur" onclick="window.open('${esc(s.public_url)}','_blank')"><i class="ti ti-external-link"></i></button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')" title="QR کل گروه"><i class="ti ti-qrcode"></i></button>
        </div>
        <div class="sub-card-footer">
          <button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> مدیریت کانفیگ‌ها</button>
          <button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('لینک ساب کپی شد','ok'))"><i class="ti ti-rss"></i> کپی ساب</button>
          <button class="btn btn-sm btn-d" onclick="deleteSub('${esc(s.sub_id)}')"><i class="ti ti-trash"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){console.error(e)}
}
async function createSub(){
  const name=document.getElementById('ns-name').value.trim()||'گروه جدید';
  const desc=document.getElementById('ns-desc').value.trim();
  const pw=document.getElementById('ns-pw').value;
  try{
    const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw})});
    if(!r.ok)throw new Error('failed');
    ['ns-name','ns-desc','ns-pw'].forEach(id=>document.getElementById(id).value='');
    closeModal('modal-create-sub');
    toast('گروه ساخته شد ✓','ok');loadSubs();
  }catch(e){toast('خطا در ساخت گروه','err')}
}
async function deleteSub(sub_id){
  if(!confirm('حذف این گروه؟ کانفیگ‌ها حذف نمی‌شوند.'))return;
  try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}
}
async function openSubLinks(sub_id,name){
  currentSubId=sub_id;
  document.getElementById('modal-sub-name').textContent=name;
  document.getElementById('modal-links-body').innerHTML='<div style="color:var(--text2);font-size:12px;padding:10px">در حال بارگذاری...</div>';
  openModal('modal-links');
  try{
    const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);
    const {links=[]}=await lr.json();
    const {subs=[]}=await sr.json();
    const thisSub=subs.find(s=>s.sub_id===sub_id);
    const inSub=new Set(thisSub?.link_ids||[]);
    if(!links.length){document.getElementById('modal-links-body').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div>';return}
    document.getElementById('modal-links-body').innerHTML=links.map(l=>`
      <div class="lrow">
        <input type="checkbox" class="lrow-check" id="lc-${l.uuid}" ${inSub.has(l.uuid)?'checked':''} value="${l.uuid}">
        <label for="lc-${l.uuid}" class="lrow-label">${esc(l.label)}${l.game_mode?' 🎮':''}</label>
        ${l.active&&!l.expired?'<span class="lrow-badge">فعال</span>':'<span class="lrow-badge" style="background:rgba(239,68,68,0.06);color:#f87171">غیرفعال</span>'}
        <span style="font-size:9.5px;color:var(--text2)">${fmtB(l.used_bytes)}</span>
      </div>
    `).join('');
  }catch(e){toast('خطا در بارگذاری','err')}
}
async function saveSubLinks(){
  if(!currentSubId)return;
  const checks=document.querySelectorAll('#modal-links-body .lrow-check');
  const link_ids=[...checks].filter(c=>c.checked).map(c=>c.value);
  try{
    const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});
    if(!r.ok)throw new Error();
    const allChecks=[...checks].map(c=>({uuid:c.value,inSub:c.checked}));
    await Promise.all(allChecks.map(({uuid,inSub})=>
      authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:inSub?currentSubId:null})})
    ));
    closeModal('modal-links');
    toast('کانفیگ‌های گروه ذخیره شدند ✓','ok');
    loadSubs();loadLinks();
  }catch(e){toast('خطا در ذخیره','err')}
}

// ============== سابسکریپشن ==============
async function loadSubsPage(){
  document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all';
  try{
    const r=await authF('/api/subs'),d=await r.json();
    const subs=d.subs||[];
    const el=document.getElementById('sub-groups-list');
    if(!subs.length){el.innerHTML='<div class="empty"><i class="ti ti-rss-off"></i><p>هنوز گروهی ندارید</p></div>';return}
    el.innerHTML=subs.map(s=>`
      <div style="padding:14px 16px;background:rgba(124,58,237,0.02);border:1px solid var(--glass-border);border-radius:12px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap">
        <div>
          <div style="font-weight:700;font-size:13px;margin-bottom:3px">${esc(s.name)}</div>
          <div style="font-family:ui-monospace,monospace;font-size:10px;color:var(--accent3)">${esc(s.sub_url)}</div>
          <div style="font-size:10px;color:var(--text2);margin-top:3px">${toFa(s.links_count)} کانفیگ · ${esc(s.total_used_fmt)} مصرف ${s.has_password?'· 🔒 رمزدار':''}</div>
        </div>
        <div style="display:flex;gap:5px;flex-wrap:wrap">
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i> ساب</button>
          <button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i> پابلیک</button>
          <button class="btn btn-sm btn-g" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button>
        </div>
      </div>
    `).join('');
  }catch(e){}
}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ✓','ok'))}

// ============== اتصالات و خطاها ==============
async function loadConns(){
  try{const r=await authF('/stats'),d=await r.json();const cl=document.getElementById('conns-list'),ce=document.getElementById('conns-empty');if(d.active_connections===0){cl.innerHTML='';ce.style.display='block';return}ce.style.display='none';cl.innerHTML=`<div style="padding:14px;background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.06);border-radius:12px;display:flex;align-items:center;gap:12px;font-size:12px;color:#34d399"><span class="dot dg pulse"></span>${d.active_connections} اتصال فعال · کل ${d.total_traffic_mb.toFixed(1)} MB</div>`;}catch(e){}
}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){
  try{const r=await authF('/api/links'),d=await r.json();const links=d.links||[];const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];document.getElementById('vless-main').textContent=def?def.vless_link:'هنوز کانفیگی وجود ندارد';}catch(e){}
}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();toast('رفرش شد','ok')}

// ============== تغییر رمز ==============
async function changePw(){
  const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;
  if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}
  if(nw.length<4){toast('حداقل ۴ کاراکتر','err');return}
  if(nw!==cf){toast('تکرار رمز اشتباه','err');return}
  try{
    const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});
    const d=await r.json().catch(()=>({}));
    if(!r.ok)throw new Error(d.detail||'خطا');
    toast('رمز تغییر کرد ✓','ok');
    ['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');
  }catch(e){toast('✗ '+e.message,'err')}
}

// ============== نمودارها ==============
function initCharts(){
  const opts={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:'rgba(12,10,26,0.95)',borderColor:'rgba(124,58,237,0.12)',borderWidth:1,titleColor:'#f1f5f9',bodyColor:'#94a3b8',callbacks:{label:v=>`${v.parsed.y.toFixed(2)} MB`}}},scales:{x:{grid:{color:'rgba(255,255,255,0.02)'},ticks:{color:'#64748b',font:{size:9}}},y:{grid:{color:'rgba(255,255,255,0.02)'},ticks:{color:'#64748b',font:{size:9},callback:v=>v+'MB'}}}};
  const ds={label:'MB',data:[],borderColor:'rgba(124,58,237,0.8)',backgroundColor:'rgba(124,58,237,0.03)',fill:true,tension:0.4,pointRadius:3,pointHoverRadius:5,borderWidth:2};
  ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch3=new Chart(document.getElementById('ch3'),{type:'line',data:{labels:[],datasets:[{...ds}]},options:opts});
  ch2=new Chart(document.getElementById('ch2'),{type:'doughnut',data:{labels:['VLESS/WS','HTTP Proxy','سایر'],datasets:[{data:[70,25,5],backgroundColor:['rgba(124,58,237,0.8)','rgba(16,185,129,0.7)','rgba(236,72,153,0.7)'],borderColor:'rgba(0,0,0,0)',borderWidth:3,hoverOffset:8}]},options:{responsive:true,maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{color:'#94a3b8',font:{size:9},padding:10,usePointStyle:true}}}}});
}

// ============== WebSocket ==============
let ws;
function wsLog(c,m){const l=document.getElementById('ws-log'),p=document.createElement('p');const colors={ok:'#34d399',err:'#f87171',info:'#94a3b8',sent:'#fcd34d'};p.style.color=colors[c]||'#fff';p.textContent='['+new Date().toLocaleTimeString('fa-IR')+'] '+m;l.appendChild(p);l.scrollTop=l.scrollHeight}
function wsConn(){const u=document.getElementById('ws-uuid').value.trim();if(!u){toast('UUID را وارد کنید','err');return}const url=(location.protocol==='https:'?'wss':'ws')+'://'+location.host+'/ws/'+u;wsLog('info','اتصال: '+url);ws=new WebSocket(url);ws.onopen=()=>wsLog('ok','✓ متصل - UUID معتبر');ws.onerror=()=>wsLog('err','✗ خطا - UUID نامعتبر یا غیرفعال');ws.onmessage=m=>wsLog('info','دریافت '+(m.data.size||m.data.length)+' byte');ws.onclose=e=>wsLog('err','قطع ('+e.code+')'+(e.code===1008?' - دسترسی رد شد':''))}
function wsSend(){const m=document.getElementById('ws-msg').value;if(!m||!ws||ws.readyState!==1)return;ws.send(m);wsLog('sent','ارسال: '+m);document.getElementById('ws-msg').value=''}
function wsDisc(){if(ws)ws.close()}

// ============== راه‌اندازی اولیه ==============
document.addEventListener('DOMContentLoaded',async()=>{
  await checkAuth();
  initCharts();
  document.getElementById('set-host').textContent=location.host;
  document.getElementById('sub-all-url')&&(document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all');
  fetchStats();fetchDefaultVless();loadLinks();loadSubs();
  setInterval(fetchStats,4000);
  setInterval(()=>{
    if(document.getElementById('pg-links').classList.contains('on'))loadLinks();
    if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();
    if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();
  },5000);
});
</script>
</body></html>"""


def get_public_page_html(uuid_key: str) -> str:
    """صفحه پابلیک ساب — نمایش کانفیگ‌ها با QR code و آمار مصرف کاربر"""
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>B2 Sub · tg_khalili</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --glass:rgba(255,255,255,0.04);
  --glass-hover:rgba(255,255,255,0.08);
  --glass-border:rgba(255,255,255,0.05);
  --glass-border-hover:rgba(255,255,255,0.15);
  --glass-shadow:0 8px 50px rgba(0,0,0,0.5);
  --accent:#7c3aed;
  --accent2:#6d28d9;
  --accent3:#a78bfa;
  --accent-glow:rgba(124,58,237,0.25);
  --pink:#ec4899;
  --pink-glow:rgba(236,72,153,0.15);
  --green:#10b981;
  --green-glow:rgba(16,185,129,0.12);
  --red:#ef4444;
  --amber:#f59e0b;
  --text:#f1f5f9;
  --text2:#94a3b8;
  --text3:#64748b;
  --bg1:#0c0a1a;
  --bg2:#1a1435;
  --bg3:#241b4a;
  --radius:16px;
}}
html,body{{min-height:100%;background:linear-gradient(135deg,var(--bg1),var(--bg2),var(--bg3));background-attachment:fixed;font-family:'Vazirmatn',sans-serif;color:var(--text);font-size:14px}}
.bg-animation{{position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none}}
.bg-animation .orb{{position:absolute;border-radius:50%;filter:blur(130px);animation:float 20s ease-in-out infinite}}
.bg-animation .orb:nth-child(1){{width:600px;height:600px;background:rgba(124,58,237,0.08);top:-250px;right:-200px;animation-delay:0s}}
.bg-animation .orb:nth-child(2){{width:450px;height:450px;background:rgba(236,72,153,0.06);bottom:-150px;left:-150px;animation-delay:6s}}
@keyframes float{{0%,100%{{transform:translate(0,0) scale(1)}}33%{{transform:translate(40px,-50px) scale(1.1)}}66%{{transform:translate(-40px,40px) scale(0.9)}}}}
.wrap{{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:32px 16px 60px}}
.top{{display:flex;align-items:center;justify-content:space-between;margin-bottom:30px;flex-wrap:wrap;gap:12px}}
.brand{{display:flex;align-items:center;gap:14px}}
.brand-icon{{width:48px;height:48px;border-radius:14px;background:linear-gradient(135deg,var(--accent),var(--pink));display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:900;color:#fff;box-shadow:0 4px 30px var(--accent-glow);flex-shrink:0;position:relative}}
.brand-icon::after{{content:'';position:absolute;inset:-3px;border-radius:16px;background:linear-gradient(135deg,var(--accent),var(--pink));z-index:-1;filter:blur(12px);opacity:0.3}}
.brand-name{{font-size:18px;font-weight:700;color:var(--text);background:linear-gradient(135deg,#fff,#c4b5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.brand-sub{{font-size:10px;color:var(--text2);-webkit-text-fill-color:var(--text2)}}
.glass-card{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);box-shadow:var(--glass-shadow);transition:all 0.4s ease}}
.glass-card:hover{{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}}
.stats-bar{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}}
.stat-card{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--glass-shadow);transition:all 0.4s ease}}
.stat-card:hover{{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}}
.stat-label{{font-size:9.5px;color:var(--text2);font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px}}
.stat-val{{font-size:26px;font-weight:800;color:var(--text);line-height:1}}
.stat-sub{{font-size:10px;color:var(--text2);margin-top:4px}}
.sub-info{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:24px 26px;margin-bottom:20px;box-shadow:var(--glass-shadow);transition:all 0.4s ease;position:relative;overflow:hidden}}
.sub-info::before{{content:'';position:absolute;top:-30%;right:-20%;width:60%;height:60%;background:radial-gradient(circle,rgba(124,58,237,0.03),transparent 70%);pointer-events:none}}
.sub-info:hover{{border-color:var(--glass-border-hover);background:var(--glass-hover);transform:translateY(-2px)}}
.sub-name{{font-size:22px;font-weight:800;color:var(--text);margin-bottom:6px}}
.sub-desc{{font-size:12px;color:var(--text2);line-height:1.8;margin-bottom:16px}}
.sub-sub-box{{background:rgba(139,92,246,0.03);border:1px solid rgba(139,92,246,0.04);border-radius:12px;padding:14px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.sub-sub-url{{font-family:ui-monospace,monospace;font-size:10px;color:var(--accent3);word-break:break-all;flex:1}}
.cfg-title{{font-size:13px;font-weight:700;color:var(--text2);margin-bottom:16px;display:flex;align-items:center;gap:8px;text-transform:uppercase;letter-spacing:0.06em}}
.cfg-title i{{color:var(--accent);font-size:18px}}
.cfg-grid{{display:grid;gap:14px}}
.cfg-card{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:var(--radius);padding:20px 22px;transition:all 0.4s ease;position:relative;overflow:hidden;box-shadow:var(--glass-shadow)}}
.cfg-card::after{{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:linear-gradient(180deg,var(--green),#059669);opacity:0.4}}
.cfg-card.inactive::after{{background:linear-gradient(180deg,var(--red),#dc2626)}}
.cfg-card.game::after{{background:linear-gradient(180deg,#f59e0b,#d97706)}}
.cfg-card:hover{{border-color:var(--glass-border-hover);transform:translateY(-3px);background:var(--glass-hover)}}
.cfg-head{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:14px}}
.cfg-label{{font-size:15px;font-weight:700;color:var(--text)}}
.game-tag{{font-size:8px;padding:3px 10px;border-radius:6px;background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;font-weight:700;display:inline-flex;align-items:center;gap:4px;margin-right:6px;animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.5}}}}
.cfg-status{{display:flex;align-items:center;gap:5px;font-size:10px;font-weight:700;padding:4px 12px;border-radius:20px;border:1px solid transparent}}
.cfg-status.ok{{background:rgba(16,185,129,0.08);color:#34d399;border-color:rgba(16,185,129,0.06)}}
.cfg-status.no{{background:rgba(239,68,68,0.08);color:#f87171;border-color:rgba(239,68,68,0.06)}}
.cfg-usage{{margin-bottom:16px}}
.ubar{{height:6px;border-radius:6px;background:rgba(255,255,255,0.02);overflow:hidden;margin-bottom:4px}}
.ubar-f{{height:100%;border-radius:6px;transition:width 0.6s ease}}
.utxt{{font-size:10px;color:var(--text2);display:flex;justify-content:space-between}}
.cfg-vless{{background:rgba(0,0,0,0.12);border:1px solid var(--glass-border);border-radius:10px;padding:12px 16px;font-size:10px;font-family:ui-monospace,monospace;color:var(--accent3);word-break:break-all;line-height:1.7;margin-bottom:14px}}
.cfg-actions{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.btn{{font-family:inherit;font-size:11.5px;font-weight:600;border-radius:10px;padding:8px 16px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;border:none;transition:all 0.3s ease;white-space:nowrap}}
.btn i{{font-size:12px}}
.btn-p{{background:linear-gradient(135deg,var(--accent),var(--pink));color:#fff;box-shadow:0 4px 20px var(--accent-glow)}}
.btn-p:hover{{transform:translateY(-3px);box-shadow:0 8px 30px var(--accent-glow)}}
.btn-g{{background:rgba(124,58,237,0.05);color:var(--accent3);border:1px solid rgba(124,58,237,0.06)}}
.btn-g:hover{{background:rgba(124,58,237,0.1);transform:translateY(-2px)}}
.btn-pur{{background:rgba(139,92,246,0.05);color:var(--accent3);border:1px solid rgba(139,92,246,0.06)}}
.btn-pur:hover{{background:rgba(139,92,246,0.1);transform:translateY(-2px)}}
.conn-chip{{display:inline-flex;align-items:center;gap:4px;font-size:9.5px;padding:4px 12px;border-radius:20px;background:rgba(16,185,129,0.06);color:#34d399;font-weight:700}}
.dot{{width:5px;height:5px;border-radius:50%;background:var(--green);display:inline-block;animation:pulse-dot 2s infinite;box-shadow:0 0 12px var(--green-glow)}}
@keyframes pulse-dot{{0%,100%{{opacity:1}}50%{{opacity:0.3}}}}
.lock-card{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:22px;padding:44px 38px;text-align:center;max-width:400px;margin:80px auto;box-shadow:var(--glass-shadow)}}
.lock-icon{{font-size:52px;color:var(--accent);margin-bottom:16px;opacity:0.7}}
.lock-title{{font-size:20px;font-weight:700;margin-bottom:6px}}
.lock-sub{{font-size:12px;color:var(--text2);margin-bottom:24px}}
.lock-inp{{width:100%;padding:14px 18px;border-radius:12px;border:1px solid var(--glass-border);background:rgba(0,0,0,0.12);color:var(--text);font-family:inherit;font-size:13px;outline:none;margin-bottom:14px;text-align:center;letter-spacing:0.1em;transition:0.3s}}
.lock-inp:focus{{border-color:rgba(124,58,237,0.25);box-shadow:0 0 0 4px rgba(124,58,237,0.03)}}
.lock-err{{color:#f87171;font-size:11.5px;margin-bottom:14px;min-height:16px}}
.toast{{position:fixed;bottom:28px;left:50%;transform:translateX(-50%) translateY(50px);background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);color:var(--text);border-radius:14px;padding:12px 26px;font-size:12px;opacity:0;transition:all 0.4s ease;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--glass-shadow);white-space:nowrap}}
.toast.show{{opacity:1;transform:translateX(-50%) translateY(0)}}
.toast.ok{{border-color:rgba(16,185,129,0.1);background:rgba(16,185,129,0.03);color:#34d399}}
.toast.err{{border-color:rgba(239,68,68,0.1);background:rgba(239,68,68,0.03);color:#f87171}}
.qr-modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(10px)}}
.qr-modal.open{{display:flex}}
.qr-box{{background:var(--glass);backdrop-filter:blur(50px);-webkit-backdrop-filter:blur(50px);border:1px solid var(--glass-border);border-radius:20px;padding:28px;text-align:center;max-width:360px;width:calc(100% - 32px);box-shadow:var(--glass-shadow)}}
.qr-title{{font-size:16px;font-weight:700;margin-bottom:16px;color:var(--text)}}
.qr-img{{border-radius:14px;overflow:hidden;margin-bottom:16px}}
.qr-img img{{width:100%;display:block;background:#fff;padding:10px;border-radius:14px}}
.footer{{text-align:center;padding-top:32px;font-size:11px;color:var(--text2)}}
.footer a{{color:var(--accent3);font-weight:600;text-decoration:none;transition:0.3s}}
.footer a:hover{{color:var(--pink)}}
@media(max-width:500px){{.stats-bar{{grid-template-columns:1fr 1fr}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="bg-animation"><div class="orb"></div><div class="orb"></div></div>
<div class="toast" id="toast"></div>
<div class="qr-modal" id="qr-modal" onclick="this.classList.remove('open')">
  <div class="qr-box" onclick="event.stopPropagation()">
    <div class="qr-title" id="qr-label">QR Code</div>
    <div class="qr-img"><img id="qr-img" src="" alt="QR"></div>
    <button class="btn btn-g" style="width:100%;justify-content:center" onclick="document.getElementById('qr-modal').classList.remove('open')"><i class="ti ti-x"></i> بستن</button>
  </div>
</div>
<div class="wrap">
  <div class="top">
    <div class="brand">
      <div class="brand-icon">B2</div>
      <div><div class="brand-name">B2 Gateway</div><div class="brand-sub">نسخه ۹ · قدرتمند و سریع</div></div>
    </div>
    <a href="https://t.me/timazadi" target="_blank" style="display:flex;align-items:center;gap:6px;font-size:12px;color:var(--accent3);font-weight:600;transition:0.3s">
      <i class="ti ti-brand-telegram" style="font-size:16px"></i> @timazadi
    </a>
  </div>
  <div id="root">
    <div style="text-align:center;padding:80px 20px;color:var(--text2)"><i class="ti ti-loader-2" style="font-size:38px;display:block;margin-bottom:16px;animation:spin 1s linear infinite"></i>در حال بارگذاری...</div>
  </div>
  <div class="footer">
    طراحی توسط <a href="https://t.me/timazadi" target="_blank">tg_khalili</a> · B2 Gateway v9.0
  </div>
</div>
<script>
const UUID_KEY='{uuid_key}';
let savedPw='';

function toast(msg,type=''){{
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show'+(type?' '+type:'');
  setTimeout(()=>t.classList.remove('show'),2600);
}}
function esc(s){{return String(s||'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]))}}
function fmtB(b){{if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}}
function toFa(n){{return String(n).replace(/\\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}}
function showQR(label,link){{
  document.getElementById('qr-label').textContent=label;
  document.getElementById('qr-img').src='https://api.qrserver.com/v1/create-qr-code/?size=280x280&data='+encodeURIComponent(link);
  document.getElementById('qr-modal').classList.add('open');
}}
async function loadData(pw=''){{
  const url='/api/public/sub/'+UUID_KEY+(pw?'?pw='+encodeURIComponent(pw):'');
  const r=await fetch(url);
  return r.json();
}}
function renderLock(name,errMsg=''){{
  document.getElementById('root').innerHTML=`
    <div class="lock-card">
      <div class="lock-icon"><i class="ti ti-lock"></i></div>
      <div class="lock-title">${{esc(name)}}</div>
      <div class="lock-sub">این گروه رمزدار است. رمز را وارد کنید.</div>
      <div class="lock-err" id="lock-err">${{esc(errMsg)}}</div>
      <input class="lock-inp" type="password" id="lock-pw" placeholder="رمز عبور" autofocus>
      <button class="btn btn-p" style="width:100%;justify-content:center" onclick="submitLock()"><i class="ti ti-lock-open"></i> ورود</button>
    </div>
  `;
  document.getElementById('lock-pw').addEventListener('keydown',e=>{{if(e.key==='Enter')submitLock()}});
}}
async function submitLock(){{
  const pw=document.getElementById('lock-pw').value;
  const data=await loadData(pw);
  if(data.locked){{renderLock(data.name,'رمز اشتباه است');return}}
  savedPw=pw;
  renderContent(data);
}}
function renderContent(d){{
  const activeCount=d.links.filter(l=>l.active).length;
  const baseSubUrl = d.sub_url || (window.location.protocol + '//' + window.location.host + '/sub-group/' + UUID_KEY);
  const subUrl = baseSubUrl + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : '');
  window._rvgSubUrl  = subUrl;
  window._rvgSubName = d.name;
  window._rvgLinks   = d.links.map(l => ({{
    vless : l.vless_link,
    sub   : l.sub_url + (savedPw ? '?pw=' + encodeURIComponent(savedPw) : ''),
    label : l.label,
    used  : l.used_bytes,
    limit : l.limit_bytes,
    used_fmt : l.used_fmt,
    limit_fmt : l.limit_bytes===0 ? '∞' : fmtB(l.limit_bytes),
    pct  : l.limit_bytes===0 ? 0 : Math.min(100, l.used_bytes/l.limit_bytes*100),
    game : l.game_mode || false,
    sub_link : l.sub_link || '',
  }}));
  document.getElementById('root').innerHTML=`
    <div class="sub-info">
      <div class="sub-name">${{esc(d.name)}}</div>
      ${{d.desc ? `<div class="sub-desc">${{esc(d.desc)}}</div>` : ''}}
      <div style="font-size:11px;color:var(--text2);margin-bottom:14px;display:flex;align-items:center;gap:6px">
        <i class="ti ti-clock"></i> آخرین بروزرسانی: ${{new Date().toLocaleTimeString('fa-IR')}}
      </div>
      <div class="sub-sub-box">
        <span class="sub-sub-url">${{esc(subUrl)}}</span>
        <button class="btn btn-pur" style="padding:6px 12px;font-size:11px"
          onclick="navigator.clipboard.writeText(window._rvgSubUrl).then(()=>toast('لینک ساب کپی شد ✓','ok'))">
          <i class="ti ti-copy"></i> کپی لینک ساب
        </button>
        <button class="btn btn-g" style="padding:6px 12px;font-size:11px"
          onclick="showQR(window._rvgSubName + ' — کل گروه', window._rvgSubUrl)">
          <i class="ti ti-qrcode"></i> QR کل
        </button>
      </div>
    </div>
    <div class="stats-bar">
      <div class="stat-card">
        <div class="stat-label">کانفیگ‌های فعال</div>
        <div class="stat-val">${{toFa(activeCount)}}</div>
        <div class="stat-sub">از ${{toFa(d.links.length)}} کانفیگ</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">اتصالات زنده</div>
        <div class="stat-val">${{toFa(d.active_connections)}}</div>
        <div class="stat-sub" style="color:#34d399;display:flex;align-items:center;gap:5px"><span class="dot"></span> آنلاین</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">کل مصرف</div>
        <div class="stat-val" style="font-size:18px;margin-top:3px">${{esc(d.total_used_fmt)}}</div>
        <div class="stat-sub">همه کانفیگ‌ها</div>
      </div>
    </div>
    <div class="cfg-title"><i class="ti ti-link"></i> کانفیگ‌ها (${{toFa(d.links.length)}} عدد)</div>
    <div class="cfg-grid">
      ${{d.links.map((l, i) => {{
        const pct = window._rvgLinks[i].pct;
        const bc  = pct > 90 ? '#ef4444' : pct > 70 ? '#f59e0b' : '#10b981';
        const isGame = window._rvgLinks[i].game;
        const subLink = window._rvgLinks[i].sub_link;
        return `
          <div class="cfg-card${{l.active ? '' : ' inactive'}}${{isGame ? ' game' : ''}}">
            <div class="cfg-head">
              <div>
                <div class="cfg-label">
                  ${{esc(l.label)}}
                  ${{isGame ? '<span class="game-tag"><i class="ti ti-sword"></i> گیم</span>' : ''}}
                </div>
                ${{l.connections > 0 ? `<span class="conn-chip" style="margin-top:4px;display:inline-flex"><span class="dot"></span> ${{toFa(l.connections)}} اتصال</span>` : ''}}
                ${{subLink ? `<div style="margin-top:4px;font-size:9px;color:var(--accent3);font-family:ui-monospace,monospace"><i class="ti ti-link"></i> ${esc(subLink)}</div>` : ''}}
              </div>
              <span class="cfg-status ${{l.active ? 'ok' : 'no'}}">${{l.active ? '<i class="ti ti-circle-check"></i> فعال' : '<i class="ti ti-circle-x"></i> غیرفعال'}}</span>
            </div>
            <div class="cfg-usage">
              <div class="ubar"><div class="ubar-f" style="width:${{pct}}%;background:${{bc}};box-shadow:0 0 12px ${{bc}}33"></div></div>
              <div class="utxt"><span>${{esc(l.used_fmt)}} مصرف شده</span><span>سهمیه: ${{window._rvgLinks[i].limit_fmt}}</span></div>
            </div>
            <div class="cfg-vless">${{esc(l.vless_link)}}</div>
            <div class="cfg-actions">
              <button class="btn btn-p"
                onclick="navigator.clipboard.writeText(window._rvgLinks[${{i}}].vless).then(()=>toast('لینک کپی شد ✓','ok'))">
                <i class="ti ti-copy"></i> کپی لینک
              </button>
              <button class="btn btn-g"
                onclick="showQR(window._rvgLinks[${{i}}].label, window._rvgLinks[${{i}}].vless)">
                <i class="ti ti-qrcode"></i> QR
              </button>
              ${{subLink ? `
                <button class="btn btn-pur" style="padding:6px 12px;font-size:11px"
                  onclick="navigator.clipboard.writeText('${esc(subLink)}').then(()=>toast('لینک ساب کپی شد','ok'))">
                  <i class="ti ti-link"></i> کپی ساب
                </button>
              ` : ''}}
            </div>
          </div>
        `;
      }}).join('')}}
    </div>
  `;
  setTimeout(() => autoRefresh(), 30000);
}}
async function autoRefresh(){{
  try{{
    const data = await loadData(savedPw);
    if (!data.locked) renderContent(data);
  }} catch(e) {{}}
}}
async function init(){{
  try{{
    const data = await loadData();
    if (data.locked) {{ renderLock(data.name); return; }}
    renderContent(data);
  }} catch(e) {{
    document.getElementById('root').innerHTML =
      '<div style="text-align:center;padding:80px 20px;color:#f87171"><i class="ti ti-alert-circle" style="font-size:38px;display:block;margin-bottom:14px"></i>خطا در بارگذاری</div>';
  }}
}}
init();
</script>
</body></html>"""
