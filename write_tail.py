"""Writes the tail of build_portal.py with all missing view functions."""

# This is the JS that goes BEFORE saveEmployee — all the new view functions
NEW_VIEWS_JS = r'''
// ============ VIEW: WEEKLY TIMESHEET ============
let timesheetWeekOffset = 0;
function renderTimesheet(host) {
  const u = currentUser();
  const r = getWeekRange(timesheetWeekOffset);
  let ts = DB.timesheets.find(t => t.userId === u.id && t.weekStart === r.start);
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
    function parse(s) { if (!s) return null; const [h, m] = s.split(':').map(Number); return h * 60 + m; }
    const ms1 = parse(entry.out1) != null && parse(entry.in1) != null ? parse(entry.out1) - parse(entry.in1) : 0;
    const ms2 = parse(entry.out2) != null && parse(entry.in2) != null ? parse(entry.out2) - parse(entry.in2) : 0;
    return Math.max(0, (ms1 + ms2)) / 60;
  }
  let total = 0;
  ts.entries.forEach(e => { total += calcHours(e); });
  const manager = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  const reviewer = ts.reviewedBy ? DB.users.find(x => x.id === ts.reviewedBy) : null;
  const isEditable = ts.status === 'draft' || ts.status === 'rejected';

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Weekly Timesheet</div>
        <div class="page-subtitle">Submit your hours for approval by your reporting manager</div>
      </div>
      <div class="page-actions">
        <select onchange="timesheetWeekOffset = parseInt(this.value); renderView();">
          <option value="0" ${timesheetWeekOffset === 0 ? 'selected' : ''}>This Week</option>
          <option value="-1" ${timesheetWeekOffset === -1 ? 'selected' : ''}>Last Week</option>
          <option value="-2" ${timesheetWeekOffset === -2 ? 'selected' : ''}>2 Weeks Ago</option>
          <option value="-3" ${timesheetWeekOffset === -3 ? 'selected' : ''}>3 Weeks Ago</option>
        </select>
      </div>
    </div>
    <div class="card" style="margin-bottom:18px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px;">
        <div>
          <div class="tag-label">Pay Period</div>
          <div style="font-weight:700;font-size:20px;color:var(--ink);">${fmtDate(r.start)} - ${fmtDate(r.end)}</div>
        </div>
        <div>
          <div class="tag-label">Status</div>
          <div style="margin-top:4px;"><span class="badge ${ts.status === 'approved' ? 'badge-success' : ts.status === 'rejected' ? 'badge-danger' : ts.status === 'pending' ? 'badge-warning' : 'badge-muted'}">${ts.status.toUpperCase()}</span></div>
        </div>
        <div>
          <div class="tag-label">Reporting Manager</div>
          <div style="font-weight:600; color:var(--ink); font-size:15px;">${manager ? escapeHtml(manager.name) : 'No manager assigned'}</div>
          ${manager ? `<div style="font-size:12px; color:var(--slate);">${escapeHtml(manager.position)}</div>` : ''}
        </div>
        <div>
          <div class="tag-label">Total Hours</div>
          <div style="font-weight:800; font-size:28px; color:var(--brand-red);">${total.toFixed(2)}</div>
        </div>
      </div>
      ${ts.reviewNote ? `<div style="margin-top:14px; padding:10px 14px; background:${ts.status === 'rejected' ? '#FDE9EB' : '#E6F4E6'}; border-radius:10px; font-size:13px;"><strong>Manager note:</strong> "${escapeHtml(ts.reviewNote)}" ${reviewer ? '- ' + escapeHtml(reviewer.name) : ''}</div>` : ''}
    </div>

    <div class="table-wrap">
      <div class="table-header">
        <div class="table-title">Daily Entries</div>
        <div class="table-meta">${ts.entries.length} days - ${total.toFixed(2)} hrs</div>
      </div>
      <div class="table-scroll">
        <table>
          <thead><tr>
            <th>Day</th><th>Date</th><th>Pay Code</th>
            <th>Morning In</th><th>Morning Out</th>
            <th>Afternoon In</th><th>Afternoon Out</th>
            <th>Hours</th><th>Notes</th>
          </tr></thead>
          <tbody>
            ${ts.entries.map((e, i) => `
              <tr>
                <td style="font-style:italic;color:var(--slate);">${fmtDay(e.date)}</td>
                <td><strong>${fmtDateShort(e.date)}</strong></td>
                <td>
                  ${isEditable
                    ? `<select onchange="updateTsEntry(${i}, 'payCode', this.value)" class="ts-input">
                        ${['Regular','Overtime','PTO','Sick','Holiday','Off'].map(p => `<option ${e.payCode === p ? 'selected' : ''}>${p}</option>`).join('')}
                      </select>`
                    : `<span>${escapeHtml(e.payCode)}</span>`}
                </td>
                <td>${isEditable ? `<input type="time" value="${e.in1}" onchange="updateTsEntry(${i}, 'in1', this.value)" class="ts-input">` : (e.in1 ? fmtTime12(e.in1) : '-')}</td>
                <td>${isEditable ? `<input type="time" value="${e.out1}" onchange="updateTsEntry(${i}, 'out1', this.value)" class="ts-input">` : (e.out1 ? fmtTime12(e.out1) : '-')}</td>
                <td>${isEditable ? `<input type="time" value="${e.in2}" onchange="updateTsEntry(${i}, 'in2', this.value)" class="ts-input">` : (e.in2 ? fmtTime12(e.in2) : '-')}</td>
                <td>${isEditable ? `<input type="time" value="${e.out2}" onchange="updateTsEntry(${i}, 'out2', this.value)" class="ts-input">` : (e.out2 ? fmtTime12(e.out2) : '-')}</td>
                <td style="font-weight:700;color:var(--brand-red);">${calcHours(e).toFixed(2)}</td>
                <td>${isEditable ? `<input type="text" value="${escapeHtml(e.notes || '')}" placeholder="Notes" onchange="updateTsEntry(${i}, 'notes', this.value)" class="ts-input">` : escapeHtml(e.notes || '')}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <div style="margin-top:20px; display:flex; gap:12px; justify-content:flex-end; flex-wrap:wrap;">
      ${ts.status === 'pending'
        ? `<button class="btn btn-secondary" onclick="cancelTimesheetSubmission('${ts.id}')">Withdraw Submission</button>`
        : ''}
      ${isEditable ? `<button class="btn btn-primary" onclick="submitWeeklyTimesheet()">${ts.status === 'rejected' ? 'Re-Submit' : 'Submit'} for Approval</button>` : ''}
      <button class="btn btn-secondary" onclick="exportWeeklyTimesheet()">Export</button>
    </div>
  `;
  window.__currentTimesheetDraft = ts;
}

function updateTsEntry(idx, field, value) {
  const draft = window.__currentTimesheetDraft;
  if (!draft) return;
  draft.entries[idx][field] = value;
  if (draft.id) {
    const existing = DB.timesheets.find(t => t.id === draft.id);
    if (existing) { existing.entries[idx][field] = value; saveDB(); }
  } else {
    draft.id = uid('ws');
    DB.timesheets.push({ ...draft });
    saveDB();
    window.__currentTimesheetDraft = DB.timesheets[DB.timesheets.length - 1];
  }
  clearTimeout(window.__tsRedrawTimer);
  window.__tsRedrawTimer = setTimeout(() => renderView(), 600);
}

function submitWeeklyTimesheet() {
  const draft = window.__currentTimesheetDraft;
  if (!draft) return;
  let ts;
  if (draft.id) {
    ts = DB.timesheets.find(t => t.id === draft.id);
  } else {
    ts = { ...draft, id: uid('ws') };
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
    function parse(s) { if (!s) return null; const [h, m] = s.split(':').map(Number); return h * 60 + m; }
    const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
    const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
    const hrs = Math.max(0, m1 + m2) / 60;
    return { Date: e.date, Day: fmtDay(e.date), 'Pay Code': e.payCode, 'Morning In': e.in1, 'Morning Out': e.out1, 'Afternoon In': e.in2, 'Afternoon Out': e.out2, Hours: hrs.toFixed(2), Notes: e.notes || '' };
  });
  downloadExcel(rows, 'Timesheet_' + u.name.replace(/\s/g,'_') + '_' + draft.weekStart + '.xlsx', 'Weekly Timesheet');
}

// ============ VIEW: TIMESHEET APPROVALS ============
function renderTimesheetApprovals(host) {
  const u = currentUser();
  const myReports = DB.users.filter(x => x.managerId === u.id);
  const reportIds = u.role === 'admin' ? DB.users.map(x => x.id) : myReports.map(x => x.id);
  const pending = DB.timesheets.filter(t => t.status === 'pending' && reportIds.includes(t.userId)).sort((a,b) => a.weekStart.localeCompare(b.weekStart));
  const reviewed = DB.timesheets.filter(t => t.status !== 'pending' && t.status !== 'draft' && reportIds.includes(t.userId)).sort((a,b) => b.weekStart.localeCompare(a.weekStart));

  function totalHrs(ts) {
    let h = 0;
    ts.entries.forEach(e => {
      function parse(s) { if (!s) return null; const [hh, mm] = s.split(':').map(Number); return hh * 60 + mm; }
      const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
      const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
      h += Math.max(0, m1 + m2) / 60;
    });
    return h;
  }

  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Timesheet Approvals</div>
        <div class="page-subtitle">${u.role === 'admin' ? 'Review submissions from anyone' : 'Review submissions from your direct reports (' + myReports.length + ')'}</div>
      </div>
    </div>
    <div class="grid grid-3" style="margin-bottom:24px;">
      <div class="stat-card"><div class="stat-label">Pending Review</div><div class="stat-number">${pending.length}</div><div class="stat-sub">awaiting your approval</div></div>
      <div class="stat-card"><div class="stat-label">Approved</div><div class="stat-number">${DB.timesheets.filter(t => t.status === 'approved' && reportIds.includes(t.userId)).length}</div><div class="stat-sub">all time</div></div>
      <div class="stat-card"><div class="stat-label">Direct Reports</div><div class="stat-number">${myReports.length}</div><div class="stat-sub">on your team</div></div>
    </div>
    <div class="card" style="margin-bottom:24px;">
      <div class="card-title">Pending Submissions</div>
      <div class="card-subtitle">Click to review and approve or reject</div>
      ${pending.length === 0 ? '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No pending timesheets.</div>' : pending.map(ts => {
        const emp = DB.users.find(x => x.id === ts.userId);
        return `
          <div style="padding:14px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;">
            <div style="flex:1; min-width:200px;">
              <div style="font-weight:700;color:var(--ink);">${escapeHtml(emp ? emp.name : '-')}</div>
              <div style="font-size:13px;color:var(--slate);">Week of ${fmtDate(ts.weekStart)} - ${totalHrs(ts).toFixed(2)} hrs - Submitted ${fmtDateShort(ts.submittedAt)}</div>
            </div>
            <div style="display:flex; gap:8px;">
              <button class="btn btn-sm btn-secondary" onclick="viewTimesheetDetails('${ts.id}')">View Detail</button>
              <button class="btn btn-success btn-sm" onclick="reviewTimesheet('${ts.id}', 'approved')">Approve</button>
              <button class="btn btn-danger btn-sm" onclick="reviewTimesheet('${ts.id}', 'rejected')">Reject</button>
            </div>
          </div>`;
      }).join('')}
    </div>
    <div class="card">
      <div class="card-title">Recently Reviewed</div>
      <div class="card-subtitle">History</div>
      <div class="table-scroll" style="margin:0 -22px -22px; border-top:1px solid var(--border);">
        <table>
          <thead><tr><th>Employee</th><th>Week</th><th>Hours</th><th>Status</th><th>Reviewed</th><th>Note</th></tr></thead>
          <tbody>
            ${reviewed.length === 0 ? '<tr><td colspan="6"><div class="empty"><div>No reviewed timesheets yet.</div></div></td></tr>' : reviewed.slice(0, 30).map(ts => {
              const emp = DB.users.find(x => x.id === ts.userId);
              const rev = ts.reviewedBy ? DB.users.find(x => x.id === ts.reviewedBy) : null;
              return `<tr>
                <td><strong>${escapeHtml(emp ? emp.name : '-')}</strong></td>
                <td>${fmtDateShort(ts.weekStart)}</td>
                <td><strong>${totalHrs(ts).toFixed(2)}</strong></td>
                <td><span class="badge ${ts.status === 'approved' ? 'badge-success' : 'badge-danger'}">${ts.status}</span></td>
                <td style="font-size:12px;color:var(--slate);">${rev ? escapeHtml(rev.name) : '-'}<br>${ts.reviewedAt ? fmtDateShort(ts.reviewedAt) : ''}</td>
                <td style="font-size:12px;color:var(--slate);font-style:italic;">${escapeHtml(ts.reviewNote || '')}</td>
              </tr>`;
            }).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function viewTimesheetDetails(id) {
  const ts = DB.timesheets.find(t => t.id === id);
  if (!ts) return;
  const emp = DB.users.find(u => u.id === ts.userId);
  function calcHours(e) {
    function parse(s) { if (!s) return null; const [h, m] = s.split(':').map(Number); return h * 60 + m; }
    const m1 = (parse(e.out1) != null && parse(e.in1) != null) ? parse(e.out1) - parse(e.in1) : 0;
    const m2 = (parse(e.out2) != null && parse(e.in2) != null) ? parse(e.out2) - parse(e.in2) : 0;
    return Math.max(0, m1 + m2) / 60;
  }
  let total = 0;
  showModal({
    title: 'Timesheet: ' + (emp ? emp.name : '') + ' - Week of ' + fmtDate(ts.weekStart),
    body: `
      <div style="margin-bottom:14px; color:var(--slate); font-size:13px;">
        <strong>Employee:</strong> ${escapeHtml(emp ? emp.name : '-')} - ${escapeHtml(emp ? emp.position : '')}<br>
        <strong>Submitted:</strong> ${fmtDate(ts.submittedAt)}
      </div>
      <table style="width:100%; border-collapse:collapse; font-size:13px;">
        <thead style="background:var(--bg-light);">
          <tr><th style="text-align:left; padding:8px;">Date</th><th>Pay Code</th><th>In</th><th>Out</th><th>In</th><th>Out</th><th>Hours</th></tr>
        </thead>
        <tbody>
          ${ts.entries.map(e => {
            const h = calcHours(e);
            total += h;
            return '<tr><td style="padding:6px 8px;">' + fmtDateShort(e.date) + ' (' + fmtDay(e.date).slice(0,3) + ')</td><td>' + e.payCode + '</td><td>' + (e.in1 || '-') + '</td><td>' + (e.out1 || '-') + '</td><td>' + (e.in2 || '-') + '</td><td>' + (e.out2 || '-') + '</td><td><strong>' + h.toFixed(2) + '</strong></td></tr>';
          }).join('')}
          <tr style="border-top:2px solid var(--brand-red);"><td colspan="6" style="text-align:right;padding:8px;font-weight:700;">Total</td><td style="padding:8px;font-weight:800;color:var(--brand-red);">${total.toFixed(2)}</td></tr>
        </tbody>
      </table>
      <div style="margin-top:16px;">
        <label class="label">Decision Note</label>
        <textarea id="ts-review-note" rows="2" placeholder="Optional note for the employee..."></textarea>
      </div>
    `,
    submitLabel: 'Approve',
    submitFn: () => { reviewTimesheet(id, 'approved', document.getElementById('ts-review-note').value.trim()); closeModal(); },
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
    return `
      <div class="org-node-wrap">
        <div class="org-node ${isMe ? 'org-node-me' : ''} ${user.role === 'admin' ? 'org-node-admin' : ''}" onclick="openProfileForUser('${user.id}')">
          <div class="avatar org-avatar">${initials(user.name)}</div>
          <div class="org-name">${escapeHtml(user.name)}${isMe ? ' (You)' : ''}</div>
          <div class="org-position">${escapeHtml(user.position)}</div>
          <div class="org-dept">${escapeHtml(user.department || '')}</div>
          <div class="org-meta">${reports.length} direct report${reports.length === 1 ? '' : 's'}</div>
        </div>
        ${reports.length ? `<div class="org-children">${reports.map(r => renderNode(r)).join('')}</div>` : ''}
      </div>
    `;
  }
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">Organization Chart</div>
        <div class="page-subtitle">Reporting structure - built from employees in the portal</div>
      </div>
      ${isAdmin() ? '<div class="page-actions"><button class="btn btn-primary" onclick="openEmployeeModal()">+ Add Employee</button></div>' : ''}
    </div>
    <div class="org-chart">
      ${roots.length === 0 ? '<div class="empty"><div class="empty-icon">[org]</div><div>No org structure defined yet.</div></div>' : roots.map(r => renderNode(r)).join('')}
    </div>
    <div class="grid grid-2" style="margin-top:28px;">
      <div class="card">
        <div class="card-title">By Department</div>
        <div class="card-subtitle">Headcount across teams</div>
        ${(() => {
          const depts = {};
          DB.users.filter(u => u.active).forEach(u => { const d = u.department || 'Unassigned'; if (!depts[d]) depts[d] = []; depts[d].push(u); });
          return Object.entries(depts).map(([d, ppl]) => `
            <div style="padding:12px 0; border-bottom:1px solid var(--border);">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:700;color:var(--ink);">${escapeHtml(d)}</div>
                <div style="background:var(--brand-red-soft);color:var(--brand-red);padding:2px 10px;border-radius:12px;font-weight:700;font-size:12px;">${ppl.length}</div>
              </div>
              <div style="margin-top:6px; display:flex; flex-wrap:wrap; gap:6px;">
                ${ppl.map(p => '<span class="badge badge-muted" style="cursor:pointer;" onclick="openProfileForUser(\'' + p.id + '\')">' + escapeHtml(p.name) + '</span>').join('')}
              </div>
            </div>
          `).join('');
        })()}
      </div>
      <div class="card">
        <div class="card-title">My Team</div>
        <div class="card-subtitle">${(() => { const direct = DB.users.filter(x => x.active && x.managerId === u.id); return direct.length + ' direct report' + (direct.length === 1 ? '' : 's'); })()}</div>
        ${(() => {
          const direct = DB.users.filter(x => x.active && x.managerId === u.id);
          if (direct.length === 0) return '<div style="color:var(--warm-gray); font-style:italic; padding:12px 0;">No one reports to you currently.</div>';
          return direct.map(r => '<div style="padding:10px 0; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:12px; cursor:pointer;" onclick="openProfileForUser(\'' + r.id + '\')"><div class="avatar" style="width:36px;height:36px;font-size:13px;">' + initials(r.name) + '</div><div style="flex:1;"><div style="font-weight:600;">' + escapeHtml(r.name) + '</div><div style="font-size:12px;color:var(--slate);">' + escapeHtml(r.position) + '</div></div></div>').join('');
        })()}
      </div>
    </div>
  `;
}

function openProfileForUser(uid_) {
  const user = DB.users.find(u => u.id === uid_);
  if (!user) return;
  const me = currentUser();
  const manager = user.managerId ? DB.users.find(x => x.id === user.managerId) : null;
  const reports = DB.users.filter(x => x.active && x.managerId === user.id);
  showModal({
    title: user.name + ' - Employee Profile',
    body: `
      <div style="display:flex; gap:16px; align-items:center; padding-bottom:14px; border-bottom:1px solid var(--border); margin-bottom:14px;">
        <div class="avatar" style="width:60px;height:60px;font-size:20px;">${initials(user.name)}</div>
        <div>
          <div style="font-weight:700; font-size:22px;color:var(--ink);">${escapeHtml(user.name)}</div>
          <div style="color:var(--slate);">${escapeHtml(user.position)}</div>
          <div style="font-size:12px;color:var(--warm-gray);margin-top:2px;"><a href="mailto:${escapeHtml(user.email)}">${escapeHtml(user.email)}</a></div>
        </div>
      </div>
      <div style="font-size:14px;">
        <div style="padding:6px 0;"><strong style="color:var(--slate);">Department:</strong> ${escapeHtml(user.department || '-')}</div>
        <div style="padding:6px 0;"><strong style="color:var(--slate);">Role:</strong> <span class="badge ${user.role === 'admin' ? 'badge-red' : 'badge-muted'}">${user.role}</span></div>
        <div style="padding:6px 0;"><strong style="color:var(--slate);">Reports To:</strong> ${manager ? escapeHtml(manager.name) + ' (' + escapeHtml(manager.position) + ')' : 'No manager (top level)'}</div>
        <div style="padding:6px 0;"><strong style="color:var(--slate);">Direct Reports:</strong> ${reports.length === 0 ? 'None' : reports.map(r => escapeHtml(r.name)).join(', ')}</div>
        <div style="padding:6px 0;"><strong style="color:var(--slate);">Joined:</strong> ${user.createdAt}</div>
      </div>
    `,
    submitLabel: me.role === 'admin' ? 'Edit Employee' : 'Close',
    submitFn: () => { closeModal(); if (me.role === 'admin') openEmployeeModal(uid_); }
  });
}

// ============ VIEW: PROFILE / SETTINGS ============
function renderProfile(host) {
  const u = currentUser();
  const manager = u.managerId ? DB.users.find(x => x.id === u.managerId) : null;
  const reports = DB.users.filter(x => x.active && x.managerId === u.id);
  host.innerHTML = `
    <div class="page-header">
      <div>
        <div class="page-title">My Profile</div>
        <div class="page-subtitle">Manage your account, password, and personal info</div>
      </div>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <div class="card-title">Personal Information</div>
        <div class="card-subtitle">Visible to your team</div>
        <div style="display:flex; gap:16px; align-items:center; margin-bottom:20px; padding-bottom:18px; border-bottom:1px solid var(--border);">
          <div class="avatar" style="width:72px;height:72px;font-size:24px;">${initials(u.name)}</div>
          <div>
            <div style="font-weight:700; font-size:22px; color:var(--ink);">${escapeHtml(u.name)}</div>
            <div style="color:var(--slate); font-size:14px;">${escapeHtml(u.position)}</div>
            <div style="margin-top:4px;"><span class="badge ${u.role === 'admin' ? 'badge-red' : 'badge-muted'}">${u.role}</span></div>
          </div>
        </div>
        <form id="profile-form" onsubmit="updateProfile(event)">
          <div class="form-grid">
            <div class="field"><label class="label">Display Name</label><input id="p-name" value="${escapeHtml(u.name)}" required></div>
            <div class="field"><label class="label">Email</label><input type="email" id="p-email" value="${escapeHtml(u.email)}" required></div>
            <div class="field"><label class="label">Position</label><input id="p-position" value="${escapeHtml(u.position)}" ${u.role !== 'admin' ? 'readonly' : ''}></div>
            <div class="field"><label class="label">Department</label><input id="p-department" value="${escapeHtml(u.department || '')}" ${u.role !== 'admin' ? 'readonly' : ''}></div>
          </div>
          <div style="margin-top:16px;"><button class="btn btn-primary" type="submit">Save Changes</button></div>
        </form>
      </div>
      <div class="card">
        <div class="card-title">Change Password</div>
        <div class="card-subtitle">Update your sign-in credentials</div>
        <form id="pw-form" onsubmit="changePassword(event)">
          <div style="display:flex; flex-direction:column; gap:14px;">
            <div class="field"><label class="label">Current Password</label><input type="password" id="pw-current" required></div>
            <div class="field"><label class="label">New Password</label><input type="password" id="pw-new" required minlength="6"></div>
            <div class="field"><label class="label">Confirm New Password</label><input type="password" id="pw-confirm" required minlength="6"></div>
          </div>
          <div style="margin-top:16px;"><button class="btn btn-primary" type="submit">Update Password</button></div>
        </form>
        <div style="margin-top:28px; padding-top:20px; border-top:1px solid var(--border);">
          <div style="font-weight:700; color:var(--ink); margin-bottom:8px;">Reporting Information</div>
          <div style="font-size:14px; color:var(--slate);">
            <div><strong>Manager:</strong> ${manager ? escapeHtml(manager.name) + ' (' + escapeHtml(manager.position) + ')' : 'None assigned'}</div>
            <div style="margin-top:4px;"><strong>Direct Reports:</strong> ${reports.length === 0 ? 'None' : reports.map(r => escapeHtml(r.name)).join(', ')}</div>
            <div style="margin-top:4px;"><strong>Joined:</strong> ${u.createdAt}</div>
          </div>
        </div>
      </div>
    </div>
  `;
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
  const confirm_ = document.getElementById('pw-confirm').value;
  if (current !== u.password) { showToast('Current password is incorrect', 'error'); return; }
  if (newPw !== confirm_) { showToast('New passwords do not match', 'error'); return; }
  if (newPw.length < 6) { showToast('Password must be at least 6 characters', 'error'); return; }
  u.password = newPw;
  saveDB();
  document.getElementById('pw-form').reset();
  showToast('Password updated successfully', 'success');
}
'''

