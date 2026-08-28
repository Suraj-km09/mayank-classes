/**
 * Admin Command Center & Management Portal Logic
 * Mayank Classes Coaching Platform
 */

let adminUser = null;
let allAdminStudents = [];
let allAdminInquiries = [];
let currentInquiryStatusFilter = '';
let allAdminNotices = [];
let allAdminBatches = [];
let allAdminCourses = [];

document.addEventListener('DOMContentLoaded', async () => {
  if (!AuthManager.protectPage('ADMIN')) return;
  adminUser = AuthManager.getUser();

  updateAdminProfileUI();
  loadAdminDashboard();
});

function updateAdminProfileUI() {
  const nameEl = document.getElementById('user-display-name');
  const roleEl = document.getElementById('user-display-role');
  const avatarEl = document.getElementById('user-display-avatar');

  if (nameEl) nameEl.innerText = adminUser.full_name || 'Mayank Agrawal';
  if (roleEl) roleEl.innerText = 'Administrator';
  if (avatarEl && adminUser.avatar_url) avatarEl.src = adminUser.avatar_url;
}

function switchAdminTab(tabId) {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.sidebar-nav-item a').forEach(el => el.classList.remove('active'));

  const targetPane = document.getElementById(`pane-${tabId}`);
  const targetNav = document.getElementById(`nav-${tabId}`);

  if (targetPane) targetPane.classList.remove('hidden');
  if (targetNav) targetNav.classList.add('active');

  if (tabId === 'dashboard') loadAdminDashboard();
  if (tabId === 'students') loadAdminStudentsTab();
  if (tabId === 'teachers') loadAdminTeachersTab();
  if (tabId === 'batches') loadAdminBatchesTab();
  if (tabId === 'courses') loadAdminCoursesTab();
  if (tabId === 'finance') loadAdminFinanceTab();
  if (tabId === 'inquiries') loadAdminInquiriesTab();
  if (tabId === 'notices') loadAdminNoticesTab();
}

// ─────────────────────────────────────────────────────────
// 1. DASHBOARD OVERVIEW
// ─────────────────────────────────────────────────────────
async function loadAdminDashboard() {
  try {
    const data = await api.get('/admin/stats/');
    const kpis = data.kpis;

    const elTotalStudents = document.getElementById('kpi-total-students');
    const elTotalFaculty = document.getElementById('kpi-total-faculty');
    const elRevenue = document.getElementById('kpi-revenue-collected');
    const elPending = document.getElementById('kpi-pending-fees');
    const elAttendance = document.getElementById('kpi-today-attendance');
    const elBatches = document.getElementById('kpi-active-batches');
    const elInquiries = document.getElementById('kpi-new-inquiries');
    const elInqBadge = document.getElementById('admin-inq-badge');

    if (elTotalStudents) elTotalStudents.innerText = kpis.total_students;
    if (elTotalFaculty) elTotalFaculty.innerText = kpis.total_teachers;
    if (elRevenue) elRevenue.innerText = formatCurrency(kpis.total_collected_inr);
    if (elPending) elPending.innerText = formatCurrency(kpis.total_pending_inr);
    if (elAttendance) elAttendance.innerText = `${kpis.today_attendance_pct}%`;
    if (elBatches) elBatches.innerText = kpis.active_batches;
    if (elInquiries) elInquiries.innerText = kpis.new_inquiries;
    if (elInqBadge) elInqBadge.innerText = `${kpis.new_inquiries} New`;

    // Recent Inquiries Table
    const inqContainer = document.getElementById('recent-inquiries-table');
    if (inqContainer && data.recent_inquiries) {
      if (data.recent_inquiries.length === 0) {
        inqContainer.innerHTML = `<tr><td colspan="4" class="text-center p-3">No recent inquiries.</td></tr>`;
      } else {
        inqContainer.innerHTML = data.recent_inquiries.map(inq => {
          let badgeClass = inq.status === 'NEW' ? 'badge-warning' : (inq.status === 'CONVERTED' ? 'badge-success' : 'badge-info');
          return `
            <tr>
              <td>
                <strong>${inq.full_name}</strong>
                <div style="font-size:0.72rem;color:var(--text-muted);">${formatDate(inq.created_at)}</div>
              </td>
              <td><a href="tel:${inq.phone}" style="color:var(--cat-jee);font-weight:600;">📞 ${inq.phone}</a></td>
              <td><span style="font-size:0.8rem;">${inq.course_interested}</span></td>
              <td>
                <span class="badge ${badgeClass}">${inq.status_display || inq.status}</span>
              </td>
            </tr>
          `;
        }).join('');
      }
    }
  } catch (err) {
    console.error('Admin dashboard error:', err);
  }
}

