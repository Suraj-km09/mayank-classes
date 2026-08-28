/**
 * Teacher & Faculty Management Portal Logic
 */

let teacherUser = null;
let teacherBatches = [];
let allCourses = [];

document.addEventListener('DOMContentLoaded', async () => {
  if (!AuthManager.protectPage('TEACHER')) return;
  teacherUser = AuthManager.getUser();

  updateTeacherProfileUI();
  loadTeacherDashboard();
});

function updateTeacherProfileUI() {
  const nameEl = document.getElementById('user-display-name');
  const roleEl = document.getElementById('user-display-role');
  const avatarEl = document.getElementById('user-display-avatar');
  const desigEl = document.getElementById('teacher-desig-badge');

  if (nameEl) nameEl.innerText = teacherUser.full_name;
  if (roleEl) roleEl.innerText = 'Faculty';
  if (avatarEl && teacherUser.avatar_url) avatarEl.src = teacherUser.avatar_url;
  if (desigEl && teacherUser.teacher_profile) desigEl.innerText = teacherUser.teacher_profile.designation;
}

function switchTeacherTab(tabId) {
  if (typeof closeSidebar === 'function') {
    closeSidebar();
  }

  document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.sidebar-nav-item a').forEach(el => el.classList.remove('active'));

  const targetPane = document.getElementById(`pane-${tabId}`);
  const targetNav = document.getElementById(`nav-${tabId}`);

  if (targetPane) targetPane.classList.remove('hidden');
  if (targetNav) targetNav.classList.add('active');

  if (tabId === 'dashboard') loadTeacherDashboard();
  if (tabId === 'attendance') loadAttendanceMarkerTab();
  if (tabId === 'lessons') loadTeacherLessonsTab();
  if (tabId === 'materials') loadTeacherMaterialsTab();
  if (tabId === 'test-creator') loadTestCreatorTab();
  if (tabId === 'results') loadStudentResultsTab();
  if (tabId === 'announcements') loadTeacherAnnouncementsTab();
}

// 1. Dashboard Overview
async function loadTeacherDashboard() {
  try {
    const stats = await api.get('/teacher/stats/');
    const kpis = stats.kpis;

    document.getElementById('kpi-batches-count').innerText = kpis.assigned_batches_count;
    document.getElementById('kpi-students-count').innerText = kpis.total_students;
    document.getElementById('kpi-videos-count').innerText = kpis.uploaded_videos;
    document.getElementById('kpi-tests-count').innerText = kpis.tests_created;

    teacherBatches = stats.batches;
    const batchesContainer = document.getElementById('teacher-batches-list');
    if (batchesContainer) {
      batchesContainer.innerHTML = stats.batches.map(b => `
        <div class="card p-3 flex items-center justify-between" style="padding:1.25rem;">
          <div>
            <span class="badge badge-primary" style="font-size:0.7rem;">${b.classroom}</span>
            <h4 style="font-size:1.1rem;font-weight:700;margin:0.25rem 0;">${b.name}</h4>
            <p style="font-size:0.85rem;color:var(--text-muted);">${b.course_title} • ${b.schedule_time}</p>
          </div>
          <div class="flex gap-2 items-center">
            <span class="badge badge-info">${b.student_count} Students</span>
            <button onclick="openAttendanceForBatch(${b.id})" class="btn btn-primary btn-sm">Mark Roll Call</button>
          </div>
        </div>
      `).join('');
    }
  } catch (err) {
    console.error('Teacher dashboard error:', err);
  }
}