# Remaining JS that was originally in the tail (saveEmployee onwards)
JS_TAIL = r'''
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
        <button class="btn btn-secondary" onclick="exportAllTime()">Export Filtered</button>
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
    return { Employee: u ? u.name : '-', Email: u ? u.email : '', Date: e.clockIn.slice(0,10), Day: fmtDay(e.clockIn), 'Clock In': fmtTime(e.clockIn), 'Clock Out': out ? fmtTime(e.clockOut) : 'In progress', Hours: out ? ((out - new Date(e.clockIn)) / 3600000).toFixed(2) : '', Note: e.note || '', Edited: e.edited ? 'Yes' : '' };
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
        return '<div style="padding:14px 0; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;"><div style="flex:1; min-width:240px;"><div style="font-weight:700; color:var(--ink);">' + escapeHtml(u ? u.name : '-') + ' - ' + escapeHtml(t.type) + '</div><div style="font-size:13px; color:var(--slate); margin-top:2px;">' + fmtDate(t.startDate) + ' - ' + fmtDate(t.endDate) + '</div>' + (t.reason ? '<div style="font-size:13px; color:var(--slate); margin-top:4px; font-style:italic;">"' + escapeHtml(t.reason) + '"</div>' : '') + '</div><div style="display:flex; gap:8px; align-items:center;"><button class="btn btn-success btn-sm" onclick="reviewTimeOff(\'' + t.id + '\', \'approved\')">Approve</button><button class="btn btn-danger btn-sm" onclick="reviewTimeOff(\'' + t.id + '\', \'denied\')">Deny</button></div></div>';
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
              return '<tr><td><strong>' + escapeHtml(u ? u.name : '-') + '</strong></td><td>' + escapeHtml(t.type) + '</td><td>' + fmtDateShort(t.startDate) + ' - ' + fmtDateShort(t.endDate) + '</td><td><span class="badge ' + (t.status === 'approved' ? 'badge-success' : 'badge-danger') + '">' + t.status + '</span></td><td style="font-size:12px;color:var(--slate);">' + (r ? escapeHtml(r.name) : '-') + '</td><td style="font-size:12px;color:var(--slate);font-style:italic;">' + escapeHtml(t.reviewNote || '') + '</td></tr>';
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
              return '<tr><td><strong>' + fmtDate(s.date) + '</strong></td><td style="color:var(--slate);font-style:italic;">' + fmtDay(s.date) + '</td><td>' + escapeHtml(u ? u.name : '-') + '</td><td>' + fmtTimeRange(s.start, s.end) + '</td><td>' + escapeHtml(s.position) + '</td><td style="font-size:12px;color:var(--slate);">' + escapeHtml(s.notes || '') + '</td><td><button class="btn btn-sm btn-ghost" onclick="openShiftModal(\'' + s.id + '\')">Edit</button> <button class="btn btn-sm btn-ghost" onclick="deleteShift(\'' + s.id + '\')" style="color:var(--brand-red);">x</button></td></tr>';
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
  const data = { userId: document.getElementById('sh-user').value, date: document.getElementById('sh-date').value, start: document.getElementById('sh-start').value, end: document.getElementById('sh-end').value, position: document.getElementById('sh-position').value.trim(), notes: document.getElementById('sh-notes').value.trim() };
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
          <button class="modal-close" onclick="closeModal()">x</button>
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

// ============ BOOT ============
DB = loadDB();
renderApp();
'''

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Savon Nexo Employee Portal - v0.1</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
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
'''

# Build the tail content as Python source code
TAIL_PY = "\n" + NEW_VIEWS_JS + "\n" + JS_TAIL + '"""\n\n'
TAIL_PY += 'HTML = """' + HTML_TEMPLATE + '"""\n\n'
TAIL_PY += 'out = (HTML\n'
TAIL_PY += "  .replace('__CSS__', CSS)\n"
TAIL_PY += "  .replace('__DATA__', TASTING_DATA)\n"
TAIL_PY += "  .replace('__JS__', JS)\n"
TAIL_PY += "  .replace('__LOGO_DATA_URL__', LOGO_DATA_URL))\n\n"
TAIL_PY += "out_path = HERE / 'SavonNexo_Portal_v0.1.html'\n"
TAIL_PY += "out_path.write_text(out, encoding='utf-8')\n"
TAIL_PY += "print(f'Written: {out_path}')\n"
TAIL_PY += "print(f'Size: {out_path.stat().st_size:,} bytes')\n"

# Read the truncated file content (everything up to line 2843)
with open('build_portal.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the boundary: end of openEmployeeModal function (closing })
# We want everything up to and including the `});\n}\n` of openEmployeeModal
boundary = '    submitFn: () => document.getElementById(\'emp-form\').requestSubmit(),\n    large: true\n  });\n}\n'
idx = content.find(boundary)
if idx == -1:
    print('ERROR: Could not find boundary in build_portal.py')
    import sys; sys.exit(1)
head = content[:idx + len(boundary)]

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(head + TAIL_PY)

print(f'Wrote complete build_portal.py: {len(head + TAIL_PY):,} chars')
