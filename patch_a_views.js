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
      const dayEntries = DB.timeEntries.filter(e => e.userId === u.id && getLocalDateString(e.clockIn) === date).sort((a,b) => a.clockIn.localeCompare(b.clockIn));
      days.push({
        date,
        in1: dayEntries[0] ? getLocalHM(dayEntries[0].clockIn) : '',
        out1: dayEntries[0] && dayEntries[0].clockOut ? getLocalHM(dayEntries[0].clockOut) : '',
        in2: dayEntries[1] ? getLocalHM(dayEntries[1].clockIn) : '',
        out2: dayEntries[1] && dayEntries[1].clockOut ? getLocalHM(dayEntries[1].clockOut) : '',
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