// 2. Attendance Marker Module
let activeBatchStudents = [];
async function loadAttendanceMarkerTab(preselectedBatchId = null) {
  const batchSelect = document.getElementById('att-batch-select');
  const dateInput = document.getElementById('att-date-input');

  if (!dateInput.value) {
    dateInput.value = new Date().toISOString().split('T')[0];
  }

  // Populate batch options
  try {
    const batches = await api.get('/batches/');
    teacherBatches = batches.results || batches;

    if (batchSelect) {
      batchSelect.innerHTML = teacherBatches.map(b =>
        `<option value="${b.id}" ${preselectedBatchId && preselectedBatchId == b.id ? 'selected' : ''}>${b.name} (${b.course_title})</option>`
      ).join('');

      // Auto-load first batch students
      if (teacherBatches.length > 0) {
        fetchBatchStudentsForAttendance(preselectedBatchId || teacherBatches[0].id);
      }
    }
  } catch (err) {
    showToast('Failed to load batches', 'error');
  }
}

function openAttendanceForBatch(batchId) {
  switchTeacherTab('attendance');
  loadAttendanceMarkerTab(batchId);
}

async function onAttendanceBatchChange() {
  const batchId = document.getElementById('att-batch-select').value;
  fetchBatchStudentsForAttendance(batchId);
}

async function fetchBatchStudentsForAttendance(batchId) {
  const container = document.getElementById('attendance-rollcall-container');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const enrollments = await api.get(`/enrollments/?batch_id=${batchId}`);
    const list = enrollments.results || enrollments;

    activeBatchStudents = list.map(e => ({
      studentId: e.student_details.id,
      name: e.student_details.full_name,
      roll: (e.student_details.student_profile && e.student_details.student_profile.roll_number) || 'MC-000',
      avatar: e.student_details.avatar_url || 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=100',
      status: 'PRESENT',
      remarks: ''
    }));

    renderRollCallGrid();
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center">Failed to load batch students.</div>`;
  }
}

function renderRollCallGrid() {
  const container = document.getElementById('attendance-rollcall-container');
  if (!container) return;

  if (activeBatchStudents.length === 0) {
    container.innerHTML = `<div class="card p-4 text-center w-full">No students enrolled in this batch yet.</div>`;
    return;
  }

  container.innerHTML = activeBatchStudents.map((s, idx) => `
    <div class="student-att-card">
      <div class="flex items-center gap-3">
        <img src="${s.avatar}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">
        <div>
          <h4 style="font-size:0.95rem;font-weight:700;">${s.name}</h4>
          <span style="font-size:0.75rem;color:var(--text-muted);">${s.roll}</span>
        </div>
      </div>
      <div class="att-toggle-group">
        <button type="button" onclick="setStudentAttStatus(${idx}, 'PRESENT')" class="att-btn ${s.status === 'PRESENT' ? 'active-present' : ''}">P</button>
        <button type="button" onclick="setStudentAttStatus(${idx}, 'LATE')" class="att-btn ${s.status === 'LATE' ? 'active-late' : ''}">L</button>
        <button type="button" onclick="setStudentAttStatus(${idx}, 'ABSENT')" class="att-btn ${s.status === 'ABSENT' ? 'active-absent' : ''}">A</button>
      </div>
    </div>
  `).join('');
}

function setStudentAttStatus(idx, status) {
  if (activeBatchStudents[idx]) {
    activeBatchStudents[idx].status = status;
    renderRollCallGrid();
  }
}

function markAllPresent() {
  activeBatchStudents.forEach(s => s.status = 'PRESENT');
  renderRollCallGrid();
  showToast('All students marked Present for today.', 'info');
}

async function saveAttendanceSubmission() {
  const batchId = document.getElementById('att-batch-select').value;
  const dateVal = document.getElementById('att-date-input').value;

  if (!batchId || !dateVal) {
    showToast('Please select a batch and date', 'warning');
    return;
  }

  const payload = {
    batch_id: parseInt(batchId),
    date: dateVal,
    records: activeBatchStudents.map(s => ({
      student_id: s.studentId,
      status: s.status,
      remarks: s.remarks
    }))
  };

  try {
    await api.post('/attendance/', payload);
    showToast(`Attendance saved successfully for ${activeBatchStudents.length} students!`, 'success');
  } catch (err) {
    showToast(err.message || 'Failed to save attendance', 'error');
  }
}

