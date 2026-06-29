# pages.py – B2 Gateway Panel (Rocket Tunnel System)
# شامل تمام جزئیات فرانت‌اند، مدیریت قالب‌ها، چارت‌ها، جداول و صفحه ساب اختصاصی کاربر

LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ورود به سیستم مدیریت · B2</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #030712;
            --accent: #3B82F6;
            --text: #E8F4FF;
            --dim: #64748B;
            --mid: #94A3B8;
        }
        html, body { height: 100%; overflow: hidden; }
        body {
            font-family: 'Vazirmatn', sans-serif;
            background: var(--bg);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .bg {
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at 50% 30%, rgba(59, 130, 246, 0.18), transparent 60%), var(--bg);
            z-index: 0;
        }
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(120px);
            z-index: 0;
            animation: fl 10s ease-in-out infinite;
        }
        .o1 { width: 300px; height: 300px; background: rgba(59, 130, 246, 0.15); top: 10%; right: 15%; }
        .o2 { width: 250px; height: 250px; background: rgba(236,72,153, 0.08); bottom: 10%; left: 15%; animation-delay: 3s; }
        @keyframes fl { 0%, 100% { transform: translateY(0) scale(1); } 50% { transform: translateY(-20px) scale(1.05); } }
        
        .wrap { position: relative; z-index: 10; width: 100%; max-width: 390px; }
        .card {
            background: rgba(15, 23, 42, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 36px 30px 30px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255,255,255,0.1);
        }
        .brand { display: flex; align-items: center; gap: 14px; margin-bottom: 28px; }
        .brand-img {
            width: 46px;
            height: 46px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.25);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
            color: var(--accent);
            font-size: 22px;
        }
        .brand-name { font-size: 18px; font-weight: 800; color: var(--text); letter-spacing: 1px; }
        .brand-sub { font-size: 10.5px; color: var(--dim); margin-top: 1px; }
        h1 { font-size: 20px; font-weight: 700; color: var(--text); margin-bottom: 6px; }
        .sub { font-size: 12px; color: var(--mid); margin-bottom: 24px; line-height: 1.6; }
        
        .hint {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 20px;
            backdrop-filter: blur(5px);
        }
        .hint-label { font-size: 11px; color: var(--mid); flex: 1; }
        .hint-val {
            font-family: ui-monospace, monospace;
            font-size: 13.5px;
            font-weight: 700;
            color: var(--accent);
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 2px 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: .15s;
        }
        .hint-val:hover { background: rgba(59, 130, 246, 0.25); }
        
        .field { margin-bottom: 20px; }
        .field label { display: block; font-size: 11px; font-weight: 600; color: var(--mid); margin-bottom: 8px; }
        .inp-wrap { position: relative; }
        input[type=password] {
            width: 100%;
            padding: 13px 42px 13px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            background: rgba(0, 0, 0, 0.2);
            color: var(--text);
            font-family: inherit;
            font-size: 14px;
            outline: none;
            transition: .2s;
        }
        input[type=password]:focus {
            border-color: rgba(59, 130, 246, 0.4);
            background: rgba(0, 0, 0, 0.3);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
        }
        .ic { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--dim); font-size: 18px; pointer-events: none; transition: .2s; }
        input:focus + .ic { color: var(--accent); }
        
        .err {
            display: none;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 14px;
            font-size: 12px;
            color: #F87171;
            align-items: center;
            gap: 8px;
        }
        .err.show { display: flex; }
        
        .btn {
            width: 100%;
            padding: 13px;
            border-radius: 12px;
            border: none;
            cursor: pointer;
            background: linear-gradient(135deg, #3B82F6, #1D4ED8);
            color: #fff;
            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
            transition: .2s;
        }
        .btn:hover { filter: brightness(1.1); box-shadow: 0 4px 20px rgba(37, 99, 235, 0.45); }
        .btn:disabled { opacity: .5; cursor: not-allowed; }
        
        .footer {
            margin-top: 24px;
            padding-top: 18px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            color: var(--dim);
        }
        .footer-dev { display: flex; gap: 4px; color: var(--mid); }
        .footer-dev a { color: var(--accent); font-weight: 600; text-decoration: none; }
        .footer-chan a {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--mid);
            background: rgba(255, 255, 255, 0.03);
            padding: 3px 10px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-decoration: none;
        }
        .footer-chan a:hover { color: #fff; background: rgba(255, 255, 255, 0.07); }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="bg"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
    <div class="card">
        <div class="brand">
            <div class="brand-img"><i class="ti ti-rocket"></i></div>
            <div>
                <div class="brand-name">B2 PROJECT</div>
                <div class="brand-sub">موشک قدرتمند تونل زنی</div>
            </div>
        </div>
        <h1>ورود به پنل مدیریت</h1>
        <p class="sub">رمز عبور را برای دسترسی به داشبورد هوشمند B2 وارد کنید</p>
        <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
        <div class="hint">
            <span class="hint-label">رمز عبور پیش‌فرض سیستم</span>
            <span class="hint-val" onclick="document.getElementById('pw').value='123456';document.getElementById('pw').focus()">123456</span>
        </div>
        <form id="form">
            <div class="field">
                <label>رمز عبور دسکتاپ</label>
                <div class="inp-wrap">
                    <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
                    <i class="ti ti-lock ic"></i>
                </div>
            </div>
            <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود ایمن</button>
        </form>
        <div class="footer">
            <div class="footer-dev">سازنده: <a href="https://t.me/tg_khalili" target="_blank">@tg_khalili</a></div>
            <div class="footer-chan"><a href="https://t.me/timazadi" target="_blank"><i class="ti ti-brand-telegram"></i> کانال رسمی: @timazadi</a></div>
        </div>
    </div>
</div>
<script>
document.getElementById('form').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('btn'), err = document.getElementById('err'), et = document.getElementById('err-text');
    err.classList.remove('show'); btn.disabled = true;
    btn.innerHTML = '<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال پردازش...';
    try {
        const r = await fetch('/api/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ password: document.getElementById('pw').value }) });
        if (!r.ok) { const d = await r.json().catch(() => ({})); throw new Error(d.detail || 'رمز اشتباه است'); }
        location.href = '/dashboard';
    } catch (e) {
        et.textContent = e.message; err.classList.add('show');
        btn.disabled = false; btn.innerHTML = '<i class="ti ti-login-2"></i> ورود ایمن';
    }
});
</script>
</body></html>"""


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>داشبورد اصلی · سیستم هوشمند B2</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #030712; --bg2: rgba(15, 23, 42, 0.4); --bg3: rgba(30, 41, 59, 0.5);
            --card: rgba(15, 23, 42, 0.45); --card-b: rgba(255, 255, 255, 0.08); --card-bh: rgba(59, 130, 246, 0.3);
            --accent: #3B82F6; --accent2: #60A5FA; --accent-d: rgba(59, 130, 246, 0.12);
            --green: #10B981; --green-bg: rgba(16, 185, 129, 0.12); --green-t: #34D399;
            --red: #EF4444; --red-bg: rgba(239, 68, 68, 0.12); --red-t: #F87171;
            --amber: #F59E0B; --amber-bg: rgba(245, 158, 11, 0.12); --amber-t: #FCD34D;
            --t1: #E8F4FF; --t2: #94A3B8; --t3: #64748B;
            --sidebar-w: 260px; --radius: 18px;
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        }
        body { font-family: 'Vazirmatn', sans-serif; background: var(--bg); color: var(--t1); min-height: 100vh; display: flex; overflow-x: hidden; }
        .blur-bg { position: fixed; inset: 0; background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.08), transparent 50%), radial-gradient(circle at 20% 80%, rgba(139, 92, 246, 0.05), transparent 50%); z-index: -1; }
        
        /* Sidebar */
        .sidebar { width: var(--sidebar-w); min-height: 100vh; background: var(--bg2); border-left: 1px solid var(--card-b); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); display: flex; flex-direction: column; position: fixed; right: 0; top: 0; bottom: 0; z-index: 200; }
        .logo { display: flex; align-items: center; gap: 12px; padding: 24px 18px 18px; border-bottom: 1px solid var(--card-b); }
        .logo-img { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.2); color: var(--accent); font-size: 20px; }
        .logo-name { font-size: 16px; font-weight: 800; color: var(--t1); letter-spacing: 1px; }
        .logo-sub { font-size: 10px; color: var(--t3); margin-top: 1px; }
        
        .nav-wrap { flex: 1; overflow-y: auto; padding: 10px 0; }
        .nav-sec { padding: 14px 18px 6px; font-size: 10px; letter-spacing: .05em; color: var(--t3); font-weight: 700; text-transform: uppercase; }
        .nav-it { display: flex; align-items: center; gap: 10px; padding: 12px 16px; color: var(--t2); font-size: 13.5px; cursor: pointer; border-right: 3px solid transparent; transition: all .2s; margin: 2px 8px; border-radius: 8px; }
        .nav-it i { font-size: 18px; }
        .nav-it:hover { background: rgba(255, 255, 255, 0.04); color: var(--t1); }
        .nav-it.on { background: var(--accent-d); color: var(--t1); border-right-color: var(--accent); font-weight: 600; }
        
        .sb-foot { padding: 16px; border-top: 1px solid var(--card-b); display: flex; flex-direction: column; gap: 8px; }
        .tg-btn { display: flex; align-items: center; justify-content: center; gap: 6px; background: rgba(59, 130, 246, 0.15); color: var(--accent2); border-radius: 12px; padding: 10px; font-size: 12px; font-weight: 600; border: 1px solid rgba(59, 130, 246, 0.2); cursor: pointer; text-decoration: none; transition: 0.2s; }
        .tg-btn.chan { background: rgba(255, 255, 255, 0.03); color: var(--t2); border-color: var(--card-b); }
        .tg-btn:hover { filter: brightness(1.2); transform: translateY(-1px); }
        .logout-btn { display: flex; align-items: center; justify-content: center; gap: 6px; background: var(--red-bg); color: var(--red-t); border-radius: 12px; padding: 10px; font-size: 12px; border: 1px solid rgba(239, 68, 68, 0.2); cursor: pointer; font-family: inherit; font-weight: 600; transition: 0.2s; }
        .logout-btn:hover { background: rgba(239, 68, 68, 0.25); }

        /* Main Content */
        .main { margin-right: var(--sidebar-w); flex: 1; padding: 32px; min-width: 0; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; }
        .top-bar h2 { font-size: 22px; font-weight: 800; }
        
        .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .metric { background: var(--card); border: 1px solid var(--card-b); border-radius: var(--radius); padding: 20px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: var(--shadow); transition: all .2s; }
        .metric:hover { transform: translateY(-2px); border-color: var(--card-bh); }
        .m-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
        .m-icon { width: 38px; height: 38px; border-radius: 10px; background: var(--accent-d); display: flex; align-items: center; justify-content: center; color: var(--accent); font-size: 20px; }
        .m-title { font-size: 12px; color: var(--t2); font-weight: 600; }
        .m-val { font-size: 24px; font-weight: 800; color: var(--t1); letter-spacing: -0.5px; }

        .grid-2 { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 24px; }
        .card { background: var(--card); border: 1px solid var(--card-b); border-radius: var(--radius); padding: 24px; backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); box-shadow: var(--shadow); }
        .card-title { font-size: 15px; font-weight: 700; margin-bottom: 18px; display: flex; align-items: center; gap: 8px; }
        
        .tbl-wrap { overflow-x: auto; }
        .tbl { width: 100%; border-collapse: collapse; text-align: right; }
        .tbl th { font-size: 11px; color: var(--t3); padding: 12px; border-bottom: 1px solid var(--card-b); font-weight: 700; }
        .tbl td { padding: 14px 12px; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 13px; }
        
        .badge { display: inline-flex; align-items: center; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }
        .badge.active { background: var(--green-bg); color: var(--green-t); }

        @media(max-width: 1050px) {
            .sidebar { transform: translateX(100%); }
            .main { margin-right: 0; padding: 20px; }
            .metrics { grid-template-columns: repeat(2, 1fr); }
            .grid-2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
<div class="blur-bg"></div>
<aside class="sidebar">
    <div class="logo">
        <div class="logo-img"><i class="ti ti-rocket"></i></div>
        <div>
            <div class="logo-name">B2 PROJECT</div>
            <div class="logo-sub">موشک قدرتمند تونل زنی</div>
        </div>
    </div>
    <div class="nav-wrap">
        <div class="nav-sec">منو مدیریت</div>
        <div class="nav-it on"><i class="ti ti-layout-dashboard"></i> داشبورد سیستم</div>
        <div class="nav-it"><i class="ti ti-users"></i> مدیریت کاربران ساب</div>
        <div class="nav-it"><i class="ti ti-settings"></i> تنظیمات هسته B2</div>
    </div>
    <div class="sb-foot">
        <a class="tg-btn" href="https://t.me/tg_khalili" target="_blank"><i class="ti ti-user-code"></i> پشتیبانی: @tg_khalili</a>
        <a class="tg-btn chan" href="https://t.me/timazadi" target="_blank"><i class="ti ti-brand-telegram"></i> کانال ما: @timazadi</a>
        <button class="logout-btn" onclick="location.href='/'"><i class="ti ti-logout"></i> خروج از پنل</button>
    </div>
</aside>

<main class="main">
    <div class="top-bar">
        <h2>نگاه کلی به سیستم هوشمند B2</h2>
        <div id="time-box" style="font-size: 13px; color: var(--t2);">وضعیت هسته: <span class="badge active">فعال و پایدار</span></div>
    </div>

    <div class="metrics">
        <div class="metric">
            <div class="m-head"><span class="m-title">کاربران فعال آنلاین</span><div class="m-icon"><i class="ti ti-users-group"></i></div></div>
            <div class="m-val" id="m-online">۴۲ / ۱5۰</div>
        </div>
        <div class="metric">
            <div class="m-head"><span class="m-title">ترافیک مصرفی کل امروز</span><div class="m-icon" style="color:var(--accent)"><i class="ti ti-chart-arrows"></i></div></div>
            <div class="m-val">۱۴۸.۵ GB</div>
        </div>
        <div class="metric">
            <div class="m-head"><span class="m-title">لود پردازنده (CPU)</span><div class="m-icon" style="color:var(--amber)"><i class="ti ti-cpu"></i></div></div>
            <div class="m-val">۲۴٪</div>
        </div>
        <div class="metric">
            <div class="m-head"><span class="m-title">تعداد کل کانکشن‌ها</span><div class="m-icon" style="color:var(--green)"><i class="ti ti-link"></i></div></div>
            <div class="m-val">۱,۴۰۲</div>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="card-title"><i class="ti ti-chart-line" style="color:var(--accent)"></i> نمودار زنده ترافیک عبوری موشک B2</div>
            <div style="position: relative; height:220px; width:100%">
                <canvas id="trafficChart"></canvas>
            </div>
        </div>
        <div class="card">
            <div class="card-title"><i class="ti ti-device-sd-card"></i> وضعیت رم و هارد سرور</div>
            <div style="display:flex; flex-direction:column; gap:14px; margin-top:20px;">
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;"><span>مصرف حافظه RAM</span><span>۳.۲ GB از ۸ GB</span></div>
                    <div style="width:100%; height:6px; background:rgba(255,255,255,0.05); border-radius:5px; overflow:hidden;"><div style="width:40%; height:100%; background:var(--accent)"></div></div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:5px;"><span>فضای دیسک (Storage)</span><span>۱۸ GB از ۵۰ GB</span></div>
                    <div style="width:100%; height:6px; background:rgba(255,255,255,0.05); border-radius:5px; overflow:hidden;"><div style="width:36%; height:100%; background:var(--green)"></div></div>
                </div>
            </div>
        </div>
    </div>

    <div class="card">
        <div class="card-title"><i class="ti ti-list-details"></i> لیست سابسکریپشن‌های فعال اخیر و مانیتورینگ ترافیک</div>
        <div class="tbl-wrap">
            <table class="tbl">
                <thead>
                    <tr><th>نام کاربر / توکن</th><th>وضعیت اکانت</th><th>حجم مصرف شده</th><th>کل حجم اختصاصی</th><th>تاریخ انقضا</th></tr>
                </thead>
                <tbody>
                    <tr><td>User_Token_01</td><td><span class="badge active">فعال</span></td><td>22.5 GB</td><td>50 GB</td><td>۱۴ روز دیگر</td></tr>
                    <tr><td>User_Token_02</td><td><span class="badge active">فعال</span></td><td>12.1 GB</td><td>80 GB</td><td>۲۹ روز دیگر</td></tr>
                    <tr><td>User_Token_03</td><td><span class="badge active">فعال</span></td><td>44.9 GB</td><td>45 GB</td><td>۲ روز دیگر</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</main>

<script>
const ctx = document.getElementById('trafficChart').getContext('2d');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30'],
        datasets: [{
            label: 'ترافیک ورودی (Inbound)',
            data: [65, 78, 72, 95, 120, 142],
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59, 130, 246, 0.05)',
            fill: true,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { grid: { display: false } }, y: { grid: { color: 'rgba(255,255,255,0.03)' } } }
    }
});
</script>
</body></html>"""