// ─────────────────────────────────────────────────────────
// 2. STUDENTS DIRECTORY & ADMISSION
// ─────────────────────────────────────────────────────────
async function loadAdminStudentsTab() {
  const tableBody = document.getElementById('students-table-body');
  if (!tableBody) return;

  tableBody.innerHTML = `<tr><td colspan="7" class="text-center p-4"><div class="spinner" style="margin:0 auto;"></div></td></tr>`;

  try {
    const data = await api.get('/students/');
    allAdminStudents = data.results || data;

    const countBadge = document.getElementById('admin-students-count');
    if (countBadge) {
      countBadge.innerText = `${allAdminStudents.length} Enrolled Students`;
    }

    renderAdminStudentsTable(allAdminStudents);
  } catch (err) {
    console.error('Error loading students:', err);
    tableBody.innerHTML = `<tr><td colspan="7" class="text-center p-4 text-danger">Failed to load students directory.</td></tr>`;
  }
}

function renderAdminStudentsTable(students) {
  const tableBody = document.getElementById('students-table-body');
  if (!tableBody) return;

  if (students.length === 0) {
    tableBody.innerHTML = `<tr><td colspan="7" class="text-center p-4">No enrolled students found.</td></tr>`;
    return;
  }

  tableBody.innerHTML = students.map(s => {
    const prof = s.student_profile || {};
    return `
      <tr>
        <td>
          <div class="flex items-center gap-2">
            <img src="${s.avatar_url || 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=100'}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;flex-shrink:0;">
            <div>
              <strong style="color:var(--text-main);">${s.full_name}</strong>
              <div style="font-size:0.75rem;color:var(--text-muted);">${s.email}</div>
            </div>
          </div>
        </td>
        <td><span class="badge badge-primary font-mono">${prof.roll_number || '-'}</span></td>
        <td><span style="font-size:0.85rem;font-weight:600;">${prof.target_exam || 'JEE / NEET'}</span></td>
        <td><span class="badge badge-secondary">${prof.current_class || 'Class 11'}</span></td>
        <td><a href="tel:${s.phone}" style="font-size:0.85rem;color:var(--primary-600);font-weight:600;">${s.phone || '-'}</a></td>
        <td><span style="font-size:0.85rem;color:var(--text-muted);">${prof.parent_phone || '-'}</span></td>
        <td>
          <button onclick="deleteStudent(${s.id}, '${s.full_name.replace(/'/g, "\\'")}')" class="btn btn-secondary btn-sm" style="padding:0.25rem 0.55rem;font-size:0.75rem;color:var(--brand-red);" title="Remove Student">
            🗑 Remove
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

function searchAdminStudents(keyword) {
  const q = keyword.toLowerCase().trim();
  if (!q) {
    renderAdminStudentsTable(allAdminStudents);
    return;
  }
  const filtered = allAdminStudents.filter(s => {
    const prof = s.student_profile || {};
    return (
      s.full_name.toLowerCase().includes(q) ||
      s.email.toLowerCase().includes(q) ||
      (s.phone && s.phone.toLowerCase().includes(q)) ||
      (prof.roll_number && prof.roll_number.toLowerCase().includes(q)) ||
      (prof.target_exam && prof.target_exam.toLowerCase().includes(q))
    );
  });
  renderAdminStudentsTable(filtered);
}

function openAddStudentModal() {
  const existing = document.getElementById('new-student-modal');
  if (existing) existing.remove();

  const modalHtml = `
    <div class="global-modal-backdrop" id="new-student-modal" style="display:flex;" onclick="if(event.target===this) this.remove()">
      <div class="global-modal-card" style="max-width:540px;">
        <div class="modal-header-banner">
          <div>
            <span class="badge badge-gold" style="margin-bottom:0.25rem;">Student Admission</span>
            <h3 style="margin:0;font-size:1.25rem;">Admit & Enroll New Student</h3>
          </div>
          <button onclick="document.getElementById('new-student-modal').remove()" class="modal-close-btn">&times;</button>
        </div>

        <form id="add-student-form" onsubmit="submitNewStudentForm(event)" style="padding:1.5rem;">
          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">First Name *</label>
              <input class="form-control" id="stu_fname" placeholder="e.g. Rohan" required>
            </div>
            <div class="form-group">
              <label class="form-label">Last Name *</label>
              <input class="form-control" id="stu_lname" placeholder="e.g. Sharma" required>
            </div>
          </div>

          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">Username *</label>
              <input class="form-control" id="stu_uname" placeholder="rohan.sharma" required>
            </div>
            <div class="form-group">
              <label class="form-label">Email Address *</label>
              <input class="form-control" type="email" id="stu_email" placeholder="rohan@example.com" required>
            </div>
          </div>

          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">Initial Password *</label>
              <input class="form-control" type="password" id="stu_pass" placeholder="Min 6 chars" required minlength="6">
            </div>
            <div class="form-group">
              <label class="form-label">Student Phone *</label>
              <input class="form-control" id="stu_phone" placeholder="+91 98765..." required>
            </div>
          </div>

          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">Target Examination *</label>
              <select class="form-control" id="stu_target">
                <option value="JEE Advanced 2026/27">JEE Advanced (Main & Adv)</option>
                <option value="NEET-UG 2026/27">NEET-UG Medical</option>
                <option value="Class 10 Board & NTSE">Class 10 Board & NTSE</option>
                <option value="Class 9 Foundation">Class 9 Foundation</option>
                <option value="Class 8 Pre-Foundation">Class 8 Pre-Foundation</option>
                <option value="CUET / NDA">CUET (UG) / NDA</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Academic Class *</label>
              <select class="form-control" id="stu_class">
                <option value="Class 11">Class 11</option>
                <option value="Class 12">Class 12</option>
                <option value="Dropper / Repeater">Dropper / Repeater</option>
                <option value="Class 10">Class 10</option>
                <option value="Class 9">Class 9</option>
                <option value="Class 8">Class 8</option>
                <option value="Class 7">Class 7</option>
                <option value="Class 6">Class 6</option>
              </select>
            </div>
          </div>

          <div class="flex items-center justify-end gap-2" style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--border-color);">
            <button type="button" onclick="document.getElementById('new-student-modal').remove()" class="btn btn-secondary">Cancel</button>
            <button type="submit" id="btn-submit-student" class="btn btn-primary">Admit & Generate Roll Number ➔</button>
          </div>
        </form>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function submitNewStudentForm(e) {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-student');
  const origText = btn.innerHTML;

  const payload = {
    first_name: document.getElementById('stu_fname').value.trim(),
    last_name: document.getElementById('stu_lname').value.trim(),
    username: document.getElementById('stu_uname').value.trim(),
    email: document.getElementById('stu_email').value.trim(),
    password: document.getElementById('stu_pass').value,
    phone: document.getElementById('stu_phone').value.trim(),
    target_exam: document.getElementById('stu_target').value,
    current_class: document.getElementById('stu_class').value,
  };

  try {
    btn.disabled = true;
    btn.innerHTML = 'Enrolling... ⏳';

    const res = await api.post('/students/', payload);
    const roll = (res.student_profile && res.student_profile.roll_number) || 'MC-NEW';
    showToast(`🎉 Student ${payload.first_name} ${payload.last_name} admitted! Roll: ${roll}`, 'success', 6000);
    
    const modal = document.getElementById('new-student-modal');
    if (modal) modal.remove();
    loadAdminStudentsTab();
  } catch (err) {
    showToast(err.message || 'Failed to admit student.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

async function deleteStudent(studentId, studentName) {
  if (!confirm(`Are you sure you want to remove student "${studentName}"? This action cannot be undone.`)) return;

  try {
    await api.delete(`/users/${studentId}/`);
    showToast(`Student "${studentName}" removed successfully.`, 'info');
    loadAdminStudentsTab();
  } catch (err) {
    showToast(err.message || 'Failed to remove student.', 'error');
  }
}

// ─────────────────────────────────────────────────────────
// 3. TEACHERS & FACULTY ROSTER
// ─────────────────────────────────────────────────────────
async function loadAdminTeachersTab() {
  const container = document.getElementById('teachers-grid-container');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center w-full"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const data = await api.get('/teachers/');
    const teachers = data.results || data;

    container.innerHTML = teachers.map(t => {
      const prof = t.teacher_profile || {};
      return `
        <div class="card p-4" style="border-radius:18px;box-shadow:var(--shadow-sm);border:1.5px solid var(--border-color);transition:all 0.2s ease;">
          <div class="flex items-center gap-3" style="margin-bottom:1rem;">
            <img src="${t.avatar_url || 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200'}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid var(--brand-crimson);">
            <div>
              <h4 style="font-size:1.15rem;font-weight:800;margin:0 0 0.25rem;color:var(--text-main);">${t.full_name}</h4>
              <p style="font-size:0.84rem;color:var(--primary-600);font-weight:700;margin:0 0 0.35rem;">${prof.designation || 'Master Faculty'}</p>
              <span class="badge badge-gold" style="font-size:0.7rem;">⭐ ${prof.rating || '4.9'} / 5.0 Rating</span>
            </div>
          </div>

          <div style="font-size:0.85rem;color:var(--text-muted);line-height:1.6;margin-bottom:1rem;">
            <p style="margin:0 0 0.35rem;"><strong>🎯 Subject:</strong> ${prof.specialization || 'STEM Core'}</p>
            <p style="margin:0 0 0.35rem;"><strong>🎓 Qualifications:</strong> ${prof.qualification || 'Ex-IIT / AIIMS'}</p>
            <p style="margin:0;"><strong>⏳ Experience:</strong> ${prof.experience_years || 5}+ Years Teaching</p>
          </div>

          <div class="flex items-center justify-between" style="padding-top:0.75rem;border-top:1px solid var(--border-color);font-size:0.8rem;color:var(--text-muted);">
            <span>Employee ID: <strong>${prof.employee_id || 'FAC-01'}</strong></span>
            <span>${prof.total_students_mentored || 1500}+ Students Mentored</span>
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading faculty roster:', err);
    container.innerHTML = `<div class="card p-4 text-center w-full text-danger">Failed to load faculty roster.</div>`;
  }
}

// ─────────────────────────────────────────────────────────
// 4. BATCHES MANAGER
// ─────────────────────────────────────────────────────────
async function loadAdminBatchesTab() {
  const container = document.getElementById('admin-batches-table-body');
  if (!container) return;

  container.innerHTML = `<tr><td colspan="6" class="text-center p-4"><div class="spinner" style="margin:0 auto;"></div></td></tr>`;

  try {
    const data = await api.get('/batches/');
    allAdminBatches = data.results || data;

    if (allAdminBatches.length === 0) {
      container.innerHTML = `<tr><td colspan="6" class="text-center p-4">No active classroom batches found.</td></tr>`;
      return;
    }

    container.innerHTML = allAdminBatches.map(b => {
      const pct = Math.round(((b.enrolled_count || 0) / (b.max_capacity || 40)) * 100);
      return `
        <tr>
          <td><strong style="color:var(--text-main);">${b.name}</strong></td>
          <td><span class="badge badge-primary font-mono">${b.code}</span></td>
          <td><span style="font-size:0.85rem;font-weight:600;">${b.course_title || 'Classroom Program'}</span></td>
          <td><span class="badge badge-secondary">🏛️ ${b.classroom || 'Lecture Hall 1'}</span></td>
          <td><span style="font-size:0.84rem;color:var(--text-muted);">⏱ ${b.schedule_time || 'Mon-Fri 4:00 PM'}</span></td>
          <td>
            <div style="font-size:0.82rem;margin-bottom:0.25rem;">
              <strong>${b.enrolled_count || 0}</strong> / ${b.max_capacity || 40} (${pct}%)
            </div>
            <div style="background:#E2E8F0;border-radius:6px;height:6px;width:100px;overflow:hidden;">
              <div style="background:var(--primary-600);height:100%;width:${Math.min(pct, 100)}%;"></div>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading batches:', err);
    container.innerHTML = `<tr><td colspan="6" class="text-center p-4 text-danger">Failed to load batches list.</td></tr>`;
  }
}

async function openAddBatchModal() {
  const existing = document.getElementById('new-batch-modal');
  if (existing) existing.remove();

  // Fetch courses list
  let coursesList = [];
  try {
    const cData = await api.get('/courses/');
    coursesList = cData.results || cData;
  } catch (e) {}

  const optionsHtml = coursesList.map(c => `<option value="${c.id}">${c.title}</option>`).join('');

  const modalHtml = `
    <div class="global-modal-backdrop" id="new-batch-modal" style="display:flex;" onclick="if(event.target===this) this.remove()">
      <div class="global-modal-card" style="max-width:520px;">
        <div class="modal-header-banner">
          <div>
            <span class="badge badge-gold" style="margin-bottom:0.25rem;">Academic Schedule</span>
            <h3 style="margin:0;font-size:1.25rem;">Create New Classroom Batch</h3>
          </div>
          <button onclick="document.getElementById('new-batch-modal').remove()" class="modal-close-btn">&times;</button>
        </div>

        <form id="add-batch-form" onsubmit="submitNewBatchForm(event)" style="padding:1.5rem;">
          <div class="form-group">
            <label class="form-label">Course Program *</label>
            <select class="form-control" id="bat_course" required>
              ${optionsHtml || '<option value="1">JEE Advanced Pinnacle</option>'}
            </select>
          </div>

          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">Batch Name *</label>
              <input class="form-control" id="bat_name" placeholder="e.g. Pinnacle Super-30 Morning" required>
            </div>
            <div class="form-group">
              <label class="form-label">Batch Code *</label>
              <input class="form-control" id="bat_code" placeholder="e.g. JEE-PINN-M1" required>
            </div>
          </div>

          <div class="grid grid-2 gap-3">
            <div class="form-group">
              <label class="form-label">Lecture Hall / Room *</label>
              <input class="form-control" id="bat_room" placeholder="Room 101, Kota Campus" required>
            </div>
            <div class="form-group">
              <label class="form-label">Max Student Capacity *</label>
              <input class="form-control" type="number" id="bat_capacity" value="35" min="5" max="100" required>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Weekly Schedule Timing *</label>
            <input class="form-control" id="bat_schedule" placeholder="Mon, Wed, Fri (4:00 PM – 7:30 PM)" required>
          </div>

          <div class="flex items-center justify-end gap-2" style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--border-color);">
            <button type="button" onclick="document.getElementById('new-batch-modal').remove()" class="btn btn-secondary">Cancel</button>
            <button type="submit" id="btn-submit-batch" class="btn btn-primary">Create Batch Allocation ➔</button>
          </div>
        </form>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function submitNewBatchForm(e) {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-batch');
  const origText = btn.innerHTML;

  const payload = {
    course: document.getElementById('bat_course').value,
    name: document.getElementById('bat_name').value.trim(),
    code: document.getElementById('bat_code').value.trim(),
    classroom: document.getElementById('bat_room').value.trim(),
    max_capacity: parseInt(document.getElementById('bat_capacity').value),
    schedule_time: document.getElementById('bat_schedule').value.trim(),
    is_active: true
  };

  try {
    btn.disabled = true;
    btn.innerHTML = 'Creating... ⏳';

    await api.post('/batches/', payload);
    showToast(`🎉 Batch "${payload.name}" created successfully!`, 'success', 5000);
    
    const modal = document.getElementById('new-batch-modal');
    if (modal) modal.remove();
    loadAdminBatchesTab();
  } catch (err) {
    showToast(err.message || 'Failed to create batch.', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

// ─────────────────────────────────────────────────────────
// 5. PROGRAMS & COURSES OVERVIEW
// ─────────────────────────────────────────────────────────
async function loadAdminCoursesTab() {
  const container = document.getElementById('admin-courses-grid');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center w-full"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const data = await api.get('/courses/');
    allAdminCourses = data.results || data;

    container.innerHTML = allAdminCourses.map(c => `
      <div class="card" style="border-radius:18px;overflow:hidden;border:1.5px solid var(--border-color);display:flex;flex-direction:column;">
        <img src="${c.thumbnail_url || 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=400'}" style="width:100%;height:160px;object-fit:cover;">
        <div style="padding:1.25rem;flex:1;display:flex;flex-direction:column;">
          <div class="flex items-center justify-between" style="margin-bottom:0.5rem;">
            <span class="badge badge-primary">${c.category_display || c.category}</span>
            <span style="font-size:0.75rem;color:var(--text-muted);font-weight:600;">${c.duration_weeks} Wks</span>
          </div>
          <h4 style="font-size:1.1rem;font-weight:800;margin:0 0 0.5rem;color:var(--text-main);">${c.title}</h4>
          <p style="font-size:0.82rem;color:var(--text-muted);line-height:1.4;margin-bottom:1rem;flex:1;">${c.short_description}</p>
          <div class="flex items-center justify-between" style="padding-top:0.75rem;border-top:1px solid var(--border-color);">
            <div>
              <span style="font-size:0.75rem;color:var(--text-muted);text-decoration:line-through;">₹${Number(c.price).toLocaleString('en-IN')}</span>
              <div style="font-size:1.1rem;font-weight:900;color:var(--cat-jee);">₹${Number(c.discount_price || c.price).toLocaleString('en-IN')}</div>
            </div>
            <a href="/courses/${c.slug}/" target="_blank" class="btn btn-secondary btn-sm">Public View ↗</a>
          </div>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Error loading courses:', err);
    container.innerHTML = `<div class="card p-4 text-center w-full text-danger">Failed to load courses.</div>`;
  }
}

// ─────────────────────────────────────────────────────────
// 6. FINANCE & INVOICES
// ─────────────────────────────────────────────────────────
async function loadAdminFinanceTab() {
  const container = document.getElementById('admin-fees-table-body');
  if (!container) return;

  container.innerHTML = `<tr><td colspan="8" class="text-center p-4"><div class="spinner" style="margin:0 auto;"></div></td></tr>`;

  try {
    const data = await api.get('/fees/');
    const invoices = data.results || data;

    if (invoices.length === 0) {
      container.innerHTML = `<tr><td colspan="8" class="text-center p-4">No tuition fee records found.</td></tr>`;
      return;
    }

    container.innerHTML = invoices.map(inv => {
      const badgeClass = inv.status === 'PAID' ? 'badge-success' : (inv.status === 'PARTIAL' ? 'badge-warning' : 'badge-danger');
      return `
        <tr>
          <td><strong class="font-mono">#${inv.invoice_number}</strong></td>
          <td>
            <strong>${inv.student_name}</strong>
            <div style="font-size:0.75rem;color:var(--text-muted);">${inv.roll_number}</div>
          </td>
          <td><span style="font-size:0.85rem;">${inv.course_title || 'Classroom Coaching'}</span></td>
          <td><strong>${formatCurrency(inv.total_amount)}</strong></td>
          <td style="color:#15803D;font-weight:700;">${formatCurrency(inv.paid_amount)}</td>
          <td style="color:#BE123C;font-weight:700;">${formatCurrency(inv.due_amount)}</td>
          <td><span class="badge ${badgeClass}">${inv.status_display || inv.status}</span></td>
          <td><span style="font-size:0.82rem;color:var(--text-muted);">${formatDate(inv.due_date)}</span></td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading finance records:', err);
    container.innerHTML = `<tr><td colspan="8" class="text-center p-4 text-danger">Failed to load fee accounting records.</td></tr>`;
  }
}

// ─────────────────────────────────────────────────────────
// 7. ADMISSION INQUIRIES & LEADS
// ─────────────────────────────────────────────────────────
async function loadAdminInquiriesTab() {
  const container = document.getElementById('all-inquiries-table-body');
  if (!container) return;

  container.innerHTML = `<tr><td colspan="7" class="text-center p-4"><div class="spinner" style="margin:0 auto;"></div></td></tr>`;

  try {
    const data = await api.get('/inquiries/');
    allAdminInquiries = data.results || data;

    renderAdminInquiriesTable(allAdminInquiries);
  } catch (err) {
    console.error('Error loading inquiries:', err);
    container.innerHTML = `<tr><td colspan="7" class="text-center p-4 text-danger">Failed to load inquiries.</td></tr>`;
  }
}

function renderAdminInquiriesTable(inquiries) {
  const container = document.getElementById('all-inquiries-table-body');
  if (!container) return;

  if (inquiries.length === 0) {
    container.innerHTML = `<tr><td colspan="7" class="text-center p-4">No admission leads found.</td></tr>`;
    return;
  }

  container.innerHTML = inquiries.map(inq => {
    const cleanPhone = inq.phone.replace(/[^0-9]/g, '');
    return `
      <tr>
        <td>
          <strong style="color:var(--text-main);">${inq.full_name}</strong>
          <div style="font-size:0.75rem;color:var(--text-muted);">${inq.email}</div>
        </td>
        <td>
          <a href="tel:${inq.phone}" style="color:var(--primary-600);font-weight:700;font-size:0.88rem;">
            📞 ${inq.phone}
          </a>
        </td>
        <td><span style="font-size:0.85rem;font-weight:600;">${inq.course_interested}</span></td>
        <td><span class="badge badge-secondary">${inq.current_class}</span></td>
        <td style="max-width:240px;font-size:0.82rem;color:var(--text-muted);line-height:1.4;">
          ${inq.message || 'General inquiry'}
        </td>
        <td>
          <select onchange="updateInquiryStatus(${inq.id}, this.value)" class="form-control" style="font-size:0.75rem;padding:0.25rem 0.5rem;width:auto;">
            <option value="NEW" ${inq.status === 'NEW' ? 'selected' : ''}>🔥 New</option>
            <option value="CONTACTED" ${inq.status === 'CONTACTED' ? 'selected' : ''}>📞 Contacted</option>
            <option value="CONVERTED" ${inq.status === 'CONVERTED' ? 'selected' : ''}>✅ Enrolled</option>
            <option value="CLOSED" ${inq.status === 'CLOSED' ? 'selected' : ''}>Closed</option>
          </select>
        </td>
        <td>
          <div class="flex items-center gap-1">
            <a href="https://wa.me/${cleanPhone}" target="_blank" class="btn btn-secondary btn-sm" style="padding:0.2rem 0.45rem;font-size:0.75rem;color:#16A34A;" title="WhatsApp Student">💬</a>
            <button onclick="deleteInquiry(${inq.id})" class="btn btn-secondary btn-sm" style="padding:0.2rem 0.45rem;font-size:0.75rem;color:var(--brand-red);" title="Delete Lead">🗑</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

function filterAdminInquiries(status) {
  currentInquiryStatusFilter = status;

  document.querySelectorAll('#admin-inq-filters button').forEach(btn => {
    if (btn.getAttribute('data-status') === status) {
      btn.className = 'btn btn-sm btn-primary';
    } else {
      btn.className = 'btn btn-sm btn-secondary';
    }
  });

  applyAdminInquiryFilters();
}

function searchAdminInquiries(keyword) {
  applyAdminInquiryFilters();
}

function applyAdminInquiryFilters() {
  const searchInput = document.getElementById('admin-inq-search');
  const keyword = (searchInput ? searchInput.value : '').toLowerCase().trim();

  let filtered = allAdminInquiries;

  if (currentInquiryStatusFilter) {
    filtered = filtered.filter(i => i.status === currentInquiryStatusFilter);
  }

  if (keyword) {
    filtered = filtered.filter(i => 
      i.full_name.toLowerCase().includes(keyword) ||
      i.phone.toLowerCase().includes(keyword) ||
      i.email.toLowerCase().includes(keyword) ||
      i.course_interested.toLowerCase().includes(keyword)
    );
  }

  renderAdminInquiriesTable(filtered);
}

async function updateInquiryStatus(inquiryId, newStatus) {
  try {
    await api.patch(`/inquiries/${inquiryId}/`, { status: newStatus });
    showToast(`Lead status updated to ${newStatus}.`, 'success', 3000);
    // Update local object
    const target = allAdminInquiries.find(i => i.id === inquiryId);
    if (target) target.status = newStatus;
  } catch (err) {
    showToast(err.message || 'Failed to update status.', 'error');
  }
}

async function deleteInquiry(inquiryId) {
  if (!confirm('Delete this inquiry record?')) return;

  try {
    await api.delete(`/inquiries/${inquiryId}/`);
    showToast('Inquiry lead deleted.', 'info');
    loadAdminInquiriesTab();
  } catch (err) {
    showToast(err.message || 'Failed to delete inquiry.', 'error');
  }
}

// ─────────────────────────────────────────────────────────
// 8. NOTICE BOARD & BROADCASTS
// ─────────────────────────────────────────────────────────
async function loadAdminNoticesTab() {
  const container = document.getElementById('admin-notices-container');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const data = await api.get('/notices/');
    allAdminNotices = data.results || data;

    if (allAdminNotices.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center" style="border:1px dashed var(--border-color);">No published circulars found.</div>`;
      return;
    }

    container.innerHTML = allAdminNotices.map(n => {
      let badgeClass = n.category === 'URGENT' ? 'badge-danger' : (n.category === 'EXAM' ? 'badge-primary' : 'badge-gold');
      let audience = n.target_role === 'STUDENT' ? '🎓 Students' : (n.target_role === 'TEACHER' ? '👨‍🏫 Faculty' : '🌐 All Portals');
      
      return `
        <div class="card p-3" style="border-left:4px solid var(--primary-600);border-radius:12px;margin-bottom:0.75rem;">
          <div class="flex items-center justify-between" style="margin-bottom:0.4rem;">
            <div class="flex items-center gap-1">
              <span class="badge ${badgeClass}" style="font-size:0.7rem;">${n.category_display || n.category}</span>
              <span class="badge badge-secondary" style="font-size:0.68rem;">${audience}</span>
              ${n.is_pinned ? '<span class="badge badge-gold" style="font-size:0.68rem;">📌 PINNED</span>' : ''}
            </div>
            <div class="flex items-center gap-2">
              <span style="font-size:0.72rem;color:var(--text-muted);">${formatDate(n.published_date)}</span>
              <button onclick="deleteAdminNotice(${n.id})" class="btn btn-secondary btn-sm" style="padding:0.15rem 0.45rem;font-size:0.72rem;color:var(--brand-red);" title="Delete Notice">🗑</button>
            </div>
          </div>

          <h4 style="font-size:0.95rem;font-weight:700;margin:0.25rem 0 0.35rem;color:var(--text-main);">${n.title}</h4>
          <p style="font-size:0.825rem;color:var(--text-muted);line-height:1.5;margin:0;">${n.content}</p>
        </div>
      `;
    }).join('');
  } catch (err) {
    console.error('Error loading notices:', err);
    container.innerHTML = `<div class="card p-4 text-center text-danger">Failed to load notices.</div>`;
  }
}

async function submitAdminNoticeForm(e) {
  e.preventDefault();
  const btn = document.getElementById('adm-ann-submit-btn');
  const origText = btn.innerHTML;

  const payload = {
    title: document.getElementById('adm-ann-title').value.trim(),
    category: document.getElementById('adm-ann-category').value,
    target_role: document.getElementById('adm-ann-target').value,
    content: document.getElementById('adm-ann-content').value.trim(),
    attachment_url: document.getElementById('adm-ann-attachment').value.trim() || null,
    is_pinned: document.getElementById('adm-ann-pin').checked
  };

  try {
    btn.disabled = true;
    btn.innerHTML = 'Broadcasting... ⏳';

    await api.post('/notices/', payload);
    showToast('🎉 Notice circular broadcasted to portal dashboards!', 'success', 5000);
    document.getElementById('admin-ann-form').reset();
    loadAdminNoticesTab();
  } catch (err) {
    showToast(err.message || 'Failed to post notice', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

async function deleteAdminNotice(noticeId) {
  if (!confirm('Are you sure you want to delete this notice circular?')) return;

  try {
    await api.delete(`/notices/${noticeId}/`);
    showToast('Notice circular deleted.', 'info');
    loadAdminNoticesTab();
  } catch (err) {
    showToast(err.message || 'Failed to delete notice.', 'error');
  }
}