// 3. Teacher Video Lesson Publisher
async function loadTeacherLessonsTab() {
  const selectCourse = document.getElementById('lesson-course-select');
  try {
    const data = await api.get('/courses/');
    allCourses = data.results || data;
    if (selectCourse) {
      selectCourse.innerHTML = allCourses.map(c => `<option value="${c.id}">${c.title}</option>`).join('');
      onLessonCourseSelectChange();
    }
  } catch (e) {
    console.error(e);
  }
}

async function onLessonCourseSelectChange() {
  const courseId = document.getElementById('lesson-course-select').value;
  const selectSubject = document.getElementById('lesson-subject-select');
  const selectChapter = document.getElementById('lesson-chapter-select');

  try {
    const subs = await api.get(`/subjects/?course_id=${courseId}`);
    const subjects = subs.results || subs;
    if (selectSubject) {
      selectSubject.innerHTML = subjects.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
      if (subjects.length > 0) {
        const chaps = await api.get(`/chapters/?subject_id=${subjects[0].id}`);
        const chapters = chaps.results || chaps;
        if (selectChapter) {
          selectChapter.innerHTML = chapters.map(ch => `<option value="${ch.id}">Ch ${ch.chapter_number}: ${ch.title}</option>`).join('');
        }
      }
    }
  } catch (e) {
    console.error(e);
  }
}

async function submitNewLessonForm(e) {
  e.preventDefault();
  const payload = {
    course: parseInt(document.getElementById('lesson-course-select').value),
    subject: parseInt(document.getElementById('lesson-subject-select').value),
    chapter: parseInt(document.getElementById('lesson-chapter-select').value),
    title: document.getElementById('lesson-title-input').value,
    description: document.getElementById('lesson-desc-input').value,
    video_url: document.getElementById('lesson-url-input').value,
    thumbnail_url: document.getElementById('lesson-thumb-input').value || 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500',
    duration_minutes: parseInt(document.getElementById('lesson-duration-input').value || 45),
    is_published: true,
    is_free_preview: document.getElementById('lesson-preview-check').checked
  };

  try {
    await api.post('/videos/', payload);
    showToast('Video lesson published successfully into LMS!', 'success');
    document.getElementById('new-lesson-form').reset();
  } catch (err) {
    showToast(err.message || 'Failed to publish lesson', 'error');
  }
}

// 4. Teacher Study Material Uploader
async function loadTeacherMaterialsTab() {
  const selectCourse = document.getElementById('mat-course-select');
  try {
    const data = await api.get('/courses/');
    allCourses = data.results || data;
    if (selectCourse) {
      selectCourse.innerHTML = allCourses.map(c => `<option value="${c.id}">${c.title}</option>`).join('');
      onMatCourseSelectChange();
    }
  } catch (e) {
    console.error(e);
  }
}

async function onMatCourseSelectChange() {
  const courseId = document.getElementById('mat-course-select').value;
  const selectSubject = document.getElementById('mat-subject-select');
  try {
    const subs = await api.get(`/subjects/?course_id=${courseId}`);
    const subjects = subs.results || subs;
    if (selectSubject) {
      selectSubject.innerHTML = subjects.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
    }
  } catch (e) {
    console.error(e);
  }
}

async function submitNewMaterialForm(e) {
  e.preventDefault();
  const payload = {
    course: parseInt(document.getElementById('mat-course-select').value),
    subject: parseInt(document.getElementById('mat-subject-select').value),
    title: document.getElementById('mat-title-input').value,
    description: document.getElementById('mat-desc-input').value,
    material_type: document.getElementById('mat-type-select').value,
    file_url: document.getElementById('mat-url-input').value || 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
    file_size_mb: 2.5,
    is_published: true
  };

  try {
    await api.post('/study-materials/', payload);
    showToast('Study material document uploaded and available to students!', 'success');
    document.getElementById('new-mat-form').reset();
  } catch (err) {
    showToast(err.message || 'Upload failed', 'error');
  }
}