# صفحه جدید: این قالب اختصاصی برای کاربر طراحی شده تا حجم مصرفی و آدرس لینک ساب خود را مانیتور کند
USER_SUB_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>پروفایل و وضعیت ترافیک اشتراک · B2</title>
    <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #020617;
            --card: rgba(30, 41, 59, 0.45);
            --primary: #3B82F6;
            --text: #F8FAFC;
            --subtext: #94A3B8;
        }
        body {
            font-family: 'Vazirmatn', sans-serif;
            background: var(--bg);
            color: var(--text);
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
        }
        .bg-glow {
            position: fixed;
            top: -10%;
            left: -10%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(59, 130, 246, 0.14) 0%, transparent 70%);
            z-index: 0;
        }
        .container {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 430px;
            background: var(--card);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 28px;
            padding: 32px 28px;
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.5);
        }
        .header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 26px; }
        .title-box h1 { font-size: 19px; font-weight: 800; margin-bottom: 4px; letter-spacing: 0.5px; }
        .title-box p { font-size: 12px; color: var(--subtext); }
        .status-badge {
            background: rgba(16, 185, 129, 0.12);
            color: #10B981;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
            border: 1px solid rgba(16, 185, 129, 0.25);
        }

        /* Progress Area */
        .usage-container {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 24px;
        }
        .usage-details { display: flex; justify-content: space-between; font-size: 13.5px; margin-bottom: 12px; }
        .usage-details span:nth-child(2) { font-weight: 700; color: var(--primary); }
        .bar-bg { width: 100%; height: 10px; background: rgba(255, 255, 255, 0.08); border-radius: 10px; overflow: hidden; }
        .bar-fill { height: 100%; background: linear-gradient(90deg, #3B82F6, #60A5FA); border-radius: 10px; width: 45%; transition: width 1.2s ease-in-out; }
        
        /* Information Cards Grid */
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 24px; }
        .stat-item { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 16px; border-radius: 18px; text-align: center; transition: 0.2s; }
        .stat-item:hover { border-color: rgba(59, 130, 246, 0.2); background: rgba(255, 255, 255, 0.04); }
        .stat-item i { font-size: 24px; color: var(--subtext); margin-bottom: 8px; display: block; }
        .stat-val { font-size: 18px; font-weight: 800; margin-bottom: 2px; }
        .stat-lbl { font-size: 11px; color: var(--subtext); font-weight: 500; }

        /* Subscription URL Box */
        .sub-url-header { font-size: 12px; color: var(--subtext); font-weight: 600; margin-bottom: 8px; padding-right: 4px; }
        .url-wrapper { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 16px; display: flex; align-items: center; gap: 8px; }
        .url-wrapper input { flex: 1; background: transparent; border: none; color: var(--text); font-family: ui-monospace, monospace; font-size: 12.5px; outline: none; padding: 0 8px; direction: ltr; text-align: left; }
        .btn-copy { background: var(--primary); color: #fff; border: none; padding: 10px 16px; border-radius: 12px; cursor: pointer; font-family: inherit; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 6px; transition: 0.2s; }
        .btn-copy:hover { background: #2563EB; }

        .footer { text-align: center; margin-top: 28px; font-size: 11px; color: var(--subtext); line-height: 1.7; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 16px; }
        .footer a { color: var(--primary); text-decoration: none; font-weight: 700; }
    </style>
</head>
<body>
<div class="bg-glow"></div>
<div class="container">
    <div class="header">
        <div class="title-box">
            <h1>وضعیت سرویس تونل B2</h1>
            <p>مشخصات و مانیتورینگ حجم مصرفی</p>
        </div>
        <div class="status-badge"><i class="ti ti-circle-check-filled"></i> اتصال فعال</div>
    </div>

    <div class="usage-container">
        <div class="usage-details">
            <span>میزان ترافیک استفاده شده</span>
            <span>22.5 GB / 50 GB</span>
        </div>
        <div class="bar-bg">
            <div class="bar-fill" style="width: 45%;"></div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-item">
            <i class="ti ti-cloud-download"></i>
            <div class="stat-val">۲۲.۵ <span style="font-size:12px; font-weight:400">GB</span></div>
            <div class="stat-lbl">کل حجم مصرف شده</div>
        </div>
        <div class="stat-item">
            <i class="ti ti-calendar-time"></i>
            <div class="stat-val">۱۴ <span style="font-size:12px; font-weight:400">روز</span></div>
            <div class="stat-lbl">زمان باقیمانده اشتراک</div>
        </div>
    </div>

    <div class="sub-url-header">آدرس اختصاصی سابسکریپشن (Subscription URL)</div>
    <div class="url-wrapper">
        <input type="text" id="subUrl" value="https://sub.b2-gateway.com/v1/sub/token_example_123" readonly>
        <button class="btn-copy" onclick="copySubscriptionUrl()"><i class="ti ti-copy"></i> کپی لینک</button>
    </div>

    <div class="footer">
        توسعه‌دهنده سیستم: <a href="https://t.me/tg_khalili" target="_blank">@tg_khalili</a><br>
        کانال اطلاع‌رسانی و پشتیبانی رسمی: <a href="https://t.me/timazadi" target="_blank">@timazadi</a>
    </div>
</div>

<script>
function copySubscriptionUrl() {
    const inputElement = document.getElementById("subUrl");
    inputElement.select();
    inputElement.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(inputElement.value);
    
    const copyBtn = document.querySelector('.btn-copy');
    const originalText = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="ti ti-check"></i> انجام شد';
    copyBtn.style.background = '#10B981';
    
    setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.style.background = 'var(--primary)';
    }, 1800);
}
</script>
</body></html>"""
