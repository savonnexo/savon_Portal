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
