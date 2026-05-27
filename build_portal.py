"""Builder for Savon Nexo Employee Portal HTML — Version 0.1"""
import json
from pathlib import Path

HERE = Path(__file__).parent

# Load tasting data
with open(HERE / 'tastings_data_compact.json', 'r') as f:
    TASTING_DATA = f.read()

# Load logo as base64 data URL
with open(HERE / 'logo_b64.txt', 'r') as f:
    LOGO_B64 = f.read().strip()
LOGO_DATA_URL = f'data:image/png;base64,{LOGO_B64}'

# ------------------ CSS ------------------
CSS = r"""
/* ============ SAVON NEXO THEME — v0.1 ============ */
:root {
  --brand-red: #E11D2A;
  --brand-red-hover: #C8161F;
  --brand-red-dark: #8B1A1F;
  --brand-red-soft: #FDE8EA;
  --brand-red-pale: #FFF5F6;

  --ink: #0E0F11;
  --ink-soft: #2A2B30;
  --slate: #5C5F66;
  --warm-gray: #8E9197;
  --border: #ECEEF1;
  --border-strong: #DDE0E5;

  --bg: #FFFFFF;
  --bg-light: #FAFAFB;
  --bg-soft: #F4F6F9;

  --success: #1E9A4F;
  --success-light: #E5F6EC;
  --danger: #DC2A37;
  --danger-light: #FDE9EB;
  --warning: #D4882F;
  --warning-light: #FFF3DE;
  --info: #2F6BC9;
  --info-light: #E4EEF9;

  --shadow-sm: 0 1px 2px rgba(14, 15, 17, 0.04);
  --shadow: 0 4px 16px rgba(14, 15, 17, 0.06);
  --shadow-md: 0 8px 28px rgba(14, 15, 17, 0.08);
  --shadow-lg: 0 16px 48px rgba(14, 15, 17, 0.12);

  --radius: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-pill: 999px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; }

body {
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
}

button { font-family: inherit; cursor: pointer; }
a { color: var(--brand-red); text-decoration: none; transition: color 0.15s; }
a:hover { color: var(--brand-red-hover); }

/* ============ LOGIN ============ */
.login-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFFFFF 0%, #FFF5F6 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}
.login-screen::before {
  content: '';
  position: absolute;
  top: -30%; right: -10%;
  width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(225, 29, 42, 0.08) 0%, transparent 60%);
  border-radius: 50%;
}
.login-screen::after {
  content: '';
  position: absolute;
  bottom: -30%; left: -10%;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(225, 29, 42, 0.04) 0%, transparent 60%);
  border-radius: 50%;
}
.login-card {
  background: white;
  border-radius: var(--radius-xl);
  width: 100%; max-width: 460px;
  padding: 44px 40px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  position: relative;
  z-index: 2;
}
.login-brand { text-align: center; margin-bottom: 32px; }
.login-brand .logo, .login-brand .logo-wide {
  width: 100%;
  max-width: 280px;
  margin: 0 auto 18px;
  display: flex; align-items: center; justify-content: center;
}
.login-brand .logo-wide img,
.brand-logo-img { width: 100%; height: auto; display: block; max-width: 100%; }
.login-brand .tagline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--brand-red-soft);
  color: var(--brand-red-dark);
  padding: 6px 14px;
  border-radius: var(--radius-pill);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  margin-top: 8px;
}
.login-brand .tagline::before {
  content: '';
  width: 6px; height: 6px;
  background: var(--brand-red);
  border-radius: 50%;
}

.login-card form { display: flex; flex-direction: column; gap: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--slate);
}

input, select, textarea {
  padding: 12px 14px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  font-family: inherit;
  font-size: 14px;
  background: white;
  color: var(--ink);
  transition: border-color 0.15s, box-shadow 0.15s;
  width: 100%;
}
input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--brand-red);
  box-shadow: 0 0 0 4px rgba(225, 29, 42, 0.12);
}
textarea { resize: vertical; min-height: 80px; }

.login-error {
  background: var(--danger-light);
  color: var(--danger);
  padding: 10px 14px;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 600;
  display: none;
}
.login-error.active { display: block; }

.demo-creds {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--slate);
}
.demo-creds .title {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 10px;
  font-size: 10px;
  color: var(--warm-gray);
  text-align: center;
}
.demo-creds .cred {
  cursor: pointer;
  padding: 8px 12px;
  border-radius: var(--radius);
  margin-bottom: 4px;
  transition: background 0.15s, border-color 0.15s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid transparent;
}
.demo-creds .cred:hover { background: var(--bg-light); border-color: var(--border); }
.demo-creds .cred .role {
  background: var(--brand-red-soft);
  color: var(--brand-red);
  padding: 2px 10px;
  border-radius: var(--radius-pill);
  font-size: 10px;
  font-weight: 700;
}

.login-version {
  margin-top: 22px;
  padding-top: 18px;
  border-top: 1px dashed var(--border);
  text-align: center;
  font-size: 11px;
  color: var(--warm-gray);
  letter-spacing: 0.3px;
}
.login-version strong { color: var(--brand-red); }

/* ============ BUTTONS ============ */
.btn {
  padding: 11px 22px;
  border: none;
  border-radius: var(--radius-pill);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.3px;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  white-space: nowrap;
  font-family: inherit;
}
.btn-primary {
  background: var(--brand-red);
  color: white;
  box-shadow: 0 4px 14px rgba(225, 29, 42, 0.25);
}
.btn-primary:hover {
  background: var(--brand-red-hover);
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(225, 29, 42, 0.32);
}
.btn-gold, .btn-success {
  background: var(--ink);
  color: white;
}
.btn-gold:hover, .btn-success:hover { background: #000; transform: translateY(-1px); }
.btn-outline {
  background: white;
  color: var(--ink);
  border: 1.5px solid var(--border-strong);
}
.btn-outline:hover {
  border-color: var(--brand-red);
  color: var(--brand-red);
}
.btn-secondary {
  background: white;
  color: var(--ink);
  border: 1.5px solid var(--border);
}
.btn-secondary:hover { background: var(--bg-light); border-color: var(--border-strong); }
.btn-ghost {
  background: transparent;
  color: var(--slate);
  border: 1px solid transparent;
  padding: 6px 12px;
  font-size: 12px;
}
.btn-ghost:hover { background: var(--bg-light); color: var(--ink); }
.btn-danger {
  background: transparent;
  color: var(--danger);
  border: 1.5px solid var(--danger);
}
.btn-danger:hover { background: var(--danger); color: white; }
.btn-sm { padding: 7px 14px; font-size: 12px; }
.btn-lg { padding: 14px 28px; font-size: 15px; }
.btn-block { width: 100%; }

/* ============ APP SHELL ============ */
.app {
  display: grid;
  grid-template-columns: 260px 1fr;
  min-height: 100vh;
  background: var(--bg-light);
}
.sidebar {
  background: white;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-brand {
  padding: 22px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--border);
}
.sidebar-brand .logo, .sidebar-brand .logo-wide-sidebar {
  width: 100%;
  display: flex; align-items: center; justify-content: center;
}
.sidebar-brand .logo-wide-sidebar img { width: 100%; height: auto; display: block; }

.nav-section { padding: 16px 12px 4px; }
.nav-section-title {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--warm-gray);
  padding: 0 12px 10px;
  font-weight: 700;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius);
  color: var(--slate);
  cursor: pointer;
  transition: all 0.15s;
  font-size: 14px;
  margin-bottom: 2px;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
  font-weight: 600;
  font-family: inherit;
  position: relative;
}
.nav-item:hover { background: var(--bg-light); color: var(--ink); }
.nav-item.active {
  background: var(--brand-red-soft);
  color: var(--brand-red);
  font-weight: 700;
}
.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0; top: 8px; bottom: 8px;
  width: 3px;
  background: var(--brand-red);
  border-radius: 0 3px 3px 0;
}
.nav-icon { width: 18px; text-align: center; font-size: 15px; opacity: 0.85; }

.sidebar-footer {
  margin-top: auto;
  padding: 14px 12px;
  border-top: 1px solid var(--border);
}
.user-card {
  background: var(--bg-light);
  border-radius: var(--radius);
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--border);
}
.avatar {
  width: 38px; height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand-red) 0%, var(--brand-red-dark) 100%);
  color: white;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}
.user-card .name { font-size: 13px; font-weight: 700; line-height: 1.2; color: var(--ink); }
.user-card .position { font-size: 11px; color: var(--slate); margin-top: 2px; }
.user-card .info { flex: 1; min-width: 0; overflow: hidden; }
.user-card .name, .user-card .position { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.logout-btn {
  background: transparent;
  border: none;
  color: var(--warm-gray);
  padding: 6px;
  border-radius: 6px;
  font-size: 16px;
  transition: all 0.15s;
}
.logout-btn:hover { background: var(--brand-red-soft); color: var(--brand-red); }

.content {
  padding: 28px 36px 60px;
  overflow-x: hidden;
  background: var(--bg-light);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  gap: 20px;
  flex-wrap: wrap;
}
.page-title {
  font-size: 28px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1.15;
  letter-spacing: -0.5px;
}
.page-subtitle {
  color: var(--slate);
  margin-top: 6px;
  font-size: 14px;
}
.page-actions { display: flex; gap: 10px; flex-wrap: wrap; }

/* ============ CARDS ============ */
.card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
  box-shadow: var(--shadow-sm);
}
.card-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 4px;
  letter-spacing: -0.2px;
}
.card-subtitle {
  color: var(--slate);
  font-size: 13px;
  margin-bottom: 16px;
}

.grid { display: grid; gap: 20px; }
.grid-2 { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }
.grid-3 { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
.grid-4 { grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); }

.stat-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 22px;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
  transition: transform 0.15s, box-shadow 0.15s;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 22px; left: 22px;
  width: 8px; height: 8px;
  background: var(--brand-red);
  border-radius: 50%;
}
.stat-label {
  text-transform: uppercase;
  letter-spacing: 1.2px;
  font-size: 10px;
  color: var(--slate);
  font-weight: 700;
  margin-bottom: 10px;
  padding-left: 18px;
}
.stat-number {
  font-size: 36px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1;
  letter-spacing: -1px;
}
.stat-sub {
  margin-top: 6px;
  font-size: 12px;
  color: var(--slate);
}

.tag-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--brand-red-soft);
  color: var(--brand-red-dark);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.tag-label::before {
  content: '';
  width: 5px; height: 5px;
  background: var(--brand-red);
  border-radius: 50%;
}

/* ============ CLOCK ============ */
.clock-hero {
  background: linear-gradient(135deg, var(--ink) 0%, #2A2B30 100%);
  color: white;
  border-radius: var(--radius-xl);
  padding: 36px;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}
.clock-hero::before {
  content: '';
  position: absolute;
  top: -50%; right: -10%;
  width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(225, 29, 42, 0.25) 0%, transparent 65%);
  border-radius: 50%;
}
.clock-time {
  font-size: 64px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -2px;
  position: relative;
  z-index: 2;
}
.clock-date {
  color: rgba(255,255,255,0.7);
  margin-top: 10px;
  font-size: 15px;
  position: relative;
  z-index: 2;
}
.clock-status {
  margin: 22px 0;
  font-size: 12px;
  color: rgba(255,255,255,0.6);
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
  position: relative;
  z-index: 2;
}
.clock-status .dot {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--warm-gray);
  margin-right: 8px;
  vertical-align: middle;
}
.clock-status.active .dot {
  background: var(--success);
  box-shadow: 0 0 0 0 var(--success);
  animation: pulse 1.8s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(30, 154, 79, 0.7); }
  70% { box-shadow: 0 0 0 14px rgba(30, 154, 79, 0); }
  100% { box-shadow: 0 0 0 0 rgba(30, 154, 79, 0); }
}
.clock-btn {
  padding: 18px 44px;
  font-size: 15px;
  border: none;
  border-radius: var(--radius-pill);
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  z-index: 2;
  font-family: inherit;
}
.clock-btn.start {
  background: var(--brand-red);
  color: white;
  box-shadow: 0 8px 24px rgba(225, 29, 42, 0.4);
}
.clock-btn.start:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 28px rgba(225, 29, 42, 0.5);
}
.clock-btn.stop {
  background: white;
  color: var(--ink);
}
.clock-btn.stop:hover { transform: translateY(-2px); }
.clock-elapsed {
  font-size: 28px;
  color: var(--brand-red);
  font-weight: 800;
  margin: 18px 0 4px;
  position: relative;
  z-index: 2;
}

/* ============ TABLES ============ */
.table-wrap {
  background: white;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}
.table-header {
  padding: 16px 22px;
  background: var(--ink);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.table-title { font-size: 16px; font-weight: 700; }
.table-meta { color: rgba(255,255,255,0.7); font-size: 12px; }
.table-scroll { overflow-x: auto; max-height: 70vh; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
thead { background: var(--bg-light); position: sticky; top: 0; z-index: 5; }
th {
  text-align: left;
  padding: 12px 16px;
  font-size: 11px;
  font-weight: 700;
  color: var(--slate);
  text-transform: uppercase;
  letter-spacing: 1px;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}
td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
tbody tr:hover { background: var(--brand-red-pale); }

.badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.badge-gold, .badge-red { background: var(--brand-red); color: white; }
.badge-success { background: var(--success-light); color: var(--success); }
.badge-danger { background: var(--danger-light); color: var(--danger); }
.badge-warning { background: var(--warning-light); color: var(--warning); }
.badge-info { background: var(--info-light); color: var(--info); }
.badge-muted { background: var(--bg-soft); color: var(--slate); }

/* ============ MODAL ============ */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(14, 15, 17, 0.55);
  backdrop-filter: blur(8px);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}
.modal-overlay.active { display: flex; }
.modal {
  background: white;
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 580px;
  max-height: 92vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  animation: slideUp 0.25s ease-out;
}
.modal.modal-lg { max-width: 760px; }
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.modal-header {
  padding: 22px 26px;
  background: var(--ink);
  color: white;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-title { font-size: 18px; font-weight: 700; }
.modal-close {
  background: none; border: none; color: white;
  font-size: 22px; width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.modal-close:hover { background: rgba(255,255,255,0.15); }
.modal-body { padding: 24px 26px; }
.modal-footer {
  padding: 16px 26px 22px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.form-grid .full { grid-column: span 2; }

/* ============ ANNOUNCEMENTS ============ */
.announcement {
  background: white;
  border: 1px solid var(--border);
  border-left: 4px solid var(--brand-red);
  padding: 18px 22px;
  border-radius: 0 var(--radius) var(--radius) 0;
  margin-bottom: 12px;
  box-shadow: var(--shadow-sm);
}
.announcement.pinned {
  border-left-color: var(--ink);
  background: linear-gradient(90deg, var(--brand-red-pale) 0%, white 100%);
}
.announcement-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.announcement-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--ink);
}
.announcement-date { font-size: 12px; color: var(--warm-gray); }
.announcement-body { color: var(--ink-soft); line-height: 1.6; white-space: pre-wrap; }
.announcement-author { margin-top: 10px; font-size: 12px; color: var(--slate); }
.pin-marker { color: var(--brand-red); margin-right: 6px; }

/* ============ CALENDAR ============ */
.cal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 12px;
  flex-wrap: wrap;
}
.cal-nav { display: flex; gap: 8px; align-items: center; }
.cal-month {
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
}
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 6px;
  background: white;
  padding: 18px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
.cal-day-name {
  text-align: center;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--slate);
  padding: 8px 0;
}
.cal-day {
  background: var(--bg-light);
  border-radius: var(--radius);
  min-height: 100px;
  padding: 8px;
  border: 1px solid transparent;
  transition: all 0.15s;
}
.cal-day:hover { border-color: var(--brand-red); background: var(--brand-red-pale); }
.cal-day.today {
  background: var(--brand-red-soft);
  border: 1.5px solid var(--brand-red);
}
.cal-day.other-month { opacity: 0.4; }
.cal-day-num {
  font-weight: 700;
  font-size: 13px;
  color: var(--ink);
  margin-bottom: 4px;
}
.cal-event {
  padding: 3px 7px;
  border-radius: 5px;
  font-size: 10px;
  font-weight: 600;
  margin-bottom: 3px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}
.cal-event.shift { background: var(--ink); color: white; }
.cal-event.timeoff { background: var(--info); color: white; }
.cal-event.tasting { background: var(--brand-red); color: white; }

/* ============ EMPTY / TOAST ============ */
.empty {
  text-align: center;
  padding: 50px 20px;
  color: var(--warm-gray);
}
.empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.55; }

.toast {
  position: fixed;
  bottom: 30px; right: 30px;
  background: var(--ink);
  color: white;
  padding: 14px 22px;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  z-index: 300;
  transform: translateY(140%);
  transition: transform 0.3s ease-out;
  font-weight: 600;
  font-size: 14px;
}
.toast.show { transform: translateY(0); }
.toast.success { background: var(--success); }
.toast.error { background: var(--danger); }

/* ============ TASTING PILL ============ */
.product-pill {
  display: inline-block;
  background: var(--brand-red-pale);
  color: var(--brand-red-dark);
  padding: 2px 9px;
  margin: 2px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--brand-red-soft);
  font-size: 11px;
  font-weight: 600;
}

/* ============ TABS ============ */
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 20px;
}
.tab {
  background: transparent;
  border: none;
  padding: 12px 18px;
  font-size: 13px;
  font-weight: 600;
  color: var(--slate);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  font-family: inherit;
}
.tab:hover { color: var(--ink); }
.tab.active { color: var(--brand-red); border-bottom-color: var(--brand-red); }

/* ============ MOBILE ============ */
.mobile-toggle {
  display: none;
  background: var(--brand-red);
  color: white;
  border: none;
  padding: 10px;
  border-radius: 8px;
  font-size: 18px;
}
.mobile-overlay {
  display: none;
  position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 40;
}
.mobile-overlay.active { display: block; }
@media (max-width: 900px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { position: fixed; left: -280px; top: 0; width: 260px; z-index: 50; transition: left 0.25s; height: 100vh; }
  .sidebar.open { left: 0; }
  .mobile-toggle { display: inline-flex; }
  .content { padding: 18px 16px 60px; }
  .page-title { font-size: 24px; }
  .clock-time { font-size: 48px; }
  .form-grid { grid-template-columns: 1fr; }
  .form-grid .full { grid-column: span 1; }
}

/* ============ ZOHO BANNER ============ */
.zoho-banner {
  background: linear-gradient(135deg, var(--brand-red) 0%, var(--brand-red-dark) 100%);
  color: white;
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  box-shadow: 0 12px 32px rgba(225, 29, 42, 0.2);
  position: relative;
  overflow: hidden;
}
.zoho-banner::before {
  content: ''; position: absolute; top: -40%; right: -10%;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.zoho-left { display: flex; align-items: center; gap: 14px; position: relative; z-index: 2; }
.zoho-icon {
  width: 52px; height: 52px;
  background: rgba(255,255,255,0.18);
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
}
.zoho-title { font-size: 17px; font-weight: 700; }
.zoho-sub { font-size: 13px; opacity: 0.92; }
.zoho-banner .btn { position: relative; z-index: 2; background: white; color: var(--brand-red-dark); }
.zoho-banner .btn:hover { background: var(--bg-light); }

/* ============ KRONOS-STYLE TIMECARD ============ */
.kronos-bar {
  background: var(--bg-light);
  border: 1px solid var(--border);
  border-radius: var(--radius) var(--radius) 0 0;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
  border-bottom: none;
}
.kronos-bar-left, .kronos-bar-meta, .kronos-bar-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.kronos-btn-approve {
  background: var(--brand-red);
  border: none;
  padding: 9px 16px;
  border-radius: var(--radius-pill);
  font-size: 12px;
  font-weight: 700;
  color: white;
  display: inline-flex; align-items: center; gap: 6px;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
  box-shadow: 0 2px 8px rgba(225, 29, 42, 0.25);
}
.kronos-btn-approve:hover:not(:disabled) { background: var(--brand-red-hover); transform: translateY(-1px); }
.kronos-btn-approve:disabled { opacity: 0.5; cursor: not-allowed; }
.kronos-period-select {
  background: white;
  padding: 7px 12px;
  font-size: 13px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-family: inherit;
  width: auto;
}
.kronos-action {
  background: white;
  border: 1px solid var(--border);
  padding: 6px 10px;
  border-radius: var(--radius);
  font-size: 10px;
  color: var(--slate);
  cursor: pointer;
  transition: all 0.15s;
  display: flex; flex-direction: column; align-items: center; gap: 2px;
  min-width: 60px;
  font-family: inherit;
  font-weight: 600;
}
.kronos-action:hover { background: var(--bg-light); border-color: var(--brand-red); color: var(--brand-red); }
.kronos-action span:first-child { font-size: 16px; }
.kronos-action-save { background: var(--ink); color: white; border-color: var(--ink); }
.kronos-action-save:hover { background: #000; color: white; }

.kronos-table-wrap {
  overflow-x: auto;
  border: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  background: white;
}
.kronos-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.kronos-table th {
  background: var(--bg-light);
  color: var(--slate);
  padding: 10px 8px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
  text-align: center;
  white-space: nowrap;
}
.kronos-table td {
  padding: 8px;
  border-bottom: 1px solid var(--border);
  text-align: center;
  vertical-align: middle;
  background: white;
}
.kronos-row:hover td { background: var(--brand-red-pale); }
.kronos-row-today td { background: #FFF5F6 !important; }
.kronos-row-today td:hover { background: var(--brand-red-soft) !important; }
.kronos-row-missing td { background: #FAFAFB; color: var(--warm-gray); }
.kronos-row-total td {
  background: var(--ink) !important;
  color: white;
  font-weight: 700;
}
.kronos-date {
  font-weight: 700;
  color: var(--ink);
  text-align: left !important;
  padding-left: 12px !important;
  white-space: nowrap;
}
.kronos-code { color: var(--slate); font-size: 11px; }
.kronos-punch { font-variant-numeric: tabular-nums; color: var(--brand-red); font-weight: 600; }
.kronos-total { font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
.kronos-total-daily { background: var(--bg-light) !important; }
.kronos-total-period { background: var(--brand-red-soft) !important; color: var(--brand-red); }
.kronos-actions-cell {
  display: flex;
  gap: 2px;
  padding: 4px !important;
  justify-content: center;
}
.kronos-mini {
  width: 20px; height: 20px;
  border-radius: 4px;
  border: 1px solid var(--border);
  background: white;
  font-size: 11px;
  line-height: 1;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700;
  color: var(--success);
  font-family: inherit;
}
.kronos-mini:hover { background: var(--success-light); }
.kronos-mini-x { color: var(--danger); }

/* ============ ORG CHART ============ */
.org-chart {
  background: white;
  border-radius: var(--radius-lg);
  padding: 36px 24px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  overflow-x: auto;
}
.org-node-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}
.org-node {
  background: white;
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  padding: 16px 22px;
  text-align: center;
  min-width: 180px;
  max-width: 230px;
  box-shadow: var(--shadow-sm);
  margin: 8px;
  cursor: pointer;
  transition: all 0.15s;
  position: relative;
  z-index: 2;
}
.org-node:hover {
  border-color: var(--brand-red);
  box-shadow: 0 8px 24px rgba(225, 29, 42, 0.15);
  transform: translateY(-2px);
}
.org-node-me {
  border-color: var(--brand-red);
  background: linear-gradient(135deg, var(--brand-red-pale) 0%, white 100%);
}
.org-node-admin { border-top: 3px solid var(--brand-red); }
.org-avatar { margin: 0 auto 8px; width: 44px; height: 44px; font-size: 14px; }
.org-name { font-weight: 800; color: var(--ink); font-size: 14px; line-height: 1.2; }
.org-position { color: var(--slate); font-size: 12px; margin-top: 3px; }
.org-dept {
  display: inline-block;
  background: var(--brand-red-soft);
  color: var(--brand-red);
  padding: 1px 8px;
  border-radius: var(--radius-pill);
  font-size: 10px;
  margin-top: 6px;
  font-weight: 700;
}
.org-meta {
  color: var(--warm-gray);
  font-size: 10px;
  margin-top: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}
.org-children {
  display: flex;
  gap: 16px;
  margin-top: 18px;
  position: relative;
  padding-top: 22px;
  flex-wrap: wrap;
  justify-content: center;
}
.org-children::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 18px;
  background: var(--brand-red);
}
.org-children > .org-node-wrap::before {
  content: '';
  position: absolute;
  top: -22px;
  left: 50%;
  transform: translateX(-50%);
  width: 2px;
  height: 18px;
  background: var(--brand-red);
}

/* ============ TIMESHEET INPUTS ============ */
.ts-input {
  padding: 6px 8px;
  font-size: 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-family: inherit;
  background: white;
  width: auto;
  min-width: 100px;
}
.ts-input:focus { border-color: var(--brand-red); outline: none; box-shadow: 0 0 0 3px rgba(225, 29, 42, 0.1); }

/* ============ VERSION FOOTER ============ */
.version-footer {
  margin-top: auto;
  padding: 12px 14px;
  font-size: 10px;
  color: var(--warm-gray);
  text-align: center;
  letter-spacing: 0.5px;
  border-top: 1px solid var(--border);
  margin-top: 12px;
}
.version-footer strong { color: var(--brand-red); font-weight: 800; }

/* compatibility aliases for any leftover var refs */
.brand-logo-svg { display: block; }
"""