// 5. Online Test Creator
let testBuilderQuestions = [];

function loadTestCreatorTab() {
  testBuilderQuestions = [];
  renderTestBuilderQuestions();

  const selectCourse = document.getElementById('test-course-select');
  if (selectCourse && allCourses.length > 0) {
    selectCourse.innerHTML = allCourses.map(c => `<option value="${c.id}">${c.title}</option>`).join('');
  }
}

function addQuestionToBuilder() {
  testBuilderQuestions.push({
    question_text: '',
    option_a: '',
    option_b: '',
    option_c: '',
    option_d: '',
    correct_option: 'A',
    marks: 4.0,
    negative_marks: 1.0,
    explanation: ''
  });
  renderTestBuilderQuestions();
}

function renderTestBuilderQuestions() {
  const container = document.getElementById('test-questions-builder-container');
  if (!container) return;

  if (testBuilderQuestions.length === 0) {
    container.innerHTML = `
      <div class="card p-4 text-center" style="background:#F8FAFC;border:2px dashed #CBD5E1;">
        <p style="color:var(--text-muted);margin-bottom:0.75rem;">No questions added yet to this mock test.</p>
        <button type="button" onclick="addQuestionToBuilder()" class="btn btn-secondary btn-sm">+ Add First MCQ Question</button>
      </div>
    `;
    return;
  }

  container.innerHTML = testBuilderQuestions.map((q, idx) => `
    <div class="card p-4" style="margin-bottom:1rem;background:#F8FAFC;">
      <div class="flex items-center justify-between" style="margin-bottom:0.75rem;">
        <span class="badge badge-primary">Question ${idx + 1}</span>
        <button type="button" onclick="removeBuilderQuestion(${idx})" style="color:var(--brand-rose);background:none;border:none;cursor:pointer;font-size:0.85rem;font-weight:700;">Remove</button>
      </div>
      <div class="form-group">
        <textarea class="form-control" placeholder="Enter Question Problem Statement..." oninput="testBuilderQuestions[${idx}].question_text = this.value" required>${q.question_text}</textarea>
      </div>
      <div class="grid grid-2 gap-2" style="margin-bottom:1rem;">
        <input class="form-control" placeholder="Option A" value="${q.option_a}" oninput="testBuilderQuestions[${idx}].option_a = this.value" required>
        <input class="form-control" placeholder="Option B" value="${q.option_b}" oninput="testBuilderQuestions[${idx}].option_b = this.value" required>
        <input class="form-control" placeholder="Option C" value="${q.option_c}" oninput="testBuilderQuestions[${idx}].option_c = this.value" required>
        <input class="form-control" placeholder="Option D" value="${q.option_d}" oninput="testBuilderQuestions[${idx}].option_d = this.value" required>
      </div>
      <div class="grid grid-2 gap-3 items-center">
        <div>
          <label class="form-label" style="font-size:0.8rem;">Correct Choice:</label>
          <select class="form-control" onchange="testBuilderQuestions[${idx}].correct_option = this.value">
            <option value="A" ${q.correct_option === 'A' ? 'selected' : ''}>Option A</option>
            <option value="B" ${q.correct_option === 'B' ? 'selected' : ''}>Option B</option>
            <option value="C" ${q.correct_option === 'C' ? 'selected' : ''}>Option C</option>
            <option value="D" ${q.correct_option === 'D' ? 'selected' : ''}>Option D</option>
          </select>
        </div>
        <div>
          <label class="form-label" style="font-size:0.8rem;">Step Solution / Explanation:</label>
          <input class="form-control" placeholder="Step-by-step formula explanation" value="${q.explanation}" oninput="testBuilderQuestions[${idx}].explanation = this.value">
        </div>
      </div>
    </div>
  `).join('');
}

function removeBuilderQuestion(idx) {
  testBuilderQuestions.splice(idx, 1);
  renderTestBuilderQuestions();
}

