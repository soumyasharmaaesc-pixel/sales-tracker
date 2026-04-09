#!/usr/bin/env python3
"""Build manager.html, rep.html, and index.html from app.js + templates."""

import os

V2 = "/sessions/lucid-vibrant-ramanujan/sales-dashboard/v2"
OUT = "/sessions/lucid-vibrant-ramanujan/sales-dashboard/vercel-deploy"
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(V2, "app.js"), "r") as f:
    app_code = f.read()

# Common head + CDN scripts for the dashboard HTMLs
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; -webkit-font-smoothing: antialiased; background: #F9FAFB; }
    #root { width: 100%; }
  </style>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/prop-types/15.8.1/prop-types.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/recharts/2.12.7/Recharts.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.6.0/mammoth.browser.min.js"></script>
  <script crossorigin src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.9/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>
  <script>window._ROLE = "__ROLE__";</script>
  <script type="text/babel">
__APP_CODE__
  </script>
</body>
</html>
"""

def build(role, title, filename):
    html = HEAD.replace("{title}", title).replace("__ROLE__", role).replace("__APP_CODE__", app_code)
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    size = os.path.getsize(os.path.join(OUT, filename))
    print(f"Wrote {filename}: {size} bytes")

build("manager", "TheHireHub.AI - Manager Dashboard", "manager.html")
build("rep", "TheHireHub.AI - Rep Dashboard", "rep.html")

# Build index.html — the role picker landing page
INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TheHireHub.AI - Sales Tracker</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      -webkit-font-smoothing: antialiased;
      background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      color: #F9FAFB;
    }
    .wrap { max-width: 920px; width: 100%; text-align: center; }
    .brand {
      font-size: 13px; font-weight: 700; letter-spacing: 0.2em;
      color: #818CF8; margin-bottom: 14px;
    }
    h1 {
      font-size: 44px; font-weight: 800; line-height: 1.1;
      margin-bottom: 16px; color: #F9FAFB;
      background: linear-gradient(135deg, #F9FAFB 0%, #C7D2FE 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .sub {
      font-size: 17px; color: #94A3B8; max-width: 560px;
      margin: 0 auto 48px; line-height: 1.55;
    }
    .cards {
      display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
      margin-bottom: 32px;
    }
    @media (max-width: 680px) { .cards { grid-template-columns: 1fr; } }
    .card {
      background: rgba(255,255,255,0.04);
      border: 1.5px solid rgba(255,255,255,0.1);
      border-radius: 20px; padding: 36px 28px 32px;
      text-decoration: none; color: inherit;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      text-align: left; position: relative; overflow: hidden;
      backdrop-filter: blur(10px);
    }
    .card::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
      transition: height 0.25s;
    }
    .card.manager::before { background: linear-gradient(90deg, #4F46E5, #818CF8); }
    .card.rep::before { background: linear-gradient(90deg, #14B8A6, #5EEAD4); }
    .card:hover {
      background: rgba(255,255,255,0.07);
      border-color: rgba(255,255,255,0.2);
      transform: translateY(-4px);
      box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    .card:hover::before { height: 5px; }
    .icon {
      width: 56px; height: 56px; border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; font-weight: 700; margin-bottom: 22px;
    }
    .card.manager .icon { background: rgba(79, 70, 229, 0.2); color: #A5B4FC; border: 1px solid rgba(129, 140, 248, 0.3); }
    .card.rep .icon { background: rgba(20, 184, 166, 0.2); color: #5EEAD4; border: 1px solid rgba(94, 234, 212, 0.3); }
    .card h2 { font-size: 22px; font-weight: 700; margin-bottom: 10px; color: #F9FAFB; }
    .card p { font-size: 14px; color: #94A3B8; line-height: 1.55; margin-bottom: 20px; min-height: 44px; }
    .bullets { list-style: none; padding: 0; margin: 0 0 24px; }
    .bullets li {
      font-size: 13px; color: #CBD5E1; padding: 6px 0;
      display: flex; align-items: flex-start; gap: 8px;
    }
    .bullets li::before {
      content: '→'; color: #6366F1; font-weight: 700; margin-top: 0px;
    }
    .card.rep .bullets li::before { color: #14B8A6; }
    .cta {
      display: inline-flex; align-items: center; gap: 8px;
      font-size: 14px; font-weight: 700; letter-spacing: 0.02em;
    }
    .card.manager .cta { color: #A5B4FC; }
    .card.rep .cta { color: #5EEAD4; }
    .footer {
      font-size: 12px; color: #64748B;
      margin-top: 24px; letter-spacing: 0.04em;
    }
    .footer a { color: #818CF8; text-decoration: none; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="brand">THEHIREHUB.AI · SALES MANAGEMENT</div>
    <h1>Sales Tracker Command Center</h1>
    <p class="sub">Dual-role sales monitoring dashboard for TheHireHub.AI — track pipeline, weekly reports, onboarding and targets across Manager and Rep views.</p>

    <div class="cards">
      <a href="manager.html" class="card manager">
        <div class="icon">M</div>
        <h2>Manager Dashboard</h2>
        <p>Full command center with CRUD access, private notes, and complete visibility into rep performance.</p>
        <ul class="bullets">
          <li>Create, edit, and track all deals</li>
          <li>Send messages and targets to the rep</li>
          <li>Review weekly reports and onboarding</li>
          <li>GTM benchmarks · Scenarios · Enterprise overlay</li>
          <li>Private notes (only you can see)</li>
        </ul>
        <div class="cta">Open Manager View →</div>
      </a>

      <a href="rep.html" class="card rep">
        <div class="icon">R</div>
        <h2>Rep Dashboard</h2>
        <p>Focused daily workspace for the Sales Rep — your pipeline, weekly reports, onboarding checklist and messages.</p>
        <ul class="bullets">
          <li>View assigned pipeline and deals</li>
          <li>Submit weekly activity reports</li>
          <li>Check off onboarding tasks</li>
          <li>Read messages and targets from management</li>
          <li>Track your progress against stretch targets</li>
        </ul>
        <div class="cta">Open Rep View →</div>
      </a>
    </div>

    <div class="footer">
      Both views share live data via localStorage — updates in one view instantly appear in the other.
    </div>
  </div>
</body>
</html>
"""
with open(os.path.join(OUT, "index.html"), "w") as f:
    f.write(INDEX_HTML)
print(f"Wrote index.html: {os.path.getsize(os.path.join(OUT, 'index.html'))} bytes")