# ------------------ JS ------------------
# We'll write the JS as a Python raw string for ease of editing
JS = r"""
// ============ DATA LAYER ============
const STORAGE_KEY = 'savonnexo_portal_v4';
const APP_VERSION = '0.1';
const ZOHO_MAIL_URL = 'https://workplace.zoho.com/#mail_app/mail/folder/inbox';

function uid(prefix = 'id') {
  return prefix + '_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
}

function todayISO() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}

function loadDB() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored) {
    try { return JSON.parse(stored); } catch(e) { console.warn('parse fail', e); }
  }
  // Seed with sample data
  const now = new Date();
  const yesterday = new Date(now.getTime() - 86400000);
  const twoDaysAgo = new Date(now.getTime() - 2 * 86400000);

  const db = {
    users: [
      { id: 'u_owner', email: 'owner@savonnexo.com', password: 'admin123', name: 'Sarah Owens', role: 'admin', position: 'Owner / HR Manager', department: 'Executive', managerId: null, tastingAccess: true, active: true, createdAt: '2025-01-15' },
      { id: 'u_david', email: 'david@savonnexo.com', password: 'david123', name: 'David Cole', role: 'admin', position: 'Operations Manager', department: 'Operations', managerId: 'u_owner', tastingAccess: false, active: true, createdAt: '2025-01-30' },
      { id: 'u_portia', email: 'portia@savonnexo.com', password: 'portia123', name: 'Portia Bellamkonda', role: 'employee', position: 'Wine & Spirits Manager', department: 'Sales & Tasting', managerId: 'u_david', tastingAccess: true, active: true, createdAt: '2025-02-10' },
      { id: 'u_mike', email: 'mike@savonnexo.com', password: 'mike123', name: 'Mike Reeves', role: 'employee', position: 'Cashier', department: 'Floor', managerId: 'u_david', tastingAccess: false, active: true, createdAt: '2025-03-05' },
      { id: 'u_jenna', email: 'jenna@savonnexo.com', password: 'jenna123', name: 'Jenna Park', role: 'employee', position: 'Stock Associate', department: 'Floor', managerId: 'u_david', tastingAccess: false, active: true, createdAt: '2025-03-22' }
    ],
    sessionUserId: null,
    timeEntries: [
      { id: uid('te'), userId: 'u_portia', clockIn: yesterday.toISOString().slice(0,10) + 'T09:00:00', clockOut: yesterday.toISOString().slice(0,10) + 'T17:32:00', note: '', edited: false },
      { id: uid('te'), userId: 'u_mike', clockIn: yesterday.toISOString().slice(0,10) + 'T08:00:00', clockOut: yesterday.toISOString().slice(0,10) + 'T16:05:00', note: '', edited: false },
      { id: uid('te'), userId: 'u_jenna', clockIn: yesterday.toISOString().slice(0,10) + 'T10:00:00', clockOut: yesterday.toISOString().slice(0,10) + 'T18:00:00', note: '', edited: false },
      { id: uid('te'), userId: 'u_portia', clockIn: twoDaysAgo.toISOString().slice(0,10) + 'T09:00:00', clockOut: twoDaysAgo.toISOString().slice(0,10) + 'T17:00:00', note: '', edited: false }
    ],
    shifts: generateSampleShifts(),
    announcements: [
      { id: uid('an'), title: 'Welcome to the new savonNEXO Portal', body: 'Hi team — this is our brand new employee portal. Please clock in & out each day, and use the schedule view to see your shifts. Reach out to HR with any questions!', authorId: 'u_owner', createdAt: now.toISOString(), pinned: true },
      { id: uid('an'), title: 'Memorial Day Weekend Hours', body: 'We will be open 9 AM – 6 PM on Memorial Day. Please double-check your shift assignments and reach out to David if you have conflicts.', authorId: 'u_owner', createdAt: yesterday.toISOString(), pinned: false }
    ],
    timeOff: [
      { id: uid('to'), userId: 'u_mike', startDate: addDaysISO(7), endDate: addDaysISO(9), type: 'Vacation', reason: 'Family trip', status: 'pending', reviewedBy: null, reviewedAt: null, reviewNote: '' },
      { id: uid('to'), userId: 'u_jenna', startDate: addDaysISO(-14), endDate: addDaysISO(-12), type: 'Sick', reason: 'Flu', status: 'approved', reviewedBy: 'u_owner', reviewedAt: addDaysISO(-15) + 'T10:00:00', reviewNote: 'Feel better!' }
    ],
    tastings: SEED_TASTINGS.tastings.map((t, i) => ({...t, id: 't_seed_' + i})),
    timesheets: [
      {
        id: uid('ws'),
        userId: 'u_mike',
        weekStart: getWeekRange(-1).start,
        entries: [
          { date: addDaysISO(-7), in1: '08:00', out1: '12:00', in2: '13:00', out2: '17:00', payCode: 'Regular', notes: '' },
          { date: addDaysISO(-6), in1: '08:00', out1: '12:00', in2: '13:00', out2: '16:30', payCode: 'Regular', notes: '' },
          { date: addDaysISO(-5), in1: '09:00', out1: '13:00', in2: '14:00', out2: '18:00', payCode: 'Regular', notes: '' },
          { date: addDaysISO(-4), in1: '', out1: '', in2: '', out2: '', payCode: 'Off', notes: '' },
          { date: addDaysISO(-3), in1: '08:00', out1: '12:00', in2: '13:00', out2: '17:00', payCode: 'Regular', notes: '' }
        ],
        status: 'approved',
        submittedAt: addDaysISO(-3) + 'T18:00:00',
        reviewedBy: 'u_david',
        reviewedAt: addDaysISO(-3) + 'T20:00:00',
        reviewNote: 'Looks good'
      }
    ]
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
  return db;
}

function addDaysISO(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().slice(0,10);
}

function generateSampleShifts() {
  const shifts = [];
  const users = ['u_portia', 'u_mike', 'u_jenna', 'u_david'];
  const positions = { u_portia: 'Wine & Spirits Floor', u_mike: 'Cashier', u_jenna: 'Stocking', u_david: 'Floor Manager' };
  for (let i = -3; i < 14; i++) {
    const date = addDaysISO(i);
    users.forEach((uid_, idx) => {
      // randomize: skip ~30% of days
      if ((i + idx) % 3 === 1) return;
      shifts.push({
        id: 'sh_' + i + '_' + uid_,
        userId: uid_,
        date,
        start: idx % 2 === 0 ? '09:00' : '13:00',
        end: idx % 2 === 0 ? '17:00' : '21:00',
        position: positions[uid_],
        notes: ''
      });
    });
  }
  return shifts;
}

let DB;
function saveDB() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(DB));
}

function currentUser() {
  if (!DB.sessionUserId) return null;
  return DB.users.find(u => u.id === DB.sessionUserId);
}

function isAdmin() {
  const u = currentUser();
  return u && u.role === 'admin';
}

// ============ AUTH ============
function login(email, password) {
  const user = DB.users.find(u => u.email.toLowerCase() === email.toLowerCase().trim() && u.password === password && u.active);
  if (!user) return false;
  DB.sessionUserId = user.id;
  saveDB();
  return true;
}

function logout() {
  DB.sessionUserId = null;
  saveDB();
  renderApp();
}

function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;
  const err = document.getElementById('login-error');
  if (login(email, password)) {
    err.classList.remove('active');
    renderApp();
  } else {
    err.textContent = 'Invalid email or password. Try one of the demo accounts below.';
    err.classList.add('active');
  }
}

function fillDemoCred(email, password) {
  document.getElementById('login-email').value = email;
  document.getElementById('login-password').value = password;
}

// ============ TIME / DATE HELPERS ============
function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso.length === 10 ? iso + 'T12:00:00' : iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}
function fmtDateShort(iso) {
  if (!iso) return '';
  const d = new Date(iso.length === 10 ? iso + 'T12:00:00' : iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}
function fmtDay(iso) {
  if (!iso) return '';
  const d = new Date(iso.length === 10 ? iso + 'T12:00:00' : iso);
  return ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][d.getDay()];
}
function fmtTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}
function fmtTimeRange(startStr, endStr) {
  const fmt = t => {
    if (!t) return '';
    const [h, m] = t.split(':');
    const hour = parseInt(h);
    const period = hour >= 12 ? 'PM' : 'AM';
    const dh = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
    return dh + ':' + m + ' ' + period;
  };
  return fmt(startStr) + ' – ' + fmt(endStr);
}
function fmtDuration(ms) {
  if (!ms || ms < 0) return '0h 0m';
  const totalMin = Math.floor(ms / 60000);
  const h = Math.floor(totalMin / 60);
  const m = totalMin % 60;
  return h + 'h ' + m + 'm';
}
function fmtDurationHM(ms) {
  if (!ms || ms < 0) return '0:00:00';
  const totalSec = Math.floor(ms / 1000);
  const h = Math.floor(totalSec / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  const s = totalSec % 60;
  return String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
}
function getWeekRange(offset = 0) {
  const d = new Date();
  d.setHours(0,0,0,0);
  const dow = d.getDay();
  const daysSinceMonday = dow === 0 ? 6 : dow - 1;
  const monday = new Date(d);
  monday.setDate(d.getDate() - daysSinceMonday + (offset * 7));
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  const fmt = x => x.getFullYear() + '-' + String(x.getMonth()+1).padStart(2,'0') + '-' + String(x.getDate()).padStart(2,'0');
  return { start: fmt(monday), end: fmt(sunday) };
}
function escapeHtml(s) {
  if (s == null) return '';
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
}
function initials(name) {
  if (!name) return '?';
  return name.split(/\s+/).map(p => p[0]).slice(0, 2).join('').toUpperCase();
}

// ============ APP RENDERING ============
let currentView = 'dashboard';
let clockTickerInterval = null;

function renderApp() {
  const root = document.getElementById('root');
  const u = currentUser();
  if (!u) {
    renderLogin(root);
    return;
  }
  root.innerHTML = `
    <div class="app">
      <div class="mobile-overlay" id="mobile-overlay" onclick="toggleSidebar()"></div>
      <aside class="sidebar" id="sidebar">
        ${renderSidebar(u)}
      </aside>
      <div class="content">
        <div style="display:flex; align-items:center; justify-content: space-between; margin-bottom: 8px;">
          <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
        </div>
        <div id="view"></div>
      </div>
    </div>
    <div id="modal-host"></div>
    <div class="toast" id="toast">Saved</div>
  `;
  renderView();
}

const LOGO_IMG = '<img src="__LOGO_DATA_URL__" alt="Savon Nexo" class="brand-logo-img" />';

function renderLogin(root) {
  root.innerHTML = `
    <div class="login-screen">
      <div class="login-card">
        <div class="login-brand">
          <div class="logo-wide">${LOGO_IMG}</div>
          <div class="tagline">EMPLOYEE PORTAL</div>
        </div>
        <form onsubmit="handleLogin(event)">
          <div class="field">
            <label class="label">Email</label>
            <input type="email" id="login-email" required autofocus placeholder="you@savonnexo.com">
          </div>
          <div class="field">
            <label class="label">Password</label>
            <input type="password" id="login-password" required placeholder="••••••••">
          </div>
          <div class="login-error" id="login-error"></div>
          <button class="btn btn-primary btn-block btn-lg" type="submit">Sign In</button>
        </form>
        <div class="demo-creds">
          <div class="title">— Demo Accounts (click to fill) —</div>
          <div class="cred" onclick="fillDemoCred('owner@savonnexo.com', 'admin123')">
            <span>owner@savonnexo.com</span>
            <span class="role">HR / Admin</span>
          </div>
          <div class="cred" onclick="fillDemoCred('portia@savonnexo.com', 'portia123')">
            <span>portia@savonnexo.com</span>
            <span class="role">Tasting Mgr</span>
          </div>
          <div class="cred" onclick="fillDemoCred('mike@savonnexo.com', 'mike123')">
            <span>mike@savonnexo.com</span>
            <span class="role">Employee</span>
          </div>
        </div>
        <div class="login-version">
          <strong>Version 0.1</strong> &nbsp;·&nbsp; Built by Savon Nexo LLC
          <div style="margin-top:4px;">Business Intelligence · Data Analytics · Web Solutions</div>
        </div>
      </div>
    </div>
  `;
}

function renderSidebar(u) {
  const isAdminRole = u.role === 'admin';
  const hasTasting = u.tastingAccess || isAdminRole;
  // A manager is anyone who has direct reports
  const isManager = DB.users.some(x => x.managerId === u.id);
  const nav = [
    { id: 'dashboard', icon: '🏠', label: 'Dashboard' },
    { id: 'clock', icon: '⏱', label: 'Clock In/Out' },
    { id: 'mytime', icon: '📋', label: 'My Timecard' },
    { id: 'timesheet', icon: '📝', label: 'Weekly Timesheet' },
    { id: 'schedule', icon: '📅', label: 'Schedule' },
    { id: 'announcements', icon: '📣', label: 'Announcements' },
    { id: 'timeoff', icon: '🌴', label: 'Time Off' },
    { id: 'orgchart', icon: '🏢', label: 'Org Chart' }
  ];
  if (hasTasting) nav.push({ id: 'tastings', icon: '🍷', label: 'Tastings' });
  nav.push({ id: 'profile', icon: '⚙', label: 'My Profile' });

  let adminNav = [];
  if (isManager || isAdminRole) {
    adminNav.push({ id: 'tsapprovals', icon: '✍', label: 'Timesheet Approvals' });
  }
  if (isAdminRole) {
    adminNav = adminNav.concat([
      { id: 'employees', icon: '👥', label: 'Employees' },
      { id: 'alltime', icon: '📊', label: 'Time Records' },
      { id: 'approvals', icon: '✓', label: 'Time-Off Approvals' },
      { id: 'allshifts', icon: '🗓', label: 'Manage Shifts' }
    ]);
  }

  return `
    <div class="sidebar-brand">
      <div class="logo-wide-sidebar">${LOGO_IMG}</div>
    </div>
    <nav style="flex:1; overflow-y: auto;">
      <div class="nav-section">
        <div class="nav-section-title">Workspace</div>
        ${nav.map(n => `
          <button class="nav-item ${currentView === n.id ? 'active' : ''}" onclick="navigate('${n.id}')">
            <span class="nav-icon">${n.icon}</span>
            <span>${n.label}</span>
          </button>`).join('')}
      </div>
      ${adminNav.length ? `
        <div class="nav-section">
          <div class="nav-section-title">HR / Admin</div>
          ${adminNav.map(n => `
            <button class="nav-item ${currentView === n.id ? 'active' : ''}" onclick="navigate('${n.id}')">
              <span class="nav-icon">${n.icon}</span>
              <span>${n.label}</span>
            </button>`).join('')}
        </div>
      ` : ''}
    </nav>
    <div class="sidebar-footer">
      <div class="user-card">
        <div class="avatar">${initials(u.name)}</div>
        <div class="info">
          <div class="name">${escapeHtml(u.name)}</div>
          <div class="position">${escapeHtml(u.position)}</div>
        </div>
        <button class="logout-btn" onclick="logout()" title="Sign out">⎋</button>
      </div>
      <div class="version-footer">
        <strong>Version ${APP_VERSION}</strong><br>
        Built by Savon Nexo LLC
      </div>
    </div>
  `;
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('mobile-overlay').classList.toggle('active');
}

function navigate(view) {
  currentView = view;
  if (window.innerWidth <= 900) toggleSidebar();
  renderApp();
}

function renderView() {
  const host = document.getElementById('view');
  if (clockTickerInterval) { clearInterval(clockTickerInterval); clockTickerInterval = null; }
  switch(currentView) {
    case 'dashboard': renderDashboard(host); break;
    case 'clock': renderClock(host); break;
    case 'mytime': renderMyTime(host); break;
    case 'timesheet': renderTimesheet(host); break;
    case 'schedule': renderSchedule(host); break;
    case 'announcements': renderAnnouncements(host); break;
    case 'timeoff': renderTimeOff(host); break;
    case 'orgchart': renderOrgChart(host); break;
    case 'tastings': renderTastings(host); break;
    case 'profile': renderProfile(host); break;
    case 'tsapprovals': renderTimesheetApprovals(host); break;
    case 'employees': isAdmin() ? renderEmployees(host) : renderDashboard(host); break;
    case 'alltime': isAdmin() ? renderAllTime(host) : renderDashboard(host); break;
    case 'approvals': isAdmin() ? renderApprovals(host) : renderDashboard(host); break;
    case 'allshifts': isAdmin() ? renderAllShifts(host) : renderDashboard(host); break;
    default: renderDashboard(host);
  }
}

// ============ VIEW: DASHBOARD ============
function renderDashboard(host) {
  const u = currentUser();
  const today = todayISO();
  const myEntries = DB.timeEntries.filter(e => e.userId === u.id);
  const openEntry = myEntries.find(e => !e.clockOut);
  const week = getWeekRange();
  const weekEntries = myEntries.filter(e => e.clockIn.slice(0,10) >= week.start && e.clockIn.slice(0,10) <= week.end);
  let weekMs = 0;
  weekEntries.forEach(e => {
    const out = e.clockOut ? new Date(e.clockOut) : new Date();
    weekMs += out - new Date(e.clockIn);
  });

  const myShifts = DB.shifts
    .filter(s => s.userId === u.id && s.date >= today)
    .sort((a, b) => a.date.localeCompare(b.date))
    .slice(0, 3);

  const recentAnn = [...DB.announcements].sort((a, b) => {
    if (a.pinned !== b.pinned) return b.pinned - a.pinned;
    return b.createdAt.localeCompare(a.createdAt);
  }).slice(0, 3);

  const pendingTimeoff = DB.timeOff.filter(t => t.userId === u.id && t.status === 'pending').length;

  const manager = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Welcome back, ${escapeHtml(u.name.split(' ')[0])}</div>
        <div class="page-subtitle">${fmtDay(today)}, ${fmtDate(today)}${manager ? ' · Reports to ' + escapeHtml(manager.name) : ''}</div>
      </div>
      <div class="page-actions">
        <a class="btn btn-gold" href="${ZOHO_MAIL_URL}" target="_blank" rel="noopener">📧 Open Zoho Mail</a>
        <button class="btn ${openEntry ? 'btn-danger' : 'btn-primary'}" onclick="navigate('clock')">
          ${openEntry ? '⏸ Clock Out' : '▶ Clock In'}
        </button>
      </div>
    </div>

    <div class="zoho-banner">
      <div class="zoho-left">
        <div class="zoho-icon">📧</div>
        <div>
          <div class="zoho-title">Zoho Workplace Mail</div>
          <div class="zoho-sub">Check your inbox, calendar invites, and team messages</div>
        </div>
      </div>
      <a class="btn btn-primary" href="${ZOHO_MAIL_URL}" target="_blank" rel="noopener">Open Inbox ↗</a>
    </div>

    <div class="grid grid-4" style="margin-bottom: 24px;">
      <div class="stat-card">
        <div class="stat-label">Status</div>
        <div class="stat-number" style="font-size: 22px; padding-top:8px;">${openEntry ? 'Clocked In' : 'Clocked Out'}</div>
        <div class="stat-sub">${openEntry ? 'Since ' + fmtTime(openEntry.clockIn) : 'Not currently working'}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Hours This Week</div>
        <div class="stat-number">${(weekMs / 3600000).toFixed(1)}</div>
        <div class="stat-sub">${weekEntries.length} sessions</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Upcoming Shifts</div>
        <div class="stat-number">${myShifts.length}</div>
        <div class="stat-sub">in the next two weeks</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Time-off Pending</div>
        <div class="stat-number">${pendingTimeoff}</div>
        <div class="stat-sub">request${pendingTimeoff === 1 ? '' : 's'}</div>
      </div>
    </div>

    <div class="grid grid-2">
      <div class="card">
        <div class="card-title">📅 Your Next Shifts</div>
        <div class="card-subtitle">Upcoming scheduled work</div>
        ${myShifts.length === 0
          ? '<div style="color:var(--warm-gray); font-style:italic; padding: 12px 0;">No upcoming shifts scheduled.</div>'
          : myShifts.map(s => `
            <div style="padding: 12px 0; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-weight: 600;">${fmtDay(s.date)}, ${fmtDate(s.date)}</div>
                <div style="font-size: 13px; color: var(--slate);">${escapeHtml(s.position)}</div>
              </div>
              <div style="font-family: 'Playfair Display', Georgia, serif; color: var(--burgundy); font-weight: 600;">
                ${fmtTimeRange(s.start, s.end)}
              </div>
            </div>
          `).join('')}
      </div>
      <div class="card">
        <div class="card-title">📣 Latest Announcements</div>
        <div class="card-subtitle">Notes from leadership</div>
        ${recentAnn.length === 0
          ? '<div style="color:var(--warm-gray); font-style:italic; padding: 12px 0;">No announcements.</div>'
          : recentAnn.map(a => {
            const author = DB.users.find(x => x.id === a.authorId);
            return `
              <div style="padding: 12px 0; border-bottom: 1px solid var(--border);">
                <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <div style="font-weight: 600; color: var(--burgundy-dark);">${a.pinned ? '📌 ' : ''}${escapeHtml(a.title)}</div>
                  <div style="font-size: 11px; color: var(--warm-gray);">${fmtDateShort(a.createdAt)}</div>
                </div>
                <div style="font-size: 13px; color: var(--slate); line-height: 1.5;">${escapeHtml(a.body.slice(0, 140))}${a.body.length > 140 ? '…' : ''}</div>
                <div style="font-size: 11px; color: var(--warm-gray); font-style: italic; margin-top: 4px;">${author ? '— ' + escapeHtml(author.name) : ''}</div>
              </div>
            `;
          }).join('')}
      </div>
    </div>
  `;
}

// ============ VIEW: CLOCK ============
function renderClock(host) {
  const u = currentUser();
  const myEntries = DB.timeEntries.filter(e => e.userId === u.id);
  const openEntry = myEntries.find(e => !e.clockOut);

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Time Clock</div>
        <div class="page-subtitle">Sign in for the day, take a break, sign out</div>
      </div>
    </div>
    <div class="clock-hero" id="clock-hero">
      <div class="clock-time" id="big-clock"></div>
      <div class="clock-date" id="big-date"></div>
      <div class="clock-status ${openEntry ? 'active' : ''}">
        <span class="dot"></span>
        ${openEntry ? 'On the clock since ' + fmtTime(openEntry.clockIn) : 'Not clocked in'}
      </div>
      ${openEntry ? `<div class="clock-elapsed" id="elapsed-time">0:00:00</div>` : ''}
      <div style="margin-top: 16px;">
        ${openEntry
          ? `<button class="clock-btn stop" onclick="clockOut()">⏸ Clock Out</button>`
          : `<button class="clock-btn start" onclick="clockIn()">▶ Clock In</button>`}
      </div>
    </div>

    <div style="margin-top: 28px;">
      <div class="card">
        <div class="card-title">Recent Time Entries</div>
        <div class="card-subtitle">Your last 7 shifts</div>
        ${renderTimeEntriesTable(myEntries.slice().sort((a,b) => b.clockIn.localeCompare(a.clockIn)).slice(0, 7), false)}
      </div>
    </div>
  `;

  function tick() {
    const now = new Date();
    const big = document.getElementById('big-clock');
    const dateEl = document.getElementById('big-date');
    if (!big) return;
    big.textContent = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' });
    dateEl.textContent = now.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
    if (openEntry) {
      const el = document.getElementById('elapsed-time');
      if (el) el.textContent = fmtDurationHM(now - new Date(openEntry.clockIn));
    }
  }
  tick();
  clockTickerInterval = setInterval(tick, 1000);
}

function clockIn() {
  const u = currentUser();
  const open = DB.timeEntries.find(e => e.userId === u.id && !e.clockOut);
  if (open) { showToast('Already clocked in', 'error'); return; }
  DB.timeEntries.push({
    id: uid('te'),
    userId: u.id,
    clockIn: new Date().toISOString(),
    clockOut: null,
    note: '',
    edited: false
  });
  saveDB();
  showToast('Clocked in', 'success');
  renderView();
}

function clockOut() {
  const u = currentUser();
  const open = DB.timeEntries.find(e => e.userId === u.id && !e.clockOut);
  if (!open) { showToast('No active session', 'error'); return; }
  open.clockOut = new Date().toISOString();
  saveDB();
  showToast('Clocked out', 'success');
  renderView();
}

function renderTimeEntriesTable(entries, showUser = false, allowEdit = false) {
  if (entries.length === 0) {
    return '<div class="empty"><div class="empty-icon">⏱</div><div>No time entries yet.</div></div>';
  }
  return `
    <div class="table-scroll" style="margin: 0 -22px -22px; border-top: 1px solid var(--border);">
      <table>
        <thead><tr>
          ${showUser ? '<th>Employee</th>' : ''}
          <th>Date</th><th>Clock In</th><th>Clock Out</th><th>Duration</th><th>Note</th>
          ${allowEdit ? '<th></th>' : ''}
        </tr></thead>
        <tbody>
          ${entries.map(e => {
            const user = DB.users.find(u => u.id === e.userId);
            const out = e.clockOut ? new Date(e.clockOut) : null;
            const duration = out ? fmtDuration(out - new Date(e.clockIn)) : '<span class="badge badge-success">In progress</span>';
            return `
              <tr>
                ${showUser ? `<td><strong>${escapeHtml(user ? user.name : '—')}</strong></td>` : ''}
                <td>${fmtDate(e.clockIn)}</td>
                <td>${fmtTime(e.clockIn)}</td>
                <td>${e.clockOut ? fmtTime(e.clockOut) : '—'}</td>
                <td><strong>${duration}</strong>${e.edited ? ' <span class="badge badge-warning" title="Edited by HR">edited</span>' : ''}</td>
                <td style="color: var(--slate); font-size: 12px;">${escapeHtml(e.note || '')}</td>
                ${allowEdit ? `<td><button class="btn btn-sm btn-ghost" onclick="editTimeEntry('${e.id}')">Edit</button> <button class="btn btn-sm btn-ghost" onclick="deleteTimeEntry('${e.id}')" style="color:var(--danger);">Delete</button></td>` : ''}
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ============ VIEW: MY TIME ============
// Kronos-style timecard
let kronosWeekOffset = 0;
function renderMyTime(host) {
  const u = currentUser();
  const r = getWeekRange(kronosWeekOffset);
  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(r.start + 'T12:00:00');
    d.setDate(d.getDate() + i);
    days.push(d.toISOString().slice(0,10));
  }

  // For each day, find entries (could be multiple = morning + afternoon)
  function dayPunches(date) {
    const entries = DB.timeEntries.filter(e => e.userId === u.id && e.clockIn.slice(0,10) === date)
      .sort((a,b) => a.clockIn.localeCompare(b.clockIn));
    const punches = { in1:'', out1:'', in2:'', out2:'', shift1: 0, shift2: 0 };
    if (entries[0]) {
      punches.in1 = entries[0].clockIn.slice(11,16);
      if (entries[0].clockOut) {
        punches.out1 = entries[0].clockOut.slice(11,16);
        punches.shift1 = (new Date(entries[0].clockOut) - new Date(entries[0].clockIn)) / 3600000;
      }
    }
    if (entries[1]) {
      punches.in2 = entries[1].clockIn.slice(11,16);
      if (entries[1].clockOut) {
        punches.out2 = entries[1].clockOut.slice(11,16);
        punches.shift2 = (new Date(entries[1].clockOut) - new Date(entries[1].clockIn)) / 3600000;
      }
    }
    punches.daily = punches.shift1 + punches.shift2;
    return punches;
  }

  let periodTotal = 0;
  const rows = days.map(d => {
    const p = dayPunches(d);
    periodTotal += p.daily;
    return { date: d, ...p, periodTotal };
  });

  // Check if there's a submitted timesheet for this week
  const submittedTs = DB.timesheets.find(t => t.userId === u.id && t.weekStart === r.start);
  const statusBadge = submittedTs
    ? `<span class="badge ${submittedTs.status === 'approved' ? 'badge-success' : submittedTs.status === 'rejected' ? 'badge-danger' : 'badge-warning'}">${submittedTs.status.toUpperCase()}</span>`
    : '<span class="badge badge-muted">NOT SUBMITTED</span>';

  const now = new Date();
  const loadedStr = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">My Timecard</div>
        <div class="page-subtitle">Track your hours by week · ${statusBadge}</div>
      </div>
    </div>

    <div class="kronos-bar">
      <div class="kronos-bar-left">
        <button class="kronos-btn-approve" onclick="submitTimesheet()" ${submittedTs && submittedTs.status === 'approved' ? 'disabled' : ''}>
          <span style="font-size:16px;">✓</span><span>${submittedTs ? 'Re-Submit Timesheet' : 'Submit for Approval'}</span>
        </button>
      </div>
      <div class="kronos-bar-meta">
        <span style="color:#666;font-size:12px;">Loaded: ${loadedStr}</span>
        <select class="kronos-period-select" onchange="setKronosWeek(parseInt(this.value))">
          <option value="0" ${kronosWeekOffset === 0 ? 'selected' : ''}>Current Pay Period</option>
          <option value="-1" ${kronosWeekOffset === -1 ? 'selected' : ''}>Previous Pay Period</option>
          <option value="-2" ${kronosWeekOffset === -2 ? 'selected' : ''}>2 weeks ago</option>
          <option value="-3" ${kronosWeekOffset === -3 ? 'selected' : ''}>3 weeks ago</option>
          <option value="1" ${kronosWeekOffset === 1 ? 'selected' : ''}>Next Pay Period</option>
        </select>
      </div>
      <div class="kronos-bar-right">
        <button class="kronos-action" onclick="window.print()" title="Print Timecard"><span>🖨</span><span>Print<br>Timecard</span></button>
        <button class="kronos-action" onclick="renderView()" title="Refresh"><span>🔄</span><span>Refresh</span></button>
        <button class="kronos-action" onclick="recalcKronos()" title="Calculate Totals"><span>🧮</span><span>Calculate<br>Totals</span></button>
        <button class="kronos-action kronos-action-save" onclick="saveKronosWeek()" title="Save"><span>💾</span><span>Save</span></button>
      </div>
    </div>

    <div class="kronos-table-wrap">
      <table class="kronos-table">
        <thead>
          <tr>
            <th style="width:46px;"></th>
            <th>Date</th>
            <th>Pay Code</th>
            <th style="width:80px;">Amount</th>
            <th>In</th>
            <th>Transfer</th>
            <th>Out</th>
            <th>In</th>
            <th>Transfer</th>
            <th>Out</th>
            <th>Shift</th>
            <th>Daily</th>
            <th>Period</th>
            <th>Schedule</th>
          </tr>
        </thead>
        <tbody>
          ${rows.map((row, i) => {
            const isToday = row.date === todayISO();
            const isPast = row.date < todayISO();
            const shiftStr = row.daily > 0 ? row.daily.toFixed(2) : '';
            return `
              <tr class="kronos-row ${isToday ? 'kronos-row-today' : ''} ${isPast && !shiftStr ? 'kronos-row-missing' : ''}">
                <td class="kronos-actions-cell">
                  <button class="kronos-mini" onclick="kronosAddPunch('${row.date}')" title="Add punch">+</button>
                  <button class="kronos-mini kronos-mini-x" onclick="kronosClearDay('${row.date}')" title="Clear day">×</button>
                </td>
                <td class="kronos-date">${fmtDay(row.date).slice(0,3)} ${new Date(row.date+'T12:00:00').toLocaleDateString('en-US',{month:'numeric',day:'numeric'})}</td>
                <td class="kronos-code">${shiftStr ? 'Regular' : ''}</td>
                <td></td>
                <td class="kronos-punch">${row.in1 ? fmtTime12(row.in1) : ''}</td>
                <td></td>
                <td class="kronos-punch">${row.out1 ? fmtTime12(row.out1) : ''}</td>
                <td class="kronos-punch">${row.in2 ? fmtTime12(row.in2) : ''}</td>
                <td></td>
                <td class="kronos-punch">${row.out2 ? fmtTime12(row.out2) : ''}</td>
                <td class="kronos-total">${shiftStr}</td>
                <td class="kronos-total kronos-total-daily">${shiftStr ? row.daily.toFixed(2) : ''}</td>
                <td class="kronos-total kronos-total-period">${row.periodTotal > 0 ? row.periodTotal.toFixed(2) : ''}</td>
                <td></td>
              </tr>
            `;
          }).join('')}
          <tr class="kronos-row-total">
            <td colspan="10" style="text-align:right;padding-right:14px;color:var(--burgundy-dark);font-weight:700;">PERIOD TOTAL</td>
            <td colspan="2"></td>
            <td class="kronos-total kronos-total-period" style="font-size:14px;">${periodTotal.toFixed(2)}</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-3" style="margin-top: 24px;">
      <div class="stat-card">
        <div class="stat-label">Period Total</div>
        <div class="stat-number">${periodTotal.toFixed(1)}<span style="font-size:18px;color:var(--slate);"> hrs</span></div>
        <div class="stat-sub">${fmtDateShort(r.start)} – ${fmtDateShort(r.end)}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Submission Status</div>
        <div class="stat-number" style="font-size:22px;padding-top:8px;">${submittedTs ? submittedTs.status[0].toUpperCase() + submittedTs.status.slice(1) : 'Draft'}</div>
        <div class="stat-sub">${submittedTs && submittedTs.reviewedAt ? 'Reviewed ' + fmtDateShort(submittedTs.reviewedAt) : submittedTs && submittedTs.submittedAt ? 'Submitted ' + fmtDateShort(submittedTs.submittedAt) : 'Not yet submitted'}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Approver</div>
        <div class="stat-number" style="font-size:22px;padding-top:8px;">${(() => {
          const mgr = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
          return mgr ? mgr.name.split(' ')[0] : 'HR';
        })()}</div>
        <div class="stat-sub">${(() => {
          const mgr = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
          return mgr ? mgr.position : 'No manager assigned';
        })()}</div>
      </div>
    </div>

    <div style="margin-top: 24px;">
      <div class="card">
        <div class="card-title">Recent Time Entries</div>
        <div class="card-subtitle">From your clock-in/out</div>
        ${renderTimeEntriesTable(DB.timeEntries.filter(e => e.userId === u.id).slice().sort((a,b) => b.clockIn.localeCompare(a.clockIn)).slice(0, 10), false)}
      </div>
    </div>
  `;
}

function setKronosWeek(offset) {
  kronosWeekOffset = offset;
  renderView();
}

function recalcKronos() {
  renderView();
  showToast('Totals recalculated', 'success');
}

function saveKronosWeek() {
  showToast('Timecard saved', 'success');
}

function kronosAddPunch(date) {
  showToast('Use Clock In/Out to add a punch, or HR to manually add', 'success');
}

function kronosClearDay(date) {
  if (!confirm('Remove all punches for ' + fmtDate(date) + '?')) return;
  const u = currentUser();
  DB.timeEntries = DB.timeEntries.filter(e => !(e.userId === u.id && e.clockIn.slice(0,10) === date));
  saveDB();
  renderView();
  showToast('Day cleared', 'success');
}

function submitTimesheet() {
  const u = currentUser();
  const r = getWeekRange(kronosWeekOffset);
  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(r.start + 'T12:00:00');
    d.setDate(d.getDate() + i);
    days.push(d.toISOString().slice(0,10));
  }
  // Build entries from existing punches
  const entries = days.map(date => {
    const dayEntries = DB.timeEntries.filter(e => e.userId === u.id && e.clockIn.slice(0,10) === date).sort((a,b) => a.clockIn.localeCompare(b.clockIn));
    return {
      date,
      in1: dayEntries[0] ? dayEntries[0].clockIn.slice(11,16) : '',
      out1: dayEntries[0] && dayEntries[0].clockOut ? dayEntries[0].clockOut.slice(11,16) : '',
      in2: dayEntries[1] ? dayEntries[1].clockIn.slice(11,16) : '',
      out2: dayEntries[1] && dayEntries[1].clockOut ? dayEntries[1].clockOut.slice(11,16) : '',
      payCode: (dayEntries[0] || dayEntries[1]) ? 'Regular' : 'Off',
      notes: ''
    };
  });
  // Check if existing submission for this week
  let ts = DB.timesheets.find(t => t.userId === u.id && t.weekStart === r.start);
  if (ts) {
    ts.entries = entries;
    ts.status = 'pending';
    ts.submittedAt = new Date().toISOString();
    ts.reviewedBy = null;
    ts.reviewedAt = null;
    ts.reviewNote = '';
    showToast('Timesheet re-submitted for approval', 'success');
  } else {
    DB.timesheets.push({
      id: uid('ws'),
      userId: u.id,
      weekStart: r.start,
      entries,
      status: 'pending',
      submittedAt: new Date().toISOString(),
      reviewedBy: null,
      reviewedAt: null,
      reviewNote: ''
    });
    showToast('Timesheet submitted to ' + (() => {
      const mgr = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
      return mgr ? mgr.name : 'HR';
    })() + ' for approval', 'success');
  }
  saveDB();
  renderView();
}

function fmtTime12(hm) {
  if (!hm) return '';
  const [h, m] = hm.split(':');
  const hour = parseInt(h);
  const period = hour >= 12 ? 'PM' : 'AM';
  const dh = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
  return dh + ':' + m + ' ' + period;
}

function exportMyTime() {
  const u = currentUser();
  const entries = DB.timeEntries.filter(e => e.userId === u.id).sort((a,b) => a.clockIn.localeCompare(b.clockIn));
  const rows = entries.map(e => {
    const out = e.clockOut ? new Date(e.clockOut) : null;
    return {
      Date: e.clockIn.slice(0,10),
      Day: fmtDay(e.clockIn),
      'Clock In': fmtTime(e.clockIn),
      'Clock Out': out ? fmtTime(e.clockOut) : 'In progress',
      'Hours': out ? ((out - new Date(e.clockIn)) / 3600000).toFixed(2) : '',
      Note: e.note || '',
      Edited: e.edited ? 'Yes' : ''
    };
  });
  downloadExcel(rows, 'My_Timesheet_' + u.name.replace(/\s/g, '_') + '_' + todayISO() + '.xlsx', 'Timesheet');
}

// ============ VIEW: SCHEDULE ============
let calMonth = null; // YYYY-MM
function renderSchedule(host) {
  const u = currentUser();
  if (!calMonth) calMonth = todayISO().slice(0, 7);
  const [yr, mo] = calMonth.split('-').map(Number);
  const firstOfMonth = new Date(yr, mo - 1, 1);
  const lastOfMonth = new Date(yr, mo, 0);
  const startDow = firstOfMonth.getDay();
  const daysInMonth = lastOfMonth.getDate();
  const prevMonthDays = new Date(yr, mo - 1, 0).getDate();

  const dayNames = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  let cells = [];

  // Leading days (previous month)
  for (let i = startDow - 1; i >= 0; i--) {
    const d = new Date(yr, mo - 2, prevMonthDays - i);
    cells.push({ date: d, otherMonth: true });
  }
  for (let i = 1; i <= daysInMonth; i++) {
    cells.push({ date: new Date(yr, mo - 1, i), otherMonth: false });
  }
  while (cells.length % 7 !== 0) {
    const last = cells[cells.length - 1].date;
    cells.push({ date: new Date(last.getTime() + 86400000), otherMonth: true });
  }

  function isoOf(d) { return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0'); }
  const todayIso = todayISO();

  const myShifts = DB.shifts.filter(s => s.userId === u.id);
  const myTimeOff = DB.timeOff.filter(t => t.userId === u.id && t.status !== 'denied');
  const myTastings = u.tastingAccess || u.role === 'admin' ? DB.tastings : [];

  function eventsFor(iso) {
    const ev = [];
    myShifts.filter(s => s.date === iso).forEach(s =>
      ev.push({ type: 'shift', label: fmtTimeRange(s.start, s.end) + ' ' + s.position }));
    myTimeOff.filter(t => iso >= t.startDate && iso <= t.endDate).forEach(t =>
      ev.push({ type: 'timeoff', label: (t.status === 'pending' ? '⏳ ' : '✓ ') + t.type }));
    if (u.tastingAccess || u.role === 'admin') {
      myTastings.filter(tt => tt.date === iso).slice(0, 3).forEach(tt =>
        ev.push({ type: 'tasting', label: '🍷 ' + (tt.location || 'Tasting') }));
    }
    return ev;
  }

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">My Schedule</div>
        <div class="page-subtitle">Shifts, time off, and tastings</div>
      </div>
      <div class="page-actions">
        <button class="btn btn-gold" onclick="exportMySchedule()">📥 Export Schedule</button>
      </div>
    </div>

    <div class="cal-header">
      <div class="cal-month">${firstOfMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</div>
      <div class="cal-nav">
        <button class="btn btn-secondary btn-sm" onclick="changeMonth(-1)">‹ Prev</button>
        <button class="btn btn-secondary btn-sm" onclick="changeMonth(0)">Today</button>
        <button class="btn btn-secondary btn-sm" onclick="changeMonth(1)">Next ›</button>
      </div>
    </div>

    <div class="cal-grid">
      ${dayNames.map(d => `<div class="cal-day-name">${d}</div>`).join('')}
      ${cells.map(c => {
        const iso = isoOf(c.date);
        const ev = eventsFor(iso);
        return `
          <div class="cal-day ${c.otherMonth ? 'other-month' : ''} ${iso === todayIso ? 'today' : ''}">
            <div class="cal-day-num">${c.date.getDate()}</div>
            ${ev.map(e => `<div class="cal-event ${e.type}" title="${escapeHtml(e.label)}">${escapeHtml(e.label)}</div>`).join('')}
          </div>
        `;
      }).join('')}
    </div>

    <div class="grid grid-2" style="margin-top: 24px;">
      <div class="card">
        <div class="card-title">Upcoming Shifts</div>
        <div class="card-subtitle">Your scheduled work in the coming weeks</div>
        ${(() => {
          const upcoming = myShifts.filter(s => s.date >= todayIso).sort((a,b) => a.date.localeCompare(b.date)).slice(0, 8);
          if (upcoming.length === 0) return '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No upcoming shifts.</div>';
          return upcoming.map(s => `
            <div style="padding: 10px 0; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between;">
              <div>
                <div style="font-weight: 600;">${fmtDay(s.date)}, ${fmtDate(s.date)}</div>
                <div style="font-size: 12px; color: var(--slate);">${escapeHtml(s.position)}</div>
              </div>
              <div style="color: var(--burgundy); font-weight: 600;">${fmtTimeRange(s.start, s.end)}</div>
            </div>
          `).join('');
        })()}
      </div>
      <div class="card">
        <div class="card-title">Time Off</div>
        <div class="card-subtitle">Your requests and approved leave</div>
        ${(() => {
          const recent = DB.timeOff.filter(t => t.userId === u.id).sort((a,b) => b.startDate.localeCompare(a.startDate)).slice(0, 5);
          if (recent.length === 0) return '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No time-off requests.</div>';
          return recent.map(t => `
            <div style="padding: 10px 0; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items:center;">
              <div>
                <div style="font-weight: 600;">${escapeHtml(t.type)}</div>
                <div style="font-size: 12px; color: var(--slate);">${fmtDateShort(t.startDate)} – ${fmtDateShort(t.endDate)}</div>
              </div>
              <span class="badge ${t.status === 'approved' ? 'badge-success' : t.status === 'denied' ? 'badge-danger' : 'badge-warning'}">${t.status}</span>
            </div>
          `).join('');
        })()}
      </div>
    </div>
  `;
}

function changeMonth(dir) {
  if (dir === 0) {
    calMonth = todayISO().slice(0, 7);
  } else {
    const [yr, mo] = calMonth.split('-').map(Number);
    const d = new Date(yr, mo - 1 + dir, 1);
    calMonth = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0');
  }
  renderView();
}

function exportMySchedule() {
  const u = currentUser();
  const myShifts = DB.shifts.filter(s => s.userId === u.id).sort((a,b) => a.date.localeCompare(b.date));
  const rows = myShifts.map(s => ({
    Date: s.date, Day: fmtDay(s.date), Start: s.start, End: s.end, Position: s.position, Notes: s.notes
  }));
  downloadExcel(rows, 'My_Schedule_' + u.name.replace(/\s/g, '_') + '_' + todayISO() + '.xlsx', 'Schedule');
}

// ============ VIEW: ANNOUNCEMENTS ============
function renderAnnouncements(host) {
  const u = currentUser();
  const isAdminUser = u.role === 'admin';
  const sorted = [...DB.announcements].sort((a, b) => {
    if (a.pinned !== b.pinned) return b.pinned - a.pinned;
    return b.createdAt.localeCompare(a.createdAt);
  });

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Announcements</div>
        <div class="page-subtitle">News and notes from management</div>
      </div>
      ${isAdminUser ? '<div class="page-actions"><button class="btn btn-primary" onclick="openAnnouncementModal()">＋ New Announcement</button></div>' : ''}
    </div>

    ${sorted.length === 0
      ? '<div class="card"><div class="empty"><div class="empty-icon">📣</div><div>No announcements yet.</div></div></div>'
      : sorted.map(a => {
        const author = DB.users.find(x => x.id === a.authorId);
        return `
          <div class="announcement ${a.pinned ? 'pinned' : ''}">
            <div class="announcement-meta">
              <div class="announcement-title">${a.pinned ? '<span class="pin-marker">📌</span>' : ''}${escapeHtml(a.title)}</div>
              <div class="announcement-date">${fmtDate(a.createdAt)}</div>
            </div>
            <div class="announcement-body">${escapeHtml(a.body)}</div>
            <div class="announcement-author">— ${escapeHtml(author ? author.name : 'Unknown')}, ${escapeHtml(author ? author.position : '')}</div>
            ${isAdminUser ? `
              <div style="margin-top: 10px; display: flex; gap: 8px;">
                <button class="btn btn-sm btn-ghost" onclick="togglePin('${a.id}')">${a.pinned ? '📌 Unpin' : '📍 Pin'}</button>
                <button class="btn btn-sm btn-ghost" onclick="editAnnouncement('${a.id}')">Edit</button>
                <button class="btn btn-sm btn-ghost" onclick="deleteAnnouncement('${a.id}')" style="color: var(--danger);">Delete</button>
              </div>` : ''}
          </div>
        `;
      }).join('')}
  `;
}

function openAnnouncementModal(id) {
  const ann = id ? DB.announcements.find(a => a.id === id) : null;
  showModal({
    title: ann ? 'Edit Announcement' : 'New Announcement',
    body: `
      <form id="announcement-form" onsubmit="saveAnnouncement(event, '${id || ''}')">
        <div class="field"><label class="label">Title</label><input id="ann-title" required value="${ann ? escapeHtml(ann.title) : ''}" placeholder="Title"></div>
        <div class="field" style="margin-top:14px;"><label class="label">Message</label><textarea id="ann-body" required rows="6" placeholder="Write your announcement...">${ann ? escapeHtml(ann.body) : ''}</textarea></div>
        <label style="display:flex; align-items:center; gap:8px; margin-top:14px;"><input type="checkbox" id="ann-pinned" style="width:auto;" ${ann && ann.pinned ? 'checked' : ''}> <span style="font-size:13px;">Pin this announcement to the top</span></label>
      </form>
    `,
    submitLabel: 'Save Announcement',
    submitFn: () => document.getElementById('announcement-form').requestSubmit()
  });
}

function saveAnnouncement(e, id) {
  e.preventDefault();
  const title = document.getElementById('ann-title').value.trim();
  const body = document.getElementById('ann-body').value.trim();
  const pinned = document.getElementById('ann-pinned').checked;
  if (id) {
    const a = DB.announcements.find(x => x.id === id);
    if (a) { a.title = title; a.body = body; a.pinned = pinned; }
    showToast('Announcement updated', 'success');
  } else {
    DB.announcements.push({
      id: uid('an'), title, body, authorId: currentUser().id,
      createdAt: new Date().toISOString(), pinned
    });
    showToast('Announcement posted', 'success');
  }
  saveDB();
  closeModal();
  renderView();
}

function editAnnouncement(id) { openAnnouncementModal(id); }
function deleteAnnouncement(id) {
  if (!confirm('Delete this announcement?')) return;
  DB.announcements = DB.announcements.filter(a => a.id !== id);
  saveDB();
  showToast('Announcement deleted', 'success');
  renderView();
}
function togglePin(id) {
  const a = DB.announcements.find(x => x.id === id);
  if (a) { a.pinned = !a.pinned; saveDB(); renderView(); }
}

// ============ VIEW: TIME OFF ============
function renderTimeOff(host) {
  const u = currentUser();
  const myRequests = DB.timeOff.filter(t => t.userId === u.id).sort((a, b) => b.startDate.localeCompare(a.startDate));

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Time Off</div>
        <div class="page-subtitle">Request days off and track your requests</div>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="openTimeOffModal()">＋ Request Time Off</button>
      </div>
    </div>

    <div class="table-wrap">
      <div class="table-header">
        <div class="table-title">My Requests</div>
        <div class="table-meta">${myRequests.length} request${myRequests.length === 1 ? '' : 's'}</div>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr>
            <th>Type</th><th>Dates</th><th>Reason</th><th>Status</th><th>Reviewed</th><th></th>
          </tr></thead>
          <tbody>
            ${myRequests.length === 0
              ? '<tr><td colspan="6"><div class="empty"><div class="empty-icon">🌴</div><div>No time-off requests yet.</div></div></td></tr>'
              : myRequests.map(t => {
                const reviewer = t.reviewedBy ? DB.users.find(x => x.id === t.reviewedBy) : null;
                return `
                  <tr>
                    <td><strong>${escapeHtml(t.type)}</strong></td>
                    <td>${fmtDateShort(t.startDate)} – ${fmtDateShort(t.endDate)}</td>
                    <td style="max-width: 240px;">${escapeHtml(t.reason || '—')}</td>
                    <td><span class="badge ${t.status === 'approved' ? 'badge-success' : t.status === 'denied' ? 'badge-danger' : 'badge-warning'}">${t.status}</span></td>
                    <td style="font-size: 12px; color: var(--slate);">
                      ${reviewer ? escapeHtml(reviewer.name) + '<br>' + fmtDateShort(t.reviewedAt) : '—'}
                      ${t.reviewNote ? '<br><em>"' + escapeHtml(t.reviewNote) + '"</em>' : ''}
                    </td>
                    <td>${t.status === 'pending' ? `<button class="btn btn-sm btn-ghost" onclick="cancelTimeOff('${t.id}')" style="color:var(--danger);">Cancel</button>` : ''}</td>
                  </tr>
                `;
              }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function openTimeOffModal() {
  showModal({
    title: 'Request Time Off',
    body: `
      <form id="timeoff-form" onsubmit="saveTimeOff(event)">
        <div class="form-grid">
          <div class="field"><label class="label">Type</label>
            <select id="to-type" required>
              <option>Vacation</option><option>Sick</option><option>Personal</option><option>Bereavement</option><option>Jury Duty</option><option>Other</option>
            </select>
          </div>
          <div class="field"><label class="label">Start Date</label><input type="date" id="to-start" required></div>
          <div class="field"><label class="label">End Date</label><input type="date" id="to-end" required></div>
          <div class="field full"><label class="label">Reason / Notes</label><textarea id="to-reason" rows="3" placeholder="Optional details..."></textarea></div>
        </div>
      </form>
    `,
    submitLabel: 'Submit Request',
    submitFn: () => document.getElementById('timeoff-form').requestSubmit()
  });
}

function saveTimeOff(e) {
  e.preventDefault();
  const u = currentUser();
  DB.timeOff.push({
    id: uid('to'),
    userId: u.id,
    startDate: document.getElementById('to-start').value,
    endDate: document.getElementById('to-end').value,
    type: document.getElementById('to-type').value,
    reason: document.getElementById('to-reason').value.trim(),
    status: 'pending',
    reviewedBy: null, reviewedAt: null, reviewNote: ''
  });
  saveDB();
  closeModal();
  showToast('Request submitted', 'success');
  renderView();
}

function cancelTimeOff(id) {
  if (!confirm('Cancel this request?')) return;
  DB.timeOff = DB.timeOff.filter(t => t.id !== id);
  saveDB();
  renderView();
  showToast('Request cancelled', 'success');
}

// ============ VIEW: TASTINGS (Portia-specific) ============
let tastingSort = 'date', tastingDir = 'asc';
function renderTastings(host) {
  const u = currentUser();
  if (!u.tastingAccess && u.role !== 'admin') {
    host.innerHTML = '<div class="card"><div class="empty"><div class="empty-icon">🔒</div><div>You don\'t have access to this section.</div></div></div>';
    return;
  }
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">🍷 Tasting Schedule</div>
        <div class="page-subtitle">Manage and export upcoming tastings</div>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="openTastingModal()">＋ Add Tasting</button>
        <button class="btn btn-gold" onclick="exportTastings('this')">📥 This Week</button>
        <button class="btn btn-gold" onclick="exportTastings('next')">📥 Next Week</button>
        <button class="btn btn-outline" onclick="openExportTastingLocation()">📍 By Location</button>
      </div>
    </div>

    <div class="grid grid-4" style="margin-bottom: 24px;">
      ${(() => {
        const today = todayISO(); const wk = getWeekRange(); const nk = getWeekRange(1);
        const todayCt = DB.tastings.filter(t => t.date === today).length;
        const weekCt = DB.tastings.filter(t => t.date >= wk.start && t.date <= wk.end && t.date >= today).length;
        const nextCt = DB.tastings.filter(t => t.date >= nk.start && t.date <= nk.end).length;
        const total = DB.tastings.length;
        return `
          <div class="stat-card"><div class="stat-label">Today</div><div class="stat-number">${todayCt}</div><div class="stat-sub">tastings scheduled</div></div>
          <div class="stat-card"><div class="stat-label">This Week</div><div class="stat-number">${weekCt}</div><div class="stat-sub">remaining</div></div>
          <div class="stat-card"><div class="stat-label">Next Week</div><div class="stat-number">${nextCt}</div><div class="stat-sub">scheduled ahead</div></div>
          <div class="stat-card"><div class="stat-label">Total Tracked</div><div class="stat-number">${total}</div><div class="stat-sub">events</div></div>
        `;
      })()}
    </div>

    <div class="card" style="padding: 16px 18px; margin-bottom: 18px;">
      <div style="display: flex; gap: 12px; flex-wrap: wrap; align-items: end;">
        <div class="field" style="flex: 2; min-width: 200px;">
          <label class="label">Search</label>
          <input id="tasting-search" placeholder="Supplier, distributor, product..." oninput="renderView()">
        </div>
        <div class="field" style="flex: 1; min-width: 160px;">
          <label class="label">Location</label>
          <select id="tasting-location" onchange="renderView()">
            <option value="">All</option>
            ${[...new Set(DB.tastings.map(t => t.location).filter(Boolean))].sort().map(l => `<option>${escapeHtml(l)}</option>`).join('')}
          </select>
        </div>
        <div class="field" style="flex: 1; min-width: 140px;">
          <label class="label">Time Frame</label>
          <select id="tasting-tf" onchange="renderView()">
            <option value="upcoming">Upcoming</option>
            <option value="this-week">This Week</option>
            <option value="next-week">Next Week</option>
            <option value="this-month">This Month</option>
            <option value="past">Past</option>
            <option value="all">All Time</option>
          </select>
        </div>
      </div>
    </div>

    <div id="tasting-table"></div>
  `;
  renderTastingTable();
}

function renderTastingTable() {
  const u = currentUser();
  const search = (document.getElementById('tasting-search')?.value || '').toLowerCase().trim();
  const loc = document.getElementById('tasting-location')?.value || '';
  const tf = document.getElementById('tasting-tf')?.value || 'upcoming';
  const today = todayISO(); const wk = getWeekRange(); const nk = getWeekRange(1);

  let items = DB.tastings.filter(t => {
    if (loc && t.location !== loc) return false;
    if (tf === 'upcoming' && t.date < today) return false;
    if (tf === 'this-week' && (t.date < wk.start || t.date > wk.end)) return false;
    if (tf === 'next-week' && (t.date < nk.start || t.date > nk.end)) return false;
    if (tf === 'past' && t.date >= today) return false;
    if (tf === 'this-month' && !t.date.startsWith(today.slice(0,7))) return false;
    if (search) {
      const hay = (t.location + ' ' + t.distributor + ' ' + t.supplier + ' ' + t.rep + ' ' + (t.products || []).join(' ')).toLowerCase();
      if (!hay.includes(search)) return false;
    }
    return true;
  });

  items.sort((a, b) => {
    const av = a[tastingSort] || ''; const bv = b[tastingSort] || '';
    if (av < bv) return tastingDir === 'asc' ? -1 : 1;
    if (av > bv) return tastingDir === 'asc' ? 1 : -1;
    return (a.from || '').localeCompare(b.from || '');
  });

  const host = document.getElementById('tasting-table');
  host.innerHTML = `
    <div class="table-wrap">
      <div class="table-header">
        <div class="table-title">Scheduled Tastings</div>
        <div class="table-meta">${items.length} event${items.length === 1 ? '' : 's'}</div>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr>
            <th>Date</th><th>Day</th><th>Time</th><th>Location</th>
            <th>Distributor</th><th>Supplier</th><th>Rep</th><th>Products</th>
            <th>Status</th><th></th>
          </tr></thead>
          <tbody>
            ${items.length === 0
              ? '<tr><td colspan="10"><div class="empty"><div class="empty-icon">🍇</div><div>No tastings match your filters.</div></div></td></tr>'
              : items.map(t => {
                const status = (() => {
                  if (t.date === today) return { label: 'Today', cls: 'badge-gold' };
                  if (t.date >= wk.start && t.date <= wk.end && t.date > today) return { label: 'This Week', cls: 'badge-warning' };
                  if (t.date >= nk.start && t.date <= nk.end) return { label: 'Next Week', cls: 'badge-info' };
                  if (t.date < today) return { label: 'Past', cls: 'badge-muted' };
                  return { label: 'Upcoming', cls: 'badge-muted' };
                })();
                const products = (t.products || []).filter(p => p);
                return `
                  <tr>
                    <td style="white-space:nowrap;font-weight:600;color:var(--burgundy-dark);">${fmtDate(t.date)}</td>
                    <td style="font-style:italic;color:var(--slate);">${escapeHtml(t.day || fmtDay(t.date))}</td>
                    <td style="white-space:nowrap;">${fmtTimeRange(t.from, t.to)}</td>
                    <td><strong>${escapeHtml(t.location)}</strong></td>
                    <td>${escapeHtml(t.distributor) || '—'}</td>
                    <td>${escapeHtml(t.supplier) || '—'}</td>
                    <td>${escapeHtml(t.rep) || '—'}</td>
                    <td style="max-width:280px;">${products.map(p => '<span class="product-pill">' + escapeHtml(p) + '</span>').join(' ') || '—'}</td>
                    <td><span class="badge ${status.cls}">${status.label}</span></td>
                    <td><button class="btn btn-sm btn-ghost" onclick="openTastingModal('${t.id}')">Edit</button> <button class="btn btn-sm btn-ghost" onclick="deleteTasting('${t.id}')" style="color:var(--danger);">×</button></td>
                  </tr>
                `;
              }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function openTastingModal(id) {
  const t = id ? DB.tastings.find(x => x.id === id) : null;
  const locations = [...new Set(DB.tastings.map(x => x.location).filter(Boolean))].sort();
  const distributors = [...new Set(DB.tastings.map(x => x.distributor).filter(Boolean))].sort();
  showModal({
    title: t ? 'Edit Tasting' : 'Add Tasting',
    body: `
      <form id="tasting-form" onsubmit="saveTasting(event, '${id || ''}')">
        <div class="form-grid">
          <div class="field"><label class="label">Date</label><input type="date" id="t-date" required value="${t ? t.date : todayISO()}"></div>
          <div class="field"><label class="label">Location</label>
            <input id="t-location" list="t-loc-list" required value="${t ? escapeHtml(t.location) : ''}">
            <datalist id="t-loc-list">${locations.map(l => `<option>${escapeHtml(l)}</option>`).join('')}</datalist>
          </div>
          <div class="field"><label class="label">From</label><input type="time" id="t-from" required value="${t ? t.from : ''}"></div>
          <div class="field"><label class="label">To</label><input type="time" id="t-to" required value="${t ? t.to : ''}"></div>
          <div class="field"><label class="label">Distributor</label>
            <input id="t-distributor" list="t-dist-list" value="${t ? escapeHtml(t.distributor) : ''}">
            <datalist id="t-dist-list">${distributors.map(l => `<option>${escapeHtml(l)}</option>`).join('')}</datalist>
          </div>
          <div class="field"><label class="label">Supplier</label><input id="t-supplier" value="${t ? escapeHtml(t.supplier) : ''}"></div>
          <div class="field full"><label class="label">Rep Contacted By</label><input id="t-rep" value="${t ? escapeHtml(t.rep) : ''}"></div>
        </div>
        <div style="margin-top:16px; padding-top:14px; border-top:1px solid var(--border);">
          <label class="label">Products (up to 6)</label>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px;">
            ${[0,1,2,3,4,5].map(i => `<input id="t-p${i+1}" placeholder="Product #${i+1}" value="${t && t.products && t.products[i] ? escapeHtml(t.products[i]) : ''}">`).join('')}
          </div>
        </div>
      </form>
    `,
    submitLabel: 'Save Tasting',
    submitFn: () => document.getElementById('tasting-form').requestSubmit(),
    large: true
  });
}

function saveTasting(e, id) {
  e.preventDefault();
  const products = [];
  for (let i = 1; i <= 6; i++) {
    const v = document.getElementById('t-p' + i).value.trim();
    if (v) products.push(v);
  }
  const data = {
    id: id || uid('t'),
    date: document.getElementById('t-date').value,
    day: fmtDay(document.getElementById('t-date').value),
    from: document.getElementById('t-from').value,
    to: document.getElementById('t-to').value,
    location: document.getElementById('t-location').value.trim(),
    distributor: document.getElementById('t-distributor').value.trim(),
    supplier: document.getElementById('t-supplier').value.trim(),
    rep: document.getElementById('t-rep').value.trim(),
    products
  };
  if (id) {
    const idx = DB.tastings.findIndex(x => x.id === id);
    if (idx >= 0) DB.tastings[idx] = data;
    showToast('Tasting updated', 'success');
  } else {
    DB.tastings.push(data);
    showToast('Tasting added', 'success');
  }
  saveDB();
  closeModal();
  renderView();
}

function deleteTasting(id) {
  const t = DB.tastings.find(x => x.id === id);
  if (!t) return;
  if (!confirm('Delete tasting on ' + fmtDate(t.date) + ' at ' + t.location + '?')) return;
  DB.tastings = DB.tastings.filter(x => x.id !== id);
  saveDB();
  renderView();
  showToast('Tasting deleted', 'success');
}

function exportTastings(which) {
  const r = which === 'this' ? getWeekRange(0) : getWeekRange(1);
  const items = DB.tastings.filter(t => t.date >= r.start && t.date <= r.end).sort((a,b) => (a.date + a.from).localeCompare(b.date + b.from));
  if (items.length === 0) { showToast('No tastings in range', 'error'); return; }
  const rows = items.map(t => ({
    'Date': t.date, 'Day': t.day || fmtDay(t.date), 'Location': t.location,
    'From': t.from, 'To': t.to, 'Distributor': t.distributor, 'Supplier': t.supplier,
    'Rep Contacted By': t.rep,
    'Product #1': (t.products||[])[0]||'', 'Product #2': (t.products||[])[1]||'',
    'Product #3': (t.products||[])[2]||'', 'Product #4': (t.products||[])[3]||'',
    'Product #5': (t.products||[])[4]||'', 'Product #6': (t.products||[])[5]||''
  }));
  downloadExcel(rows, `Tastings_${which === 'this' ? 'This' : 'Next'}_Week_${r.start}.xlsx`, which === 'this' ? 'This Week' : 'Next Week');
}

function openExportTastingLocation() {
  const locations = [...new Set(DB.tastings.map(t => t.location).filter(Boolean))].sort();
  showModal({
    title: 'Export Tastings by Location',
    body: `
      <p style="color: var(--slate); margin-bottom: 14px; font-style: italic;">Choose location(s) and optional date range.</p>
      <div id="loc-cb-list" style="max-height: 260px; overflow-y: auto; border: 1px solid var(--border); border-radius: 10px; padding: 8px; background: var(--cream);">
        ${locations.map(l => `<label style="display:flex; align-items:center; gap:8px; padding: 6px 10px; border-radius:6px; cursor:pointer;"><input type="checkbox" value="${escapeHtml(l)}" checked style="width:auto;"> ${escapeHtml(l)}</label>`).join('')}
      </div>
      <div style="margin-top: 14px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <div class="field"><label class="label">From</label><input type="date" id="loc-from"></div>
        <div class="field"><label class="label">To</label><input type="date" id="loc-to"></div>
      </div>
    `,
    submitLabel: 'Export',
    submitFn: () => {
      const checked = [...document.querySelectorAll('#loc-cb-list input:checked')].map(c => c.value);
      const from = document.getElementById('loc-from').value;
      const to = document.getElementById('loc-to').value;
      if (checked.length === 0) { showToast('Select at least one location', 'error'); return; }
      let items = DB.tastings.filter(t => checked.includes(t.location));
      if (from) items = items.filter(t => t.date >= from);
      if (to) items = items.filter(t => t.date <= to);
      items.sort((a,b) => (a.date + a.from).localeCompare(b.date + b.from));
      if (items.length === 0) { showToast('No tastings match', 'error'); return; }
      const rows = items.map(t => ({
        'Date': t.date, 'Day': t.day || fmtDay(t.date), 'Location': t.location,
        'From': t.from, 'To': t.to, 'Distributor': t.distributor, 'Supplier': t.supplier,
        'Rep Contacted By': t.rep,
        'Product #1': (t.products||[])[0]||'', 'Product #2': (t.products||[])[1]||'',
        'Product #3': (t.products||[])[2]||'', 'Product #4': (t.products||[])[3]||'',
        'Product #5': (t.products||[])[4]||'', 'Product #6': (t.products||[])[5]||''
      }));
      const label = checked.length === 1 ? checked[0].replace(/[^a-z0-9]/gi,'_') : checked.length + '_locations';
      downloadExcel(rows, `Tastings_${label}_${todayISO()}.xlsx`, 'Tastings');
      closeModal();
    }
  });
}

// ============ VIEW: HR — EMPLOYEES ============
function renderEmployees(host) {
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Employees</div>
        <div class="page-subtitle">Manage team accounts and permissions</div>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="openEmployeeModal()">＋ Add Employee</button>
      </div>
    </div>
    <div class="table-wrap">
      <div class="table-header">
        <div class="table-title">Team</div>
        <div class="table-meta">${DB.users.filter(u => u.active).length} active</div>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr>
            <th>Name</th><th>Email</th><th>Position</th><th>Department</th><th>Reports To</th><th>Role</th><th>Tasting</th><th>Status</th><th></th>
          </tr></thead>
          <tbody>
            ${DB.users.map(u => {
              const mgr = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
              return `
              <tr>
                <td><div style="display:flex; align-items:center; gap:10px;"><div class="avatar" style="width:32px;height:32px;font-size:12px;">${initials(u.name)}</div><strong>${escapeHtml(u.name)}</strong></div></td>
                <td style="color:var(--slate);font-size:12px;">${escapeHtml(u.email)}</td>
                <td>${escapeHtml(u.position)}</td>
                <td>${u.department ? `<span class="badge" style="background:var(--gold-light);color:var(--burgundy-dark);">${escapeHtml(u.department)}</span>` : '<span style="color:var(--warm-gray);">—</span>'}</td>
                <td style="font-size:13px;">${mgr ? escapeHtml(mgr.name) : '<span style="color:var(--warm-gray);">—</span>'}</td>
                <td><span class="badge ${u.role === 'admin' ? 'badge-gold' : 'badge-muted'}">${u.role}</span></td>
                <td>${u.tastingAccess ? '<span class="badge badge-success">Yes</span>' : '<span style="color:var(--warm-gray);">—</span>'}</td>
                <td>${u.active ? '<span class="badge badge-success">Active</span>' : '<span class="badge badge-muted">Inactive</span>'}</td>
                <td>
                  <button class="btn btn-sm btn-ghost" onclick="openEmployeeModal('${u.id}')">Edit</button>
                  ${u.id !== currentUser().id ? `<button class="btn btn-sm btn-ghost" onclick="toggleActive('${u.id}')" style="color:var(--danger);">${u.active ? 'Deactivate' : 'Activate'}</button>` : ''}
                </td>
              </tr>
            `;}).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function openEmployeeModal(id) {
  const u = id ? DB.users.find(x => x.id === id) : null;
  const departments = [...new Set(DB.users.map(x => x.department).filter(Boolean))].sort();
  const candidateMgrs = DB.users.filter(x => x.active && (!id || x.id !== id));
  showModal({
    title: u ? 'Edit Employee' : 'Add Employee',
    body: `
      <form id="emp-form" onsubmit="saveEmployee(event, '${id || ''}')">
        <div class="form-grid">
          <div class="field full"><label class="label">Full Name</label><input id="e-name" required value="${u ? escapeHtml(u.name) : ''}"></div>
          <div class="field"><label class="label">Email</label><input type="email" id="e-email" required value="${u ? escapeHtml(u.email) : ''}"></div>
          <div class="field"><label class="label">Password ${u ? '(leave blank to keep)' : ''}</label><input id="e-password" ${u ? '' : 'required'} placeholder="${u ? '••••••••' : 'Min 6 chars'}"></div>
          <div class="field"><label class="label">Position / Title</label><input id="e-position" required value="${u ? escapeHtml(u.position) : ''}" placeholder="e.g. Data Analyst"></div>
          <div class="field"><label class="label">Department</label>
            <input id="e-department" list="dept-list" value="${u ? escapeHtml(u.department || '') : ''}" placeholder="e.g. Operations">
            <datalist id="dept-list">${departments.map(d => `<option>${escapeHtml(d)}</option>`).join('')}</datalist>
          </div>
          <div class="field"><label class="label">Role</label>
            <select id="e-role">
              <option value="employee" ${u && u.role === 'employee' ? 'selected' : ''}>Employee</option>
              <option value="admin" ${u && u.role === 'admin' ? 'selected' : ''}>HR / Admin</option>
            </select>
          </div>
          <div class="field"><label class="label">Reports To (Manager)</label>
            <select id="e-manager">
              <option value="">— No manager (top of org) —</option>
              ${candidateMgrs.map(m => `<option value="${m.id}" ${u && u.managerId === m.id ? 'selected' : ''}>${escapeHtml(m.name)} (${escapeHtml(m.position)})</option>`).join('')}
            </select>
          </div>
          <div class="field full">
            <label style="display:flex; align-items:center; gap:8px;"><input type="checkbox" id="e-tasting" style="width:auto;" ${u && u.tastingAccess ? 'checked' : ''}> <span>Grant Tasting Schedule access</span></label>
          </div>
        </div>
      </form>
    `,
    submitLabel: 'Save Employee',
    submitFn: () => document.getElementById('emp-form').requestSubmit(),
    large: true
  });
}



function saveEmployee(e, id) {
  e.preventDefault();
  const data = {
    name: document.getElementById('e-name').value.trim(),
    email: document.getElementById('e-email').value.trim(),
    position: document.getElementById('e-position').value.trim(),
    department: document.getElementById('e-department').value.trim(),
    role: document.getElementById('e-role').value,
    managerId: document.getElementById('e-manager').value || null,
    tastingAccess: document.getElementById('e-tasting').checked
  };
  if (id && data.managerId) {
    let m = data.managerId;
    while (m) {
      if (m === id) { showToast('Cannot create circular reporting', 'error'); return; }
      const mgr = DB.users.find(x => x.id === m);
      m = mgr ? mgr.managerId : null;
    }
  }
  const pw = document.getElementById('e-password').value;
  if (id) {
    const u = DB.users.find(x => x.id === id);
    if (u) { Object.assign(u, data); if (pw) u.password = pw; }
    showToast('Employee updated', 'success');
  } else {
    if (DB.users.find(u => u.email.toLowerCase() === data.email.toLowerCase())) {
      showToast('Email already in use', 'error'); return;
    }
    DB.users.push({ ...data, id: uid('u'), password: pw, active: true, createdAt: todayISO() });
    showToast('Employee added', 'success');
  }
  saveDB();
  closeModal();
  renderView();
}

function toggleActive(id) {
  const u = DB.users.find(x => x.id === id);
  if (!u) return;
  u.active = !u.active;
  saveDB();
  renderView();
  showToast(u.active ? 'Activated' : 'Deactivated', 'success');
}

// ============ HR: ALL TIME RECORDS ============
let allTimeFilter = { userId: '', dateFrom: '', dateTo: '' };
function renderAllTime(host) {
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Time Records</div>
        <div class="page-subtitle">All employees - view, edit, export hours</div>
      </div>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="openTimeEntryModal()">+ Add Entry</button>
        <button class="btn btn-gold" onclick="exportAllTime()">Export Filtered</button>
      </div>
    </div>
    <div class="card" style="padding:16px 18px; margin-bottom:18px;">
      <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:end;">
        <div class="field" style="flex:1; min-width:180px;"><label class="label">Employee</label>
          <select id="alltime-user" onchange="updateAllTimeFilter()">
            <option value="">All employees</option>
            ${DB.users.filter(u => u.active).map(u => `<option value="${u.id}" ${allTimeFilter.userId === u.id ? 'selected' : ''}>${escapeHtml(u.name)}</option>`).join('')}
          </select>
        </div>
        <div class="field"><label class="label">From</label><input type="date" id="alltime-from" value="${allTimeFilter.dateFrom}" onchange="updateAllTimeFilter()"></div>
        <div class="field"><label class="label">To</label><input type="date" id="alltime-to" value="${allTimeFilter.dateTo}" onchange="updateAllTimeFilter()"></div>
        <button class="btn btn-secondary" onclick="resetAllTimeFilter()">Reset</button>
      </div>
    </div>
    <div id="alltime-list"></div>
  `;
  renderAllTimeList();
}
function updateAllTimeFilter() {
  allTimeFilter.userId = document.getElementById('alltime-user').value;
  allTimeFilter.dateFrom = document.getElementById('alltime-from').value;
  allTimeFilter.dateTo = document.getElementById('alltime-to').value;
  renderAllTimeList();
}
function resetAllTimeFilter() { allTimeFilter = { userId: '', dateFrom: '', dateTo: '' }; renderView(); }
function getFilteredEntries() {
  return DB.timeEntries.filter(e => {
    if (allTimeFilter.userId && e.userId !== allTimeFilter.userId) return false;
    const d = e.clockIn.slice(0, 10);
    if (allTimeFilter.dateFrom && d < allTimeFilter.dateFrom) return false;
    if (allTimeFilter.dateTo && d > allTimeFilter.dateTo) return false;
    return true;
  }).sort((a, b) => b.clockIn.localeCompare(a.clockIn));
}
function renderAllTimeList() {
  const entries = getFilteredEntries();
  let totalMs = 0;
  entries.forEach(e => { if (e.clockOut) totalMs += new Date(e.clockOut) - new Date(e.clockIn); });
  document.getElementById('alltime-list').innerHTML = `
    <div class="card">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
        <div>
          <div class="card-title">Filtered Records</div>
          <div class="card-subtitle">${entries.length} entries - ${(totalMs / 3600000).toFixed(2)} total hours</div>
        </div>
      </div>
      ${renderTimeEntriesTable(entries, true, true)}
    </div>
  `;
}
function openTimeEntryModal(id) {
  const e = id ? DB.timeEntries.find(x => x.id === id) : null;
  showModal({
    title: e ? 'Edit Time Entry' : 'Add Time Entry',
    body: `
      <form id="te-form" onsubmit="saveTimeEntry(event, '${id || ''}')">
        <div class="form-grid">
          <div class="field full"><label class="label">Employee</label>
            <select id="te-user" required ${e ? 'disabled' : ''}>
              <option value="">-- Select --</option>
              ${DB.users.filter(u => u.active).map(u => `<option value="${u.id}" ${e && e.userId === u.id ? 'selected' : ''}>${escapeHtml(u.name)}</option>`).join('')}
            </select>
          </div>
          <div class="field"><label class="label">Clock In Date</label><input type="date" id="te-cin-date" required value="${e ? e.clockIn.slice(0,10) : todayISO()}"></div>
          <div class="field"><label class="label">Clock In Time</label><input type="time" id="te-cin-time" required value="${e ? e.clockIn.slice(11,16) : '09:00'}"></div>
          <div class="field"><label class="label">Clock Out Date</label><input type="date" id="te-cout-date" value="${e && e.clockOut ? e.clockOut.slice(0,10) : todayISO()}"></div>
          <div class="field"><label class="label">Clock Out Time</label><input type="time" id="te-cout-time" value="${e && e.clockOut ? e.clockOut.slice(11,16) : '17:00'}"></div>
          <div class="field full"><label class="label">Note</label><input id="te-note" value="${e ? escapeHtml(e.note) : ''}" placeholder="Optional note..."></div>
        </div>
      </form>
    `,
    submitLabel: 'Save Entry',
    submitFn: () => document.getElementById('te-form').requestSubmit()
  });
}
function saveTimeEntry(e, id) {
  e.preventDefault();
  const userId = document.getElementById('te-user').value;
  const cin = document.getElementById('te-cin-date').value + 'T' + document.getElementById('te-cin-time').value + ':00';
  const coutDate = document.getElementById('te-cout-date').value;
  const coutTime = document.getElementById('te-cout-time').value;
  const cout = (coutDate && coutTime) ? coutDate + 'T' + coutTime + ':00' : null;
  const note = document.getElementById('te-note').value.trim();
  if (id) {
    const entry = DB.timeEntries.find(x => x.id === id);
    if (entry) { entry.clockIn = cin; entry.clockOut = cout; entry.note = note; entry.edited = true; entry.editedBy = currentUser().id; entry.editedAt = new Date().toISOString(); }
    showToast('Entry updated', 'success');
  } else {
    DB.timeEntries.push({ id: uid('te'), userId, clockIn: cin, clockOut: cout, note, edited: true, editedBy: currentUser().id, editedAt: new Date().toISOString() });
    showToast('Entry added', 'success');
  }
  saveDB();
  closeModal();
  renderView();
}
function editTimeEntry(id) { openTimeEntryModal(id); }
function deleteTimeEntry(id) {
  if (!confirm('Delete this entry?')) return;
  DB.timeEntries = DB.timeEntries.filter(x => x.id !== id);
  saveDB();
  renderView();
  showToast('Entry deleted', 'success');
}
function exportAllTime() {
  const entries = getFilteredEntries();
  if (entries.length === 0) { showToast('No entries to export', 'error'); return; }
  const rows = entries.map(e => {
    const u = DB.users.find(x => x.id === e.userId);
    const out = e.clockOut ? new Date(e.clockOut) : null;
    return {
      Employee: u ? u.name : '-', Email: u ? u.email : '',
      Date: e.clockIn.slice(0,10), Day: fmtDay(e.clockIn),
      'Clock In': fmtTime(e.clockIn), 'Clock Out': out ? fmtTime(e.clockOut) : 'In progress',
      Hours: out ? ((out - new Date(e.clockIn)) / 3600000).toFixed(2) : '',
      Note: e.note || '', Edited: e.edited ? 'Yes' : ''
    };
  });
  downloadExcel(rows, 'Time_Records_' + todayISO() + '.xlsx', 'Time Records');
}

// ============ HR: TIME-OFF APPROVALS ============
function renderApprovals(host) {
  const pending = DB.timeOff.filter(t => t.status === 'pending').sort((a,b) => a.startDate.localeCompare(b.startDate));
  const reviewed = DB.timeOff.filter(t => t.status !== 'pending').sort((a,b) => b.startDate.localeCompare(a.startDate));
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Time-Off Approvals</div>
        <div class="page-subtitle">Review and approve time-off requests</div>
      </div>
    </div>
    <div class="grid grid-3" style="margin-bottom: 24px;">
      <div class="stat-card"><div class="stat-label">Pending</div><div class="stat-number">${pending.length}</div><div class="stat-sub">awaiting review</div></div>
      <div class="stat-card"><div class="stat-label">Approved</div><div class="stat-number">${DB.timeOff.filter(t => t.status === 'approved').length}</div><div class="stat-sub">total</div></div>
      <div class="stat-card"><div class="stat-label">Denied</div><div class="stat-number">${DB.timeOff.filter(t => t.status === 'denied').length}</div><div class="stat-sub">total</div></div>
    </div>
    <div class="card" style="margin-bottom:24px;">
      <div class="card-title">Pending Requests</div>
      <div class="card-subtitle">Action needed</div>
      ${pending.length === 0 ? '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No pending requests.</div>' : pending.map(t => {
        const u = DB.users.find(x => x.id === t.userId);
        return `
          <div style="padding:14px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;">
            <div style="flex:1; min-width:240px;">
              <div style="font-weight:600; color:var(--burgundy-dark);">${escapeHtml(u ? u.name : '-')} - ${escapeHtml(t.type)}</div>
              <div style="font-size:13px; color:var(--slate); margin-top:2px;">${fmtDate(t.startDate)} - ${fmtDate(t.endDate)}</div>
              ${t.reason ? `<div style="font-size:13px; color:var(--slate); margin-top:4px; font-style:italic;">"${escapeHtml(t.reason)}"</div>` : ''}
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
              <button class="btn btn-success btn-sm" onclick="reviewTimeOff('${t.id}', 'approved')">Approve</button>
              <button class="btn btn-danger btn-sm" onclick="reviewTimeOff('${t.id}', 'denied')">Deny</button>
            </div>
          </div>`;
      }).join('')}
    </div>
    <div class="card">
      <div class="card-title">Reviewed Requests</div>
      <div class="card-subtitle">History</div>
      <div class="table-scroll" style="margin:0 -22px -22px; border-top:1px solid var(--border);">
        <table>
          <thead><tr><th>Employee</th><th>Type</th><th>Dates</th><th>Status</th><th>Reviewed By</th><th>Note</th></tr></thead>
          <tbody>
            ${reviewed.length === 0 ? '<tr><td colspan="6"><div class="empty"><div>No reviewed requests.</div></div></td></tr>' : reviewed.slice(0, 20).map(t => {
              const u = DB.users.find(x => x.id === t.userId);
              const r = t.reviewedBy ? DB.users.find(x => x.id === t.reviewedBy) : null;
              return `<tr>
                <td><strong>${escapeHtml(u ? u.name : '-')}</strong></td>
                <td>${escapeHtml(t.type)}</td>
                <td>${fmtDateShort(t.startDate)} - ${fmtDateShort(t.endDate)}</td>
                <td><span class="badge ${t.status === 'approved' ? 'badge-success' : 'badge-danger'}">${t.status}</span></td>
                <td style="font-size:12px;color:var(--slate);">${r ? escapeHtml(r.name) : '-'}</td>
                <td style="font-size:12px;color:var(--slate);font-style:italic;">${escapeHtml(t.reviewNote || '')}</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}
function reviewTimeOff(id, decision) {
  const t = DB.timeOff.find(x => x.id === id);
  if (!t) return;
  const note = prompt('Optional note for the employee:', '');
  if (note === null) return;
  t.status = decision;
  t.reviewedBy = currentUser().id;
  t.reviewedAt = new Date().toISOString();
  t.reviewNote = note.trim();
  saveDB();
  renderView();
  showToast('Request ' + decision, 'success');
}

// ============ HR: MANAGE SHIFTS ============
function renderAllShifts(host) {
  const today = todayISO();
  const upcoming = DB.shifts.filter(s => s.date >= today).sort((a,b) => (a.date + a.start).localeCompare(b.date + b.start));
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Manage Shifts</div>
        <div class="page-subtitle">Schedule shifts for all employees</div>
      </div>
      <div class="page-actions"><button class="btn btn-primary" onclick="openShiftModal()">+ Schedule Shift</button></div>
    </div>
    <div class="card">
      <div class="card-title">Upcoming Shifts</div>
      <div class="card-subtitle">${upcoming.length} scheduled</div>
      <div class="table-scroll" style="margin:0 -22px -22px; border-top:1px solid var(--border);">
        <table>
          <thead><tr><th>Date</th><th>Day</th><th>Employee</th><th>Time</th><th>Position</th><th>Notes</th><th></th></tr></thead>
          <tbody>
            ${upcoming.length === 0 ? '<tr><td colspan="7"><div class="empty"><div>No upcoming shifts.</div></div></td></tr>' : upcoming.map(s => {
              const u = DB.users.find(x => x.id === s.userId);
              return `<tr>
                <td><strong>${fmtDate(s.date)}</strong></td>
                <td style="color:var(--slate);font-style:italic;">${fmtDay(s.date)}</td>
                <td>${escapeHtml(u ? u.name : '-')}</td>
                <td>${fmtTimeRange(s.start, s.end)}</td>
                <td>${escapeHtml(s.position)}</td>
                <td style="font-size:12px;color:var(--slate);">${escapeHtml(s.notes || '')}</td>
                <td><button class="btn btn-sm btn-ghost" onclick="openShiftModal('${s.id}')">Edit</button> <button class="btn btn-sm btn-ghost" onclick="deleteShift('${s.id}')" style="color:var(--danger);">×</button></td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}
function openShiftModal(id) {
  const s = id ? DB.shifts.find(x => x.id === id) : null;
  showModal({
    title: s ? 'Edit Shift' : 'Schedule Shift',
    body: `
      <form id="shift-form" onsubmit="saveShift(event, '${id || ''}')">
        <div class="form-grid">
          <div class="field full"><label class="label">Employee</label>
            <select id="sh-user" required>
              <option value="">-- Select --</option>
              ${DB.users.filter(u => u.active).map(u => `<option value="${u.id}" ${s && s.userId === u.id ? 'selected' : ''}>${escapeHtml(u.name)}</option>`).join('')}
            </select>
          </div>
          <div class="field"><label class="label">Date</label><input type="date" id="sh-date" required value="${s ? s.date : todayISO()}"></div>
          <div class="field"><label class="label">Position</label><input id="sh-position" required value="${s ? escapeHtml(s.position) : ''}"></div>
          <div class="field"><label class="label">Start</label><input type="time" id="sh-start" required value="${s ? s.start : '09:00'}"></div>
          <div class="field"><label class="label">End</label><input type="time" id="sh-end" required value="${s ? s.end : '17:00'}"></div>
          <div class="field full"><label class="label">Notes</label><input id="sh-notes" value="${s ? escapeHtml(s.notes) : ''}" placeholder="Optional..."></div>
        </div>
      </form>
    `,
    submitLabel: 'Save Shift',
    submitFn: () => document.getElementById('shift-form').requestSubmit()
  });
}
function saveShift(e, id) {
  e.preventDefault();
  const data = {
    userId: document.getElementById('sh-user').value,
    date: document.getElementById('sh-date').value,
    start: document.getElementById('sh-start').value,
    end: document.getElementById('sh-end').value,
    position: document.getElementById('sh-position').value.trim(),
    notes: document.getElementById('sh-notes').value.trim()
  };
  if (id) {
    const sh = DB.shifts.find(x => x.id === id);
    if (sh) Object.assign(sh, data);
    showToast('Shift updated', 'success');
  } else {
    DB.shifts.push({ ...data, id: uid('sh') });
    showToast('Shift scheduled', 'success');
  }
  saveDB();
  closeModal();
  renderView();
}
function deleteShift(id) {
  if (!confirm('Delete this shift?')) return;
  DB.shifts = DB.shifts.filter(x => x.id !== id);
  saveDB();
  renderView();
  showToast('Shift deleted', 'success');
}

// ============ MODAL HELPERS ============
function showModal({ title, body, submitLabel, submitFn, large }) {
  if (!submitLabel) submitLabel = 'Save';
  const host = document.getElementById('modal-host');
  host.innerHTML = `
    <div class="modal-overlay active" onclick="if(event.target===this) closeModal()">
      <div class="modal ${large ? 'modal-lg' : ''}">
        <div class="modal-header">
          <div class="modal-title">${title}</div>
          <button class="modal-close" onclick="closeModal()">×</button>
        </div>
        <div class="modal-body">${body}</div>
        <div class="modal-footer">
          <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
          <button class="btn btn-primary" id="modal-submit">${submitLabel}</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById('modal-submit').onclick = submitFn;
}
function closeModal() { document.getElementById('modal-host').innerHTML = ''; }

// ============ EXCEL EXPORT ============
function downloadExcel(rows, filename, sheetName) {
  if (!sheetName) sheetName = 'Sheet1';
  if (!rows || rows.length === 0) { showToast('Nothing to export', 'error'); return; }
  const ws = XLSX.utils.json_to_sheet(rows);
  const keys = Object.keys(rows[0]);
  ws['!cols'] = keys.map(k => {
    const maxLen = Math.max(k.length, ...rows.map(r => String(r[k] || '').length));
    return { wch: Math.min(maxLen + 2, 32) };
  });
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, sheetName.slice(0, 30));
  XLSX.writeFile(wb, filename);
  showToast('Exported: ' + filename, 'success');
}

// ============ TOAST ============
function showToast(msg, type) {
  if (!type) type = '';
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = 'toast show ' + type;
  setTimeout(() => t.classList.remove('show'), 2400);
}

// ============ KEYBOARD ============
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ============ INTEGRATED VIEWS (FROM PATCH A) ============
// ============ VIEW: WEEKLY TIMESHEET ============
let timesheetWeekOffset = 0;
function renderTimesheet(host) {
  const u = currentUser();
  const r = getWeekRange(timesheetWeekOffset);
  let ts = DB.timesheets && DB.timesheets.find(t => t.userId === u.id && t.weekStart === r.start);
  if (!ts) {
    const days = [];
    for (let i = 0; i < 7; i++) {
      const d = new Date(r.start + 'T12:00:00');
      d.setDate(d.getDate() + i);
      const date = d.toISOString().slice(0,10);
      const dayEntries = DB.timeEntries.filter(e => e.userId === u.id && e.clockIn.slice(0,10) === date).sort((a,b) => a.clockIn.localeCompare(b.clockIn));
      days.push({
        date,
        in1: dayEntries[0] ? dayEntries[0].clockIn.slice(11,16) : '',
        out1: dayEntries[0] && dayEntries[0].clockOut ? dayEntries[0].clockOut.slice(11,16) : '',
        in2: dayEntries[1] ? dayEntries[1].clockIn.slice(11,16) : '',
        out2: dayEntries[1] && dayEntries[1].clockOut ? dayEntries[1].clockOut.slice(11,16) : '',
        payCode: (dayEntries[0] || dayEntries[1]) ? 'Regular' : 'Off',
        notes: ''
      });
    }
    ts = { id: null, userId: u.id, weekStart: r.start, entries: days, status: 'draft', submittedAt: null, reviewedBy: null, reviewedAt: null, reviewNote: '' };
  }
  function calcHours(entry) {
    function parse(s) { if (!s) return null; const p = s.split(':').map(Number); return p[0] * 60 + p[1]; }
    const ms1 = parse(entry.out1) != null && parse(entry.in1) != null ? parse(entry.out1) - parse(entry.in1) : 0;
    const ms2 = parse(entry.out2) != null && parse(entry.in2) != null ? parse(entry.out2) - parse(entry.in2) : 0;
    return Math.max(0, (ms1 + ms2)) / 60;
  }
  let total = 0;
  ts.entries.forEach(e => { total += calcHours(e); });
  const manager = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  const reviewer = ts.reviewedBy ? DB.users.find(x => x.id === ts.reviewedBy) : null;
  const isEditable = ts.status === 'draft' || ts.status === 'rejected';

  let html = '<div class="page-header"><div><div class="page-title">Weekly Timesheet</div><div class="page-subtitle">Submit your hours for approval by your reporting manager</div></div>';
  html += '<div class="page-actions"><select onchange="timesheetWeekOffset = parseInt(this.value); renderView();">';
  html += '<option value="0"' + (timesheetWeekOffset === 0 ? ' selected' : '') + '>This Week</option>';
  html += '<option value="-1"' + (timesheetWeekOffset === -1 ? ' selected' : '') + '>Last Week</option>';
  html += '<option value="-2"' + (timesheetWeekOffset === -2 ? ' selected' : '') + '>2 Weeks Ago</option>';
  html += '<option value="-3"' + (timesheetWeekOffset === -3 ? ' selected' : '') + '>3 Weeks Ago</option>';
  html += '</select></div></div>';

  const statusCls = ts.status === 'approved' ? 'badge-success' : ts.status === 'rejected' ? 'badge-danger' : ts.status === 'pending' ? 'badge-warning' : 'badge-muted';
  html += '<div class="card" style="margin-bottom:18px;"><div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">';
  html += '<div><div class="tag-label">Pay Period</div><div style="font-weight:700;font-size:20px;color:var(--ink);">' + fmtDate(r.start) + ' to ' + fmtDate(r.end) + '</div></div>';
  html += '<div><div class="tag-label">Status</div><div style="margin-top:4px;"><span class="badge ' + statusCls + '">' + ts.status.toUpperCase() + '</span></div></div>';
  html += '<div><div class="tag-label">Reporting Manager</div><div style="font-weight:600; color:var(--ink); font-size:15px;">' + (manager ? escapeHtml(manager.name) : 'No manager assigned') + '</div>' + (manager ? '<div style="font-size:12px; color:var(--slate);">' + escapeHtml(manager.position) + '</div>' : '') + '</div>';
  html += '<div><div class="tag-label">Total Hours</div><div style="font-weight:800; font-size:28px; color:var(--brand-red);">' + total.toFixed(2) + '</div></div>';
  html += '</div>';
  if (ts.reviewNote) {
    const bgCol = ts.status === 'rejected' ? '#FDE9EB' : '#E5F6EC';
    html += '<div style="margin-top:14px; padding:10px 14px; background:' + bgCol + '; border-radius:10px; font-size:13px;"><strong>Manager note:</strong> "' + escapeHtml(ts.reviewNote) + '"' + (reviewer ? ' - ' + escapeHtml(reviewer.name) : '') + '</div>';
  }
  html += '</div>';

  html += '<div class="table-wrap"><div class="table-header"><div class="table-title">Daily Entries</div><div class="table-meta">' + ts.entries.length + ' days - ' + total.toFixed(2) + ' hrs</div></div><div class="table-scroll"><table><thead><tr><th>Day</th><th>Date</th><th>Pay Code</th><th>Morning In</th><th>Morning Out</th><th>Afternoon In</th><th>Afternoon Out</th><th>Hours</th><th>Notes</th></tr></thead><tbody>';
  ts.entries.forEach((e, i) => {
    html += '<tr><td style="font-style:italic;color:var(--slate);">' + fmtDay(e.date) + '</td><td><strong>' + fmtDateShort(e.date) + '</strong></td>';
    if (isEditable) {
      html += '<td><select onchange="updateTsEntry(' + i + ', \'payCode\', this.value)" class="ts-input">';
      ['Regular','Overtime','PTO','Sick','Holiday','Off'].forEach(p => {
        html += '<option' + (e.payCode === p ? ' selected' : '') + '>' + p + '</option>';
      });
      html += '</select></td>';
      ['in1','out1','in2','out2'].forEach(f => {
        html += '<td><input type="time" value="' + (e[f] || '') + '" onchange="updateTsEntry(' + i + ', \'' + f + '\', this.value)" class="ts-input"></td>';
      });
    } else {
      html += '<td>' + escapeHtml(e.payCode) + '</td>';
      ['in1','out1','in2','out2'].forEach(f => { html += '<td>' + (e[f] ? fmtTime12(e[f]) : '-') + '</td>'; });
    }
    html += '<td style="font-weight:700;color:var(--brand-red);">' + calcHours(e).toFixed(2) + '</td>';
    if (isEditable) {
      html += '<td><input type="text" value="' + escapeHtml(e.notes || '') + '" placeholder="Notes" onchange="updateTsEntry(' + i + ', \'notes\', this.value)" class="ts-input"></td>';
    } else {
      html += '<td>' + escapeHtml(e.notes || '') + '</td>';
    }
    html += '</tr>';
  });
  html += '</tbody></table></div></div>';

  html += '<div style="margin-top:20px; display:flex; gap:12px; justify-content:flex-end; flex-wrap:wrap;">';
  if (ts.status === 'pending') html += '<button class="btn btn-secondary" onclick="cancelTimesheetSubmission(\'' + ts.id + '\')">Withdraw Submission</button>';
  if (isEditable) html += '<button class="btn btn-primary" onclick="submitWeeklyTimesheet()">' + (ts.status === 'rejected' ? 'Re-Submit' : 'Submit') + ' for Approval</button>';
  html += '<button class="btn btn-secondary" onclick="exportWeeklyTimesheet()">Export</button></div>';

  host.innerHTML = html;
  window.__currentTimesheetDraft = ts;
}

function fmtTime12(hm) {
  if (!hm) return '';
  const p = hm.split(':');
  const hour = parseInt(p[0]);
  const period = hour >= 12 ? 'PM' : 'AM';
  const dh = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
  return dh + ':' + p[1] + ' ' + period;
}

function updateTsEntry(idx, field, value) {
  const draft = window.__currentTimesheetDraft;
  if (!draft) return;
  draft.entries[idx][field] = value;
  if (!DB.timesheets) DB.timesheets = [];
  if (draft.id) {
    const existing = DB.timesheets.find(t => t.id === draft.id);
    if (existing) { existing.entries[idx][field] = value; saveDB(); }
  } else {
    draft.id = uid('ws');
    DB.timesheets.push(Object.assign({}, draft));
    saveDB();
    window.__currentTimesheetDraft = DB.timesheets[DB.timesheets.length - 1];
  }
  clearTimeout(window.__tsRedrawTimer);
  window.__tsRedrawTimer = setTimeout(() => renderView(), 700);
}

function submitWeeklyTimesheet() {
  const draft = window.__currentTimesheetDraft;
  if (!draft) return;
  if (!DB.timesheets) DB.timesheets = [];
  let ts;
  if (draft.id) {
    ts = DB.timesheets.find(t => t.id === draft.id);
  } else {
    ts = Object.assign({}, draft, { id: uid('ws') });
    DB.timesheets.push(ts);
  }
  ts.status = 'pending';
  ts.submittedAt = new Date().toISOString();
  ts.reviewedBy = null;
  ts.reviewedAt = null;
  ts.reviewNote = '';
  saveDB();
  renderView();
  const u = currentUser();
  const mgr = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  showToast('Timesheet submitted to ' + (mgr ? mgr.name : 'HR'), 'success');
}

function cancelTimesheetSubmission(id) {
  if (!confirm('Withdraw this submission?')) return;
  const ts = DB.timesheets.find(t => t.id === id);
  if (ts) { ts.status = 'draft'; saveDB(); renderView(); showToast('Submission withdrawn', 'success'); }
}

function exportWeeklyTimesheet() {
  const draft = window.__currentTimesheetDraft;
  if (!draft) return;
  const u = currentUser();
  const rows = draft.entries.map(e => {
    function parse(s) { if (!s) return null; const p = s.split(':').map(Number); return p[0]*60 + p[1]; }
    const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
    const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
    const hrs = Math.max(0, m1 + m2) / 60;
    return { Date: e.date, Day: fmtDay(e.date), 'Pay Code': e.payCode, 'Morning In': e.in1, 'Morning Out': e.out1, 'Afternoon In': e.in2, 'Afternoon Out': e.out2, Hours: hrs.toFixed(2), Notes: e.notes || '' };
  });
  downloadExcel(rows, 'Timesheet_' + u.name.replace(/\s/g,'_') + '_' + draft.weekStart + '.xlsx', 'Weekly Timesheet');
}

// ============ INTEGRATED VIEWS (FROM PATCH B) ============
// ============ VIEW: TIMESHEET APPROVALS ============
function renderTimesheetApprovals(host) {
  const u = currentUser();
  const myReports = DB.users.filter(x => x.managerId === u.id);
  const reportIds = u.role === 'admin' ? DB.users.map(x => x.id) : myReports.map(x => x.id);
  if (!DB.timesheets) DB.timesheets = [];
  const pending = DB.timesheets.filter(t => t.status === 'pending' && reportIds.includes(t.userId)).sort((a,b) => a.weekStart.localeCompare(b.weekStart));
  const reviewed = DB.timesheets.filter(t => t.status !== 'pending' && t.status !== 'draft' && reportIds.includes(t.userId)).sort((a,b) => b.weekStart.localeCompare(a.weekStart));

  function totalHrs(ts) {
    let h = 0;
    ts.entries.forEach(e => {
      function parse(s) { if (!s) return null; const p = s.split(':').map(Number); return p[0]*60+p[1]; }
      const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
      const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
      h += Math.max(0, m1 + m2) / 60;
    });
    return h;
  }

  let html = '<div class="page-header"><div><div class="page-title">Timesheet Approvals</div><div class="page-subtitle">';
  html += u.role === 'admin' ? 'Review submissions from anyone' : 'Review submissions from your direct reports (' + myReports.length + ')';
  html += '</div></div></div>';
  html += '<div class="grid grid-3" style="margin-bottom:24px;">';
  html += '<div class="stat-card"><div class="stat-label">Pending Review</div><div class="stat-number">' + pending.length + '</div><div class="stat-sub">awaiting your approval</div></div>';
  const approvedCount = DB.timesheets.filter(t => t.status === 'approved' && reportIds.includes(t.userId)).length;
  html += '<div class="stat-card"><div class="stat-label">Approved</div><div class="stat-number">' + approvedCount + '</div><div class="stat-sub">all time</div></div>';
  html += '<div class="stat-card"><div class="stat-label">Direct Reports</div><div class="stat-number">' + myReports.length + '</div><div class="stat-sub">on your team</div></div>';
  html += '</div>';

  html += '<div class="card" style="margin-bottom:24px;"><div class="card-title">Pending Submissions</div><div class="card-subtitle">Click to review and approve or reject</div>';
  if (pending.length === 0) {
    html += '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No pending timesheets.</div>';
  } else {
    pending.forEach(ts => {
      const emp = DB.users.find(x => x.id === ts.userId);
      html += '<div style="padding:14px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;">';
      html += '<div style="flex:1; min-width:200px;"><div style="font-weight:700;color:var(--ink);">' + escapeHtml(emp ? emp.name : '-') + '</div>';
      html += '<div style="font-size:13px;color:var(--slate);">Week of ' + fmtDate(ts.weekStart) + ' - ' + totalHrs(ts).toFixed(2) + ' hrs - Submitted ' + fmtDateShort(ts.submittedAt) + '</div></div>';
      html += '<div style="display:flex; gap:8px;">';
      html += '<button class="btn btn-sm btn-secondary" onclick="viewTimesheetDetails(\'' + ts.id + '\')">View Detail</button>';
      html += '<button class="btn btn-success btn-sm" onclick="reviewTimesheet(\'' + ts.id + '\', \'approved\')">Approve</button>';
      html += '<button class="btn btn-danger btn-sm" onclick="reviewTimesheet(\'' + ts.id + '\', \'rejected\')">Reject</button>';
      html += '</div></div>';
    });
  }
  html += '</div>';

  html += '<div class="card"><div class="card-title">Recently Reviewed</div><div class="card-subtitle">History</div>';
  html += '<div class="table-scroll" style="margin:0 -22px -22px; border-top:1px solid var(--border);"><table><thead><tr><th>Employee</th><th>Week</th><th>Hours</th><th>Status</th><th>Reviewed</th><th>Note</th></tr></thead><tbody>';
  if (reviewed.length === 0) {
    html += '<tr><td colspan="6"><div class="empty"><div>No reviewed timesheets yet.</div></div></td></tr>';
  } else {
    reviewed.slice(0, 30).forEach(ts => {
      const emp = DB.users.find(x => x.id === ts.userId);
      const rev = ts.reviewedBy ? DB.users.find(x => x.id === ts.reviewedBy) : null;
      const cls = ts.status === 'approved' ? 'badge-success' : 'badge-danger';
      html += '<tr><td><strong>' + escapeHtml(emp ? emp.name : '-') + '</strong></td>';
      html += '<td>' + fmtDateShort(ts.weekStart) + '</td>';
      html += '<td><strong>' + totalHrs(ts).toFixed(2) + '</strong></td>';
      html += '<td><span class="badge ' + cls + '">' + ts.status + '</span></td>';
      html += '<td style="font-size:12px;color:var(--slate);">' + (rev ? escapeHtml(rev.name) : '-') + '<br>' + (ts.reviewedAt ? fmtDateShort(ts.reviewedAt) : '') + '</td>';
      html += '<td style="font-size:12px;color:var(--slate);font-style:italic;">' + escapeHtml(ts.reviewNote || '') + '</td></tr>';
    });
  }
  html += '</tbody></table></div></div>';
  host.innerHTML = html;
}

function viewTimesheetDetails(id) {
  const ts = DB.timesheets.find(t => t.id === id);
  if (!ts) return;
  const emp = DB.users.find(u => u.id === ts.userId);
  function calcHours(e) {
    function parse(s) { if (!s) return null; const p = s.split(':').map(Number); return p[0]*60+p[1]; }
    const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
    const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
    return Math.max(0, m1 + m2) / 60;
  }
  let total = 0;
  let body = '<div style="margin-bottom:14px; color:var(--slate); font-size:13px;"><strong>Employee:</strong> ' + escapeHtml(emp ? emp.name : '-') + ' - ' + escapeHtml(emp ? emp.position : '') + '<br><strong>Submitted:</strong> ' + fmtDate(ts.submittedAt) + '</div>';
  body += '<table style="width:100%; border-collapse:collapse; font-size:13px;"><thead style="background:var(--bg-light);"><tr><th style="text-align:left; padding:8px;">Date</th><th>Pay Code</th><th>In</th><th>Out</th><th>In</th><th>Out</th><th>Hours</th></tr></thead><tbody>';
  ts.entries.forEach(e => {
    const h = calcHours(e);
    total += h;
    body += '<tr><td style="padding:6px 8px;">' + fmtDateShort(e.date) + ' (' + fmtDay(e.date).slice(0,3) + ')</td><td>' + e.payCode + '</td><td>' + (e.in1 || '-') + '</td><td>' + (e.out1 || '-') + '</td><td>' + (e.in2 || '-') + '</td><td>' + (e.out2 || '-') + '</td><td><strong>' + h.toFixed(2) + '</strong></td></tr>';
  });
  body += '<tr style="border-top:2px solid var(--brand-red);"><td colspan="6" style="text-align:right;padding:8px;font-weight:700;">Total</td><td style="padding:8px;font-weight:800;color:var(--brand-red);">' + total.toFixed(2) + '</td></tr>';
  body += '</tbody></table>';
  body += '<div style="margin-top:16px;"><label class="label">Decision Note</label><textarea id="ts-review-note" rows="2" placeholder="Optional note..."></textarea></div>';
  showModal({
    title: 'Timesheet: ' + (emp ? emp.name : '') + ' - Week of ' + fmtDate(ts.weekStart),
    body: body,
    submitLabel: 'Approve',
    submitFn: function() { reviewTimesheet(id, 'approved', document.getElementById('ts-review-note').value.trim()); closeModal(); },
    large: true
  });
}

function reviewTimesheet(id, decision, note) {
  const ts = DB.timesheets.find(t => t.id === id);
  if (!ts) return;
  const noteVal = note != null ? note : (prompt('Optional note for the employee:', '') || '');
  ts.status = decision;
  ts.reviewedBy = currentUser().id;
  ts.reviewedAt = new Date().toISOString();
  ts.reviewNote = noteVal.trim();
  saveDB();
  renderView();
  showToast('Timesheet ' + decision, 'success');
}

// ============ VIEW: ORG CHART ============
function renderOrgChart(host) {
  const roots = DB.users.filter(u => u.active && !u.managerId);
  const u = currentUser();
  function renderNode(user) {
    const reports = DB.users.filter(x => x.active && x.managerId === user.id);
    const isMe = user.id === u.id;
    let s = '<div class="org-node-wrap"><div class="org-node' + (isMe ? ' org-node-me' : '') + (user.role === 'admin' ? ' org-node-admin' : '') + '" onclick="openProfileForUser(\'' + user.id + '\')">';
    s += '<div class="avatar org-avatar">' + initials(user.name) + '</div>';
    s += '<div class="org-name">' + escapeHtml(user.name) + (isMe ? ' (You)' : '') + '</div>';
    s += '<div class="org-position">' + escapeHtml(user.position) + '</div>';
    s += '<div class="org-dept">' + escapeHtml(user.department || '') + '</div>';
    s += '<div class="org-meta">' + reports.length + ' direct report' + (reports.length === 1 ? '' : 's') + '</div>';
    s += '</div>';
    if (reports.length) {
      s += '<div class="org-children">' + reports.map(r => renderNode(r)).join('') + '</div>';
    }
    s += '</div>';
    return s;
  }
  let html = '<div class="page-header"><div><div class="page-title">Organization Chart</div><div class="page-subtitle">Reporting structure - built from employees in the portal</div></div>';
  if (isAdmin()) html += '<div class="page-actions"><button class="btn btn-primary" onclick="openEmployeeModal()">+ Add Employee</button></div>';
  html += '</div>';
  html += '<div class="org-chart">';
  if (roots.length === 0) {
    html += '<div class="empty"><div class="empty-icon">[org]</div><div>No org structure defined yet.</div></div>';
  } else {
    html += roots.map(r => renderNode(r)).join('');
  }
  html += '</div>';

  // Department breakdown
  html += '<div class="grid grid-2" style="margin-top:28px;">';
  html += '<div class="card"><div class="card-title">By Department</div><div class="card-subtitle">Headcount across teams</div>';
  const depts = {};
  DB.users.filter(u2 => u2.active).forEach(u2 => { const d = u2.department || 'Unassigned'; if (!depts[d]) depts[d] = []; depts[d].push(u2); });
  Object.entries(depts).forEach(function(entry) {
    const d = entry[0]; const ppl = entry[1];
    html += '<div style="padding:12px 0; border-bottom:1px solid var(--border);">';
    html += '<div style="display:flex; justify-content:space-between; align-items:center;">';
    html += '<div style="font-weight:700;color:var(--ink);">' + escapeHtml(d) + '</div>';
    html += '<div style="background:var(--brand-red-soft);color:var(--brand-red);padding:2px 10px;border-radius:12px;font-weight:700;font-size:12px;">' + ppl.length + '</div>';
    html += '</div><div style="margin-top:6px; display:flex; flex-wrap:wrap; gap:6px;">';
    ppl.forEach(p => { html += '<span class="badge badge-muted" style="cursor:pointer;" onclick="openProfileForUser(\'' + p.id + '\')">' + escapeHtml(p.name) + '</span>'; });
    html += '</div></div>';
  });
  html += '</div>';

  // My Team
  html += '<div class="card">';
  const direct = DB.users.filter(x => x.active && x.managerId === u.id);
  html += '<div class="card-title">My Team</div><div class="card-subtitle">' + direct.length + ' direct report' + (direct.length === 1 ? '' : 's') + '</div>';
  if (direct.length === 0) {
    html += '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No one reports to you currently.</div>';
  } else {
    direct.forEach(r => {
      html += '<div style="padding:10px 0; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:12px; cursor:pointer;" onclick="openProfileForUser(\'' + r.id + '\')">';
      html += '<div class="avatar" style="width:36px;height:36px;font-size:13px;">' + initials(r.name) + '</div>';
      html += '<div style="flex:1;"><div style="font-weight:600;">' + escapeHtml(r.name) + '</div><div style="font-size:12px;color:var(--slate);">' + escapeHtml(r.position) + '</div></div></div>';
    });
  }
  html += '</div></div>';

  host.innerHTML = html;
}

function openProfileForUser(uid_) {
  const user = DB.users.find(u => u.id === uid_);
  if (!user) return;
  const me = currentUser();
  const manager = user.managerId ? DB.users.find(x => x.id === user.managerId) : null;
  const reports = DB.users.filter(x => x.active && x.managerId === user.id);
  let body = '<div style="display:flex; gap:16px; align-items:center; padding-bottom:14px; border-bottom:1px solid var(--border); margin-bottom:14px;">';
  body += '<div class="avatar" style="width:60px;height:60px;font-size:20px;">' + initials(user.name) + '</div>';
  body += '<div><div style="font-weight:700; font-size:22px;color:var(--ink);">' + escapeHtml(user.name) + '</div>';
  body += '<div style="color:var(--slate);">' + escapeHtml(user.position) + '</div>';
  body += '<div style="font-size:12px;color:var(--warm-gray);margin-top:2px;"><a href="mailto:' + escapeHtml(user.email) + '">' + escapeHtml(user.email) + '</a></div></div></div>';
  body += '<div style="font-size:14px;">';
  body += '<div style="padding:6px 0;"><strong style="color:var(--slate);">Department:</strong> ' + escapeHtml(user.department || '-') + '</div>';
  body += '<div style="padding:6px 0;"><strong style="color:var(--slate);">Role:</strong> <span class="badge ' + (user.role === 'admin' ? 'badge-red' : 'badge-muted') + '">' + user.role + '</span></div>';
  body += '<div style="padding:6px 0;"><strong style="color:var(--slate);">Reports To:</strong> ' + (manager ? escapeHtml(manager.name) + ' (' + escapeHtml(manager.position) + ')' : 'No manager (top level)') + '</div>';
  body += '<div style="padding:6px 0;"><strong style="color:var(--slate);">Direct Reports:</strong> ' + (reports.length === 0 ? 'None' : reports.map(r => escapeHtml(r.name)).join(', ')) + '</div>';
  body += '<div style="padding:6px 0;"><strong style="color:var(--slate);">Joined:</strong> ' + user.createdAt + '</div>';
  body += '</div>';
  showModal({
    title: user.name + ' - Employee Profile',
    body: body,
    submitLabel: me.role === 'admin' ? 'Edit Employee' : 'Close',
    submitFn: function() { closeModal(); if (me.role === 'admin') openEmployeeModal(uid_); }
  });
}

// ============ VIEW: PROFILE / SETTINGS ============
function renderProfile(host) {
  const u = currentUser();
  const manager = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  const reports = DB.users.filter(x => x.active && x.managerId === u.id);
  let html = '<div class="page-header"><div><div class="page-title">My Profile</div><div class="page-subtitle">Manage your account, password, and personal info</div></div></div>';
  html += '<div class="grid grid-2">';
  html += '<div class="card"><div class="card-title">Personal Information</div><div class="card-subtitle">Visible to your team</div>';
  html += '<div style="display:flex; gap:16px; align-items:center; margin-bottom:20px; padding-bottom:18px; border-bottom:1px solid var(--border);">';
  html += '<div class="avatar" style="width:72px;height:72px;font-size:24px;">' + initials(u.name) + '</div>';
  html += '<div><div style="font-weight:700; font-size:22px; color:var(--ink);">' + escapeHtml(u.name) + '</div>';
  html += '<div style="color:var(--slate); font-size:14px;">' + escapeHtml(u.position) + '</div>';
  html += '<div style="margin-top:4px;"><span class="badge ' + (u.role === 'admin' ? 'badge-red' : 'badge-muted') + '">' + u.role + '</span></div></div></div>';
  html += '<form id="profile-form" onsubmit="updateProfile(event)"><div class="form-grid">';
  html += '<div class="field"><label class="label">Display Name</label><input id="p-name" value="' + escapeHtml(u.name) + '" required></div>';
  html += '<div class="field"><label class="label">Email</label><input type="email" id="p-email" value="' + escapeHtml(u.email) + '" required></div>';
  html += '<div class="field"><label class="label">Position</label><input id="p-position" value="' + escapeHtml(u.position) + '"' + (u.role !== 'admin' ? ' readonly' : '') + '></div>';
  html += '<div class="field"><label class="label">Department</label><input id="p-department" value="' + escapeHtml(u.department || '') + '"' + (u.role !== 'admin' ? ' readonly' : '') + '></div>';
  html += '</div><div style="margin-top:16px;"><button class="btn btn-primary" type="submit">Save Changes</button></div></form></div>';

  html += '<div class="card"><div class="card-title">Change Password</div><div class="card-subtitle">Update your sign-in credentials</div>';
  html += '<form id="pw-form" onsubmit="changePassword(event)"><div style="display:flex; flex-direction:column; gap:14px;">';
  html += '<div class="field"><label class="label">Current Password</label><input type="password" id="pw-current" required></div>';
  html += '<div class="field"><label class="label">New Password</label><input type="password" id="pw-new" required minlength="6"></div>';
  html += '<div class="field"><label class="label">Confirm New Password</label><input type="password" id="pw-confirm" required minlength="6"></div>';
  html += '</div><div style="margin-top:16px;"><button class="btn btn-primary" type="submit">Update Password</button></div></form>';
  html += '<div style="margin-top:28px; padding-top:20px; border-top:1px solid var(--border);">';
  html += '<div style="font-weight:700; color:var(--ink); margin-bottom:8px;">Reporting Information</div>';
  html += '<div style="font-size:14px; color:var(--slate);">';
  html += '<div><strong>Manager:</strong> ' + (manager ? escapeHtml(manager.name) + ' (' + escapeHtml(manager.position) + ')' : 'None assigned') + '</div>';
  html += '<div style="margin-top:4px;"><strong>Direct Reports:</strong> ' + (reports.length === 0 ? 'None' : reports.map(r => escapeHtml(r.name)).join(', ')) + '</div>';
  html += '<div style="margin-top:4px;"><strong>Joined:</strong> ' + u.createdAt + '</div>';
  html += '</div></div></div></div>';
  host.innerHTML = html;
}

function updateProfile(e) {
  e.preventDefault();
  const u = currentUser();
  const newName = document.getElementById('p-name').value.trim();
  const newEmail = document.getElementById('p-email').value.trim();
  if (DB.users.some(x => x.id !== u.id && x.email.toLowerCase() === newEmail.toLowerCase())) { showToast('Email already in use', 'error'); return; }
  u.name = newName;
  u.email = newEmail;
  if (u.role === 'admin') {
    u.position = document.getElementById('p-position').value.trim();
    u.department = document.getElementById('p-department').value.trim();
  }
  saveDB();
  renderApp();
  showToast('Profile updated', 'success');
}

function changePassword(e) {
  e.preventDefault();
  const u = currentUser();
  const current = document.getElementById('pw-current').value;
  const newPw = document.getElementById('pw-new').value;
  const cnf = document.getElementById('pw-confirm').value;
  if (current !== u.password) { showToast('Current password is incorrect', 'error'); return; }
  if (newPw !== cnf) { showToast('New passwords do not match', 'error'); return; }
  if (newPw.length < 6) { showToast('Password must be at least 6 characters', 'error'); return; }
  u.password = newPw;
  saveDB();
  document.getElementById('pw-form').reset();
  showToast('Password updated successfully', 'success');
}

// ============ BOOT ============
DB = loadDB();
renderApp();
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Savon Nexo Employee Portal - v0.1</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<style>__CSS__</style>
</head>
<body>
<div id="root"></div>
<script>
const SEED_TASTINGS = __DATA__;
__JS__
</script>
</body>
</html>
"""

out = (HTML
  .replace('__CSS__', CSS)
  .replace('__DATA__', TASTING_DATA)
  .replace('__JS__', JS)
  .replace('__LOGO_DATA_URL__', LOGO_DATA_URL))

out_path = HERE / 'SavonNexo_Portal_v0.1.html'
out_path.write_text(out, encoding='utf-8')
print(f'Written: {out_path}')
print(f'Size: {out_path.stat().st_size:,} bytes')