async function submitTestCreatorForm(e) {
  e.preventDefault();
  if (testBuilderQuestions.length === 0) {
    showToast('Please add at least 1 question to the test', 'warning');
    return;
  }

  const courseId = document.getElementById('test-course-select').value;
  const title = document.getElementById('test-title-input').value;
  const duration = parseInt(document.getElementById('test-duration-input').value || 60);
  const passMarks = parseInt(document.getElementById('test-pass-input').value || 16);

  try {
    const newTest = await api.post('/tests/', {
      course: parseInt(courseId),
      title: title,
      duration_minutes: duration,
      total_marks: testBuilderQuestions.length * 4,
      passing_marks: passMarks,
      is_published: true
    });

    showToast(`Test "${title}" created successfully!`, 'success');
    document.getElementById('new-test-form').reset();
    testBuilderQuestions = [];
    renderTestBuilderQuestions();
  } catch (err) {
    showToast(err.message || 'Failed to create test', 'error');
  }
}

// 6. Student Results & Performance Analytics
async function loadStudentResultsTab() {
  const container = document.getElementById('results-table-body');
  if (!container) return;

  try {
    const data = await api.get('/attempts/');
    const attempts = data.results || data;

    container.innerHTML = attempts.map(a => `
      <tr>
        <td>
          <strong>${a.student_details.full_name}</strong>
          <div style="font-size:0.75rem;color:var(--text-muted);">${(a.student_details.student_profile && a.student_details.student_profile.roll_number) || '-'}</div>
        </td>
        <td>${a.test_title}</td>
        <td><strong>${a.score}</strong> / ${a.total_possible_marks}</td>
        <td>${a.percentage}%</td>
        <td>
          <span class="badge ${a.is_passed ? 'badge-success' : 'badge-danger'}">
            ${a.is_passed ? 'Passed' : 'Failed'}
          </span>
        </td>
        <td>${formatDate(a.submit_time)}</td>
      </tr>
    `).join('');
  } catch (e) {
    console.error(e);
  }
}

// 7. Announcements
// 7. Announcements & Notice Board Management
let allTeacherNotices = [];
let currentTeacherNoticeFilter = '';

async function loadTeacherAnnouncementsTab() {
  const container = document.getElementById('teacher-notices-container');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const data = await api.get('/notices/');
    allTeacherNotices = data.results || data;

    const countBadge = document.getElementById('teacher-notices-count-badge');
    if (countBadge) {
      countBadge.innerText = `${allTeacherNotices.length} Active Circulars`;
    }

    renderTeacherNoticesList(allTeacherNotices);
  } catch (e) {
    console.error('Error loading teacher notices:', e);
    container.innerHTML = `<div class="card p-3 text-center" style="color:var(--text-muted);">Failed to load published notices.</div>`;
  }
}

function renderTeacherNoticesList(notices) {
  const container = document.getElementById('teacher-notices-container');
  if (!container) return;

  if (notices.length === 0) {
    container.innerHTML = `
      <div class="card p-4 text-center" style="border:1px dashed var(--border-color);">
        <p style="font-size:0.875rem;color:var(--text-muted);margin:0;">No published notices found under this filter.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = notices.map(n => {
    let badgeClass = 'badge-primary';
    let icon = '📌';
    let borderAccent = 'var(--primary-500)';

    if (n.category === 'URGENT') {
      badgeClass = 'badge-danger';
      icon = '🚨';
      borderAccent = 'var(--brand-red)';
    } else if (n.category === 'EXAM') {
      badgeClass = 'badge-primary';
      icon = '📝';
      borderAccent = 'var(--cat-jee)';
    } else if (n.category === 'EVENT') {
      badgeClass = 'badge-gold';
      icon = '⚡';
      borderAccent = 'var(--brand-gold-dark)';
    } else if (n.category === 'HOLIDAY') {
      badgeClass = 'badge-success';
      icon = '🎉';
      borderAccent = 'var(--brand-emerald)';
    }

    const pinnedMarkup = n.is_pinned ? `<span class="badge badge-gold" style="font-size:0.68rem;">📌 PINNED</span>` : '';
    const audienceLabel = n.target_role === 'STUDENT' ? '🎓 Students' : (n.target_role === 'TEACHER' ? '👨‍🏫 Faculty' : '🌐 All');

    const attachmentMarkup = n.attachment_url ? `
      <div style="margin-top:0.6rem;padding-top:0.5rem;border-top:1px dashed var(--border-color);">
        <a href="${n.attachment_url}" target="_blank" style="font-size:0.78rem;color:var(--primary-600);font-weight:600;text-decoration:underline;">
          📎 Attached Document Link ↗
        </a>
      </div>
    ` : '';

    return `
      <div class="card p-3" style="border-left:4px solid ${borderAccent};border-radius:12px;margin-bottom:0.75rem;">
        <div class="flex items-center justify-between" style="flex-wrap:wrap;gap:0.4rem;margin-bottom:0.4rem;">
          <div class="flex items-center gap-1">
            <span class="badge ${badgeClass}" style="font-size:0.7rem;">${icon} ${n.category_display || n.category}</span>
            <span class="badge badge-secondary" style="font-size:0.68rem;">${audienceLabel}</span>
            ${pinnedMarkup}
          </div>
          <div class="flex items-center gap-2">
            <span style="font-size:0.74rem;color:var(--text-muted);">${formatDate(n.published_date)}</span>
            <button onclick="deleteNotice(${n.id})" class="btn btn-secondary btn-sm" style="padding:0.15rem 0.45rem;font-size:0.72rem;color:var(--brand-red);" title="Delete Notice">🗑</button>
          </div>
        </div>

        <h4 style="font-size:0.95rem;font-weight:700;margin:0.25rem 0 0.35rem;color:var(--text-main);">${n.title}</h4>
        <p style="font-size:0.825rem;color:var(--text-muted);line-height:1.5;margin:0;">${n.content}</p>

        ${attachmentMarkup}
      </div>
    `;
  }).join('');
}

function filterTeacherNotices(category) {
  currentTeacherNoticeFilter = category;

  document.querySelectorAll('#teacher-notice-filters button').forEach(btn => {
    if (btn.getAttribute('data-tcat') === category) {
      btn.className = 'btn btn-sm btn-primary';
    } else {
      btn.className = 'btn btn-sm btn-secondary';
    }
  });

  let filtered = allTeacherNotices;
  if (category) {
    filtered = filtered.filter(n => n.category === category);
  }
  renderTeacherNoticesList(filtered);
}

async function deleteNotice(noticeId) {
  if (!confirm('Are you sure you want to delete this notice circular?')) return;

  try {
    await api.delete(`/notices/${noticeId}/`);
    showToast('Notice circular deleted successfully.', 'info');
    loadTeacherAnnouncementsTab();
  } catch (err) {
    console.error('Error deleting notice:', err);
    showToast(err.message || 'Failed to delete notice.', 'error');
  }
}

async function submitAnnouncementForm(e) {
  e.preventDefault();
  const submitBtn = document.getElementById('ann-submit-btn');
  const origText = submitBtn.innerHTML;

  const payload = {
    title: document.getElementById('ann-title-input').value.trim(),
    category: document.getElementById('ann-category-select').value,
    target_role: document.getElementById('ann-target-select').value,
    content: document.getElementById('ann-content-input').value.trim(),
    attachment_url: document.getElementById('ann-attachment-input').value.trim() || null,
    is_pinned: document.getElementById('ann-pin-check').checked
  };

  try {
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Broadcasting Notice... ⏳';

    await api.post('/notices/', payload);
    showToast('🎉 Notice published and broadcasted to student & faculty dashboards!', 'success', 5000);
    document.getElementById('new-ann-form').reset();
    loadTeacherAnnouncementsTab();
  } catch (err) {
    showToast(err.message || 'Failed to broadcast notice', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = origText;
  }
}
