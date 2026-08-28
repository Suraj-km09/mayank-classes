/**
 * Student Learning & Management Portal Logic
 */

let studentUser = null;
let currentLmsCourseId = null;
let currentActiveVideo = null;
let activeQuizState = null;
let quizTimerInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
  if (!AuthManager.protectPage('STUDENT')) return;
  studentUser = AuthManager.getUser();

  // Populate topbar profile info
  updateStudentProfileUI();

  // Load Dashboard Overview initially
  loadStudentDashboard();
});

function updateStudentProfileUI() {
  const nameEl = document.getElementById('user-display-name');
  const roleEl = document.getElementById('user-display-role');
  const avatarEl = document.getElementById('user-display-avatar');
  const rollEl = document.getElementById('student-roll-badge');

  if (nameEl) nameEl.innerText = studentUser.full_name;
  if (roleEl) roleEl.innerText = 'Student';
  if (avatarEl && studentUser.avatar_url) avatarEl.src = studentUser.avatar_url;
  if (rollEl && studentUser.student_profile) rollEl.innerText = studentUser.student_profile.roll_number;
}

// 1. Navigation Tab Switching
function switchStudentTab(tabId) {
  if (typeof closeSidebar === 'function') {
    closeSidebar();
  }

  document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.sidebar-nav-item a').forEach(el => el.classList.remove('active'));

  const targetPane = document.getElementById(`pane-${tabId}`);
  const targetNav = document.getElementById(`nav-${tabId}`);

  if (targetPane) targetPane.classList.remove('hidden');
  if (targetNav) targetNav.classList.add('active');

  // Trigger tab-specific loaders
  if (tabId === 'dashboard') loadStudentDashboard();
  if (tabId === 'courses') loadStudentCourses();
  if (tabId === 'lms') loadStudentLMS();
  if (tabId === 'tests') loadStudentTests();
  if (tabId === 'materials') loadStudentMaterials();
  if (tabId === 'attendance') loadStudentAttendance();
  if (tabId === 'fees') loadStudentFees();
  if (tabId === 'certificates') loadStudentCertificates();
  if (tabId === 'notices') loadStudentNoticesTab();
}

// 2. Load Dashboard Overview
async function loadStudentCourses() {
  const container = document.getElementById('courses-list-container');
  if (!container) return;
  try {
    const stats = await api.get('/student/stats/');
    const courses = stats.enrolled_courses;
    if (courses.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center" style="grid-column: 1 / -1;">You are not enrolled in any courses yet.</div>`;
      return;
    }
    container.innerHTML = courses.map(c => `
      <div class="card" style="overflow:hidden; display:flex; flex-direction:column; border:1px solid #E2E8F0; border-radius:16px;">
        <img src="${c.thumbnail_url || 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=100'}" style="width:100%;height:180px;object-fit:cover;">
        <div style="padding:1.5rem; flex: 1; display:flex; flex-direction:column;">
          <h4 style="font-size:1.25rem;font-weight:900;color:var(--text-color);margin-bottom:0.5rem;">${c.course_title}</h4>
          <span class="badge badge-primary" style="align-self:flex-start;margin-bottom:1rem;">${c.batch_name}</span>
          <p style="font-size:0.9rem;color:var(--text-muted);margin-bottom:1.25rem; flex:1; line-height:1.5;">
            <strong>⏱ Schedule:</strong> ${c.schedule_time}<br>
            <strong>📍 Classroom:</strong> ${c.classroom}
          </p>
          <button onclick="openLmsForCourse(${c.course_id})" class="btn btn-primary" style="width:100%; justify-content:center; padding:0.75rem;">Open LMS Curriculum ➔</button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center" style="grid-column: 1 / -1;">Failed to load enrolled courses.</div>`;
    console.error('Error loading student courses:', err);
  }
}

async function loadStudentDashboard() {
  try {
    const stats = await api.get('/student/stats/');
    const kpis = stats.kpis;

    document.getElementById('kpi-attendance').innerText = `${kpis.attendance_pct}%`;
    document.getElementById('kpi-lms-progress').innerText = `${kpis.lms_progress_pct}%`;
    document.getElementById('kpi-completed-lessons').innerText = `${kpis.completed_lessons} / ${kpis.total_lessons}`;
    document.getElementById('kpi-pending-fees').innerText = formatCurrency(kpis.pending_fee_inr);
    document.getElementById('kpi-tests-avg').innerText = `${kpis.avg_test_percentage}% (${kpis.tests_completed} Tests)`;

    // Render Enrolled Courses
    const coursesList = document.getElementById('dashboard-enrolled-courses');
    if (coursesList) {
      if (stats.enrolled_courses.length === 0) {
        coursesList.innerHTML = `<div class="card p-4 text-center">You are not currently enrolled in any active batch.</div>`;
      } else {
        coursesList.innerHTML = stats.enrolled_courses.map(c => `
          <div class="card p-3 flex items-center justify-between" style="padding:1rem 1.25rem;">
            <div class="flex items-center gap-3">
              <img src="${c.thumbnail_url || 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=100'}" style="width:64px;height:48px;border-radius:var(--radius-sm);object-fit:cover;">
              <div>
                <h4 style="font-size:1rem;font-weight:700;">${c.course_title}</h4>
                <p style="font-size:0.8rem;color:var(--text-muted);">${c.batch_name} • ${c.schedule_time}</p>
              </div>
            </div>
            <button onclick="openLmsForCourse(${c.course_id})" class="btn btn-primary btn-sm">Watch Lessons</button>
          </div>
        `).join('');
      }
    }

    // Render Notices
    const noticesList = document.getElementById('dashboard-notices');
    if (noticesList && stats.recent_notices) {
      noticesList.innerHTML = stats.recent_notices.map(n => `
        <div style="padding:0.75rem 0;border-bottom:1px solid var(--border-color);">
          <div class="flex items-center justify-between">
            <span class="badge badge-primary" style="font-size:0.7rem;">${n.category_display}</span>
            <span style="font-size:0.75rem;color:var(--text-muted);">${n.published_date}</span>
          </div>
          <h4 style="font-size:0.925rem;font-weight:700;margin:0.25rem 0;">${n.title}</h4>
          <p style="font-size:0.825rem;color:var(--text-muted);line-height:1.4;">${n.content}</p>
        </div>
      `).join('');
    }
  } catch (err) {
    console.error('Error loading student dashboard:', err);
  }
}

// 3. LMS Video Player Module
async function loadStudentLMS(courseId = null) {
  try {
    if (!courseId) {
      // Pick first enrolled course or default course 1
      const courses = await api.get('/courses/');
      const list = courses.results || courses;
      if (list.length > 0) courseId = list[0].id;
    }

    currentLmsCourseId = courseId;
    const curriculum = await api.get(`/courses/${courseId}/curriculum/`);
    renderLmsCurriculum(curriculum);
  } catch (err) {
    showToast('Failed to load course lessons.', 'error');
  }
}

function openLmsForCourse(courseId) {
  switchStudentTab('lms');
  loadStudentLMS(courseId);
}

function renderLmsCurriculum(curriculum) {
  const drawer = document.getElementById('lms-curriculum-container');
  const courseTitleEl = document.getElementById('lms-current-course-title');
  if (courseTitleEl) courseTitleEl.innerText = curriculum.course_title;

  let firstLesson = null;
  let html = '';

  curriculum.subjects.forEach(subject => {
    html += `
      <div style="margin-bottom:1rem;">
        <h4 style="font-size:0.95rem;font-weight:800;color:${subject.color_accent};margin-bottom:0.5rem;">
          📖 ${subject.name}
        </h4>
    `;

    subject.chapters.forEach(chapter => {
      html += `
        <div class="chapter-accordion">
          <div class="chapter-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
            <span>Ch ${chapter.chapter_number}: ${chapter.title}</span>
            <span style="font-size:0.75rem;color:var(--text-muted);">${chapter.lessons.length} videos</span>
          </div>
          <ul class="lesson-list">
            ${chapter.lessons.map(lesson => {
        if (!firstLesson) firstLesson = lesson;
        const isDone = lesson.user_progress && lesson.user_progress.is_completed;
        return `
                <li class="lesson-item ${currentActiveVideo && currentActiveVideo.id === lesson.id ? 'active' : ''}" id="lesson-item-${lesson.id}" onclick="playLmsLesson(${JSON.stringify(lesson).replace(/"/g, '&quot;')})">
                  <div class="flex items-center gap-2">
                    <span class="lesson-check-icon ${isDone ? 'completed' : 'pending'}">${isDone ? '✓' : '○'}</span>
                    <span>${lesson.title}</span>
                  </div>
                  <span style="font-size:0.75rem;color:var(--text-muted);">${lesson.duration_minutes}m</span>
                </li>
              `;
      }).join('')}
          </ul>
        </div>
      `;
    });

    html += `</div>`;
  });

  if (drawer) drawer.innerHTML = html;

  if (firstLesson && !currentActiveVideo) {
    playLmsLesson(firstLesson);
  }
}

function playLmsLesson(lesson) {
  currentActiveVideo = lesson;

  // Highlight in drawer
  document.querySelectorAll('.lesson-item').forEach(el => el.classList.remove('active'));
  const activeEl = document.getElementById(`lesson-item-${lesson.id}`);
  if (activeEl) activeEl.classList.add('active');

  // Update Player UI
  const titleEl = document.getElementById('player-video-title');
  const descEl = document.getElementById('player-video-desc');
  const teacherEl = document.getElementById('player-video-teacher');
  const durationEl = document.getElementById('player-video-duration');
  const iframeEl = document.getElementById('player-video-iframe');
  const completeBtn = document.getElementById('player-complete-btn');

  if (titleEl) titleEl.innerText = lesson.title;
  if (descEl) descEl.innerText = lesson.description || 'Comprehensive video module with theoretical derivations and problem-solving techniques.';
  if (teacherEl) teacherEl.innerText = `Faculty: ${lesson.teacher_name || 'Senior Institute Faculty'}`;
  if (durationEl) durationEl.innerText = `Duration: ${lesson.duration_minutes} Minutes`;

  if (iframeEl) {
    iframeEl.src = lesson.video_url || 'https://www.youtube.com/embed/dQw4w9WgXcQ';
  }

  if (completeBtn) {
    const isDone = lesson.user_progress && lesson.user_progress.is_completed;
    updateCompleteBtnState(isDone);
  }
}

function updateCompleteBtnState(isDone) {
  const completeBtn = document.getElementById('player-complete-btn');
  if (!completeBtn) return;

  if (isDone) {
    completeBtn.innerHTML = '✅ Lesson Completed';
    completeBtn.className = 'btn btn-secondary btn-sm';
  } else {
    completeBtn.innerHTML = 'Mark as Completed (+Progress)';
    completeBtn.className = 'btn btn-primary btn-sm';
  }
}

async function markCurrentVideoComplete() {
  if (!currentActiveVideo) return;

  try {
    const res = await api.post(`/videos/${currentActiveVideo.id}/progress/`, {
      is_completed: true,
      watched_duration_seconds: currentActiveVideo.duration_minutes * 60
    });

    if (!currentActiveVideo.user_progress) currentActiveVideo.user_progress = {};
    currentActiveVideo.user_progress.is_completed = true;

    updateCompleteBtnState(true);
    showToast('Lesson marked as completed! Progress updated.', 'success');

    // Update checkmark in drawer
    const activeEl = document.getElementById(`lesson-item-${currentActiveVideo.id}`);
    if (activeEl) {
      const checkIcon = activeEl.querySelector('.lesson-check-icon');
      if (checkIcon) {
        checkIcon.className = 'lesson-check-icon completed';
        checkIcon.innerText = '✓';
      }
    }
  } catch (err) {
    showToast('Failed to update progress', 'error');
  }
}

// 4. Online Test & Quiz Engine
async function loadStudentTests() {
  const container = document.getElementById('tests-list-container');
  if (!container) return;

  try {
    const data = await api.get('/tests/');
    const tests = data.results || data;

    if (tests.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center">No tests scheduled at the moment.</div>`;
      return;
    }

    container.innerHTML = tests.map(test => {
      const attempt = test.user_attempt_status;
      let actionBtn = `<button onclick="startOnlineTest(${test.id})" class="btn btn-primary btn-sm">Start Test Now</button>`;
      let statusBadge = `<span class="badge badge-info">Not Attempted</span>`;

      if (attempt && attempt.status === 'SUBMITTED') {
        statusBadge = attempt.is_passed ?
          `<span class="badge badge-success">Passed (${attempt.score}/${attempt.total_possible_marks})</span>` :
          `<span class="badge badge-danger">Failed (${attempt.score}/${attempt.total_possible_marks})</span>`;

        actionBtn = `
          <button onclick="viewTestScorecard(${attempt.attempt_id})" class="btn btn-secondary btn-sm">View Scorecard</button>
          <button onclick="startOnlineTest(${test.id})" class="btn btn-outline btn-sm">Retake</button>
        `;
      }

      return `
        <div class="card p-4 flex items-center justify-between" style="padding:1.25rem;">
          <div>
            <div class="flex items-center gap-2" style="margin-bottom:0.35rem;">
              ${statusBadge}
              <span style="font-size:0.75rem;color:var(--text-muted);">${test.course_title}</span>
            </div>
            <h3 style="font-size:1.15rem;font-weight:700;margin-bottom:0.25rem;">${test.title}</h3>
            <p style="font-size:0.85rem;color:var(--text-muted);">
              ⏱ ${test.duration_minutes} Mins • 📝 ${test.questions_count} Questions • 🎯 Max Marks: ${test.total_marks} (Pass: ${test.passing_marks})
            </p>
          </div>
          <div class="flex gap-2 items-center">
            ${actionBtn}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center">Failed to load tests.</div>`;
  }
}

async function startOnlineTest(testId) {
  try {
    showToast('Loading test paper & starting timer...', 'info');
    const data = await api.post(`/tests/${testId}/start/`, {});

    activeQuizState = {
      testId: data.test_id,
      attemptId: data.attempt_id,
      title: data.test_title,
      durationSeconds: data.duration_minutes * 60,
      questions: data.questions,
      currentIndex: 0,
      answers: {} // { questionId: selectedOption }
    };

    renderLiveQuizUI();
  } catch (err) {
    showToast(err.message || 'Could not start test', 'error');
  }
}

function renderLiveQuizUI() {
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
  const quizPane = document.getElementById('pane-live-quiz');
  quizPane.classList.remove('hidden');

  document.getElementById('quiz-title-display').innerText = activeQuizState.title;
  startQuizTimer();
  renderCurrentQuestion();
  renderQuizPalette();
}

function startQuizTimer() {
  if (quizTimerInterval) clearInterval(quizTimerInterval);

  const timerEl = document.getElementById('quiz-timer-display');
  quizTimerInterval = setInterval(() => {
    if (activeQuizState.durationSeconds <= 0) {
      clearInterval(quizTimerInterval);
      showToast('Time is up! Automatically submitting your test.', 'warning');
      submitActiveQuiz();
      return;
    }
    activeQuizState.durationSeconds--;
    const mins = Math.floor(activeQuizState.durationSeconds / 60);
    const secs = activeQuizState.durationSeconds % 60;
    if (timerEl) timerEl.innerText = `⏱ ${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }, 1000);
}

function renderCurrentQuestion() {
  const q = activeQuizState.questions[activeQuizState.currentIndex];
  if (!q) return;

  document.getElementById('question-num-badge').innerText = `Question ${activeQuizState.currentIndex + 1} of ${activeQuizState.questions.length} • (+${q.marks} / -${q.negative_marks} Marks)`;
  document.getElementById('question-text-box').innerText = q.question_text;

  const currentSelected = activeQuizState.answers[q.id] || null;

  const options = [
    { key: 'A', text: q.option_a },
    { key: 'B', text: q.option_b },
    { key: 'C', text: q.option_c },
    { key: 'D', text: q.option_d },
  ];

  const optionsContainer = document.getElementById('question-options-container');
  optionsContainer.innerHTML = options.map(opt => `
    <div class="option-choice-label ${currentSelected === opt.key ? 'selected' : ''}" onclick="selectQuizOption(${q.id}, '${opt.key}')">
      <span class="option-key-circle">${opt.key}</span>
      <span>${opt.text}</span>
    </div>
  `).join('');

  // Prev / Next button states
  document.getElementById('btn-quiz-prev').disabled = (activeQuizState.currentIndex === 0);
  const nextBtn = document.getElementById('btn-quiz-next');
  if (activeQuizState.currentIndex === activeQuizState.questions.length - 1) {
    nextBtn.innerText = 'Review & Submit';
    nextBtn.className = 'btn btn-primary';
  } else {
    nextBtn.innerText = 'Next Question →';
    nextBtn.className = 'btn btn-secondary';
  }
}

function selectQuizOption(questionId, optionKey) {
  if (activeQuizState.answers[questionId] === optionKey) {
    delete activeQuizState.answers[questionId]; // Deselect
  } else {
    activeQuizState.answers[questionId] = optionKey;
  }
  renderCurrentQuestion();
  renderQuizPalette();
}

function renderQuizPalette() {
  const palette = document.getElementById('quiz-palette-container');
  if (!palette) return;

  palette.innerHTML = activeQuizState.questions.map((q, idx) => {
    const isAnswered = !!activeQuizState.answers[q.id];
    const isCurrent = (activeQuizState.currentIndex === idx);

    return `
      <button onclick="jumpToQuizQuestion(${idx})" class="palette-num-btn ${isAnswered ? 'answered' : ''} ${isCurrent ? 'current' : ''}">
        ${idx + 1}
      </button>
    `;
  }).join('');
}

function jumpToQuizQuestion(idx) {
  activeQuizState.currentIndex = idx;
  renderCurrentQuestion();
  renderQuizPalette();
}

function nextQuizQuestion() {
  if (activeQuizState.currentIndex < activeQuizState.questions.length - 1) {
    activeQuizState.currentIndex++;
    renderCurrentQuestion();
    renderQuizPalette();
  } else {
    confirmAndSubmitQuiz();
  }
}

function prevQuizQuestion() {
  if (activeQuizState.currentIndex > 0) {
    activeQuizState.currentIndex--;
    renderCurrentQuestion();
    renderQuizPalette();
  }
}

function confirmAndSubmitQuiz() {
  const answeredCount = Object.keys(activeQuizState.answers).length;
  const total = activeQuizState.questions.length;
  if (confirm(`You have answered ${answeredCount} of ${total} questions. Are you sure you want to finish and submit?`)) {
    submitActiveQuiz();
  }
}

async function submitActiveQuiz() {
  if (quizTimerInterval) clearInterval(quizTimerInterval);

  const formattedAnswers = Object.entries(activeQuizState.answers).map(([qId, choice]) => ({
    question_id: parseInt(qId),
    selected_option: choice
  }));

  try {
    const res = await api.post(`/tests/${activeQuizState.testId}/submit/`, {
      attempt_id: activeQuizState.attemptId,
      answers: formattedAnswers
    });

    showToast('Test successfully submitted and evaluated!', 'success');
    viewTestScorecard(res.id);
  } catch (err) {
    showToast('Failed to submit test: ' + err.message, 'error');
  }
}

// 5. Scorecard & Detailed Solution Breakdown Modal
async function viewTestScorecard(attemptId) {
  try {
    const data = await api.get(`/attempts/${attemptId}/`);

    const answersList = data.answers.map((ans, idx) => {
      const q = ans.question_details || {};
      const statusColor = ans.is_correct ? '#10B981' : (ans.selected_option ? '#EF4444' : '#64748B');
      const statusText = ans.is_correct ? 'Correct (+4)' : (ans.selected_option ? 'Incorrect (-1)' : 'Unattempted (0)');

      return `
        <div style="padding:1.25rem;border:1px solid var(--border-color);border-radius:var(--radius-md);margin-bottom:1rem;background:#F8FAFC;">
          <div class="flex items-center justify-between" style="margin-bottom:0.5rem;">
            <span style="font-weight:700;">Question ${idx + 1}</span>
            <span style="font-weight:700;color:${statusColor};">${statusText}</span>
          </div>
          <p style="font-weight:600;margin-bottom:0.75rem;">${q.question_text}</p>
          <div class="flex flex-col gap-1" style="font-size:0.875rem;margin-bottom:0.75rem;">
            <div>A) ${q.option_a}</div>
            <div>B) ${q.option_b}</div>
            <div>C) ${q.option_c}</div>
            <div>D) ${q.option_d}</div>
          </div>
          <div style="padding:0.75rem;background:#EEF2FF;border-radius:var(--radius-sm);font-size:0.85rem;color:var(--primary-900);">
            <strong>Correct Option:</strong> [${q.correct_option}] &nbsp;|&nbsp; <strong>Your Choice:</strong> [${ans.selected_option || 'None'}]
            <div style="margin-top:0.4rem;"><strong>Solution:</strong> ${q.explanation || 'Refer to theoretical derivation in classroom notes.'}</div>
          </div>
        </div>
      `;
    }).join('');

    const modal = `
      <div class="modal-backdrop" id="scorecard-modal" onclick="if(event.target===this) this.remove()">
        <div class="modal-content" style="max-width:760px;">
          <div class="scorecard-hero">
            <span class="badge ${data.is_passed ? 'badge-success' : 'badge-danger'}" style="margin-bottom:1rem;">
              ${data.is_passed ? 'PASSED DISTINCTION' : 'NEEDS IMPROVEMENT'}
            </span>
            <div class="scorecard-score-circle" style="border-color:${data.is_passed ? '#10B981' : '#EF4444'};">
              <h2>${data.score}</h2>
              <span style="font-size:0.8rem;color:#94A3B8;">out of ${data.total_possible_marks}</span>
            </div>
            <h3 style="font-size:1.5rem;font-weight:800;">${data.test_title}</h3>
            <p style="color:#CBD5E1;font-size:0.9rem;margin-top:0.35rem;">Score Percentage: <strong>${data.percentage}%</strong></p>
          </div>

          <div class="card-body">
            <h4 style="font-size:1.1rem;font-weight:800;margin-bottom:1rem;">Question by Question Analysis</h4>
            ${answersList}
          </div>

          <div class="card-footer text-right">
            <button onclick="document.getElementById('scorecard-modal').remove(); switchStudentTab('tests');" class="btn btn-primary">Close Scorecard</button>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);
  } catch (err) {
    showToast('Failed to load scorecard', 'error');
  }
}

// 6. Study Materials & DPP Downloads
async function loadStudentMaterials() {
  const container = document.getElementById('materials-list-container');
  if (!container) return;

  try {
    const data = await api.get('/study-materials/');
    const items = data.results || data;

    if (items.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center">No study materials uploaded yet.</div>`;
      return;
    }

    container.innerHTML = items.map(m => `
      <div class="card p-4 flex items-center justify-between" style="padding:1.25rem;">
        <div class="flex items-center gap-3">
          <div style="width:48px;height:48px;border-radius:var(--radius-md);background:var(--primary-50);color:var(--primary-700);display:flex;align-items:center;justify-content:center;font-size:1.4rem;">
            📄
          </div>
          <div>
            <span class="badge badge-primary" style="font-size:0.7rem;margin-bottom:0.25rem;">${m.material_type_display}</span>
            <h4 style="font-size:1.05rem;font-weight:700;">${m.title}</h4>
            <p style="font-size:0.8rem;color:var(--text-muted);">${m.subject_name} • ${m.file_size_mb} MB • Uploaded by ${m.teacher_name || 'Faculty'}</p>
          </div>
        </div>
        <a href="${m.file_url}" target="_blank" class="btn btn-primary btn-sm">Download PDF</a>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center">Failed to load materials.</div>`;
  }
}

// 7. Attendance Calendar
async function loadStudentAttendance() {
  const summaryEl = document.getElementById('attendance-stats-summary');
  const recordsEl = document.getElementById('attendance-records-table');

  try {
    const stats = await api.get('/attendance/stats/');
    if (summaryEl) {
      summaryEl.innerHTML = `
        <div class="kpi-grid">
          <div class="kpi-card">
            <div class="kpi-icon-box" style="background:#DCFCE7;color:#15803D;">📅</div>
            <div class="kpi-info">
              <h4>${stats.attendance_percentage}%</h4>
              <p>Overall Attendance</p>
            </div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon-box" style="background:#EEF2FF;color:#4F46E5;">📚</div>
            <div class="kpi-info">
              <h4>${stats.total_classes}</h4>
              <p>Total Scheduled Lectures</p>
            </div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon-box" style="background:#DCFCE7;color:#15803D;">✅</div>
            <div class="kpi-info">
              <h4>${stats.present_count}</h4>
              <p>Lectures Attended</p>
            </div>
          </div>
          <div class="kpi-card">
            <div class="kpi-icon-box" style="background:#FFE4E6;color:#BE123C;">❌</div>
            <div class="kpi-info">
              <h4>${stats.absent_count}</h4>
              <p>Absences Recorded</p>
            </div>
          </div>
        </div>
      `;
    }

    const records = await api.get('/attendance/');
    const attList = records.results || records;

    if (recordsEl) {
      recordsEl.innerHTML = attList.map(r => `
        <tr>
          <td>${formatDate(r.date)}</td>
          <td>${r.roll_number || '-'}</td>
          <td>
            <span class="badge ${r.status === 'PRESENT' ? 'badge-success' : r.status === 'LATE' ? 'badge-warning' : 'badge-danger'}">
              ${r.status_display}
            </span>
          </td>
          <td>${r.remarks || 'Regular Classroom Session'}</td>
        </tr>
      `).join('');
    }
  } catch (err) {
    console.error('Attendance error:', err);
  }
}

// 8. Fees & Invoices
async function loadStudentFees() {
  const container = document.getElementById('fees-invoices-container');
  if (!container) return;

  try {
    const data = await api.get('/fees/');
    const invoices = data.results || data;

    if (invoices.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center">No fee records found.</div>`;
      return;
    }

    container.innerHTML = invoices.map(inv => {
      const isPaid = (inv.status === 'PAID');
      const isPending = (inv.status === 'PENDING' || inv.status === 'OVERDUE');

      return `
        <div class="card p-4" style="padding:1.5rem;margin-bottom:1rem;">
          <div class="flex items-center justify-between" style="margin-bottom:1rem;">
            <div>
              <span class="badge ${isPaid ? 'badge-success' : 'badge-danger'}" style="margin-bottom:0.25rem;">
                ${inv.status_display}
              </span>
              <h3 style="font-size:1.15rem;font-weight:700;">${inv.title}</h3>
              <p style="font-size:0.85rem;color:var(--text-muted);">Invoice #${inv.invoice_number} • Due: ${formatDate(inv.due_date)}</p>
            </div>
            <div class="text-right">
              <div style="font-size:1.4rem;font-weight:800;">${formatCurrency(inv.total_amount)}</div>
              <p style="font-size:0.8rem;color:var(--text-muted);">Paid: ${formatCurrency(inv.paid_amount)}</p>
            </div>
          </div>

          <div class="flex justify-between items-center" style="padding-top:1rem;border-top:1px solid var(--border-color);">
            <span style="font-size:0.85rem;color:var(--text-muted);">
              ${isPaid ? `Payment Mode: ${inv.payment_mode || 'UPI'} • Txn: ${inv.transaction_id || 'TXN-OK'}` : `Due Balance: ${formatCurrency(inv.due_amount)}`}
            </span>
            ${isPending ? `<button onclick="simulateOnlineFeePayment(${inv.id})" class="btn btn-primary btn-sm">Pay Online Now (${formatCurrency(inv.due_amount)})</button>` : `<span class="badge badge-success">Receipt Issued</span>`}
          </div>
        </div>
      `;
    }).join('');
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center">Failed to load fee invoices.</div>`;
  }
}

async function simulateOnlineFeePayment(invoiceId) {
  if (!confirm('Simulate secure online fee payment for this tuition installment?')) return;

  try {
    const res = await api.post(`/fees/${invoiceId}/pay/`, { payment_mode: 'UPI' });
    showToast('Payment successful! Transaction ID: ' + res.invoice.transaction_id, 'success', 5000);
    loadStudentFees();
  } catch (err) {
    showToast(err.message || 'Payment simulation failed', 'error');
  }
}

// 9. Digital Certificates
async function loadStudentCertificates() {
  const container = document.getElementById('certificates-container');
  if (!container) return;

  try {
    const data = await api.get('/certificates/');
    const certs = data.results || data;

    if (certs.length === 0) {
      container.innerHTML = `<div class="card p-4 text-center">Certificates are awarded upon successful completion of term benchmark assessments.</div>`;
      return;
    }

    container.innerHTML = certs.map(c => `
      <div class="certificate-frame">
        <div class="certificate-seal">🏅</div>
        <span class="badge badge-gold" style="margin-bottom:0.75rem;">OFFICIAL DIGITAL CREDENTIAL</span>
        <h2 style="font-size:1.75rem;font-weight:900;margin-bottom:0.5rem;">${c.title}</h2>
        <p style="font-size:1rem;color:var(--text-muted);margin-bottom:1.5rem;">This certifies that</p>
        <h3 style="font-size:1.6rem;color:var(--primary-700);font-weight:800;margin-bottom:0.75rem;">${c.student_name}</h3>
        <p style="font-size:0.95rem;color:var(--text-muted);max-width:520px;margin:0 auto 1.5rem;line-height:1.6;">
          ${c.description}
        </p>
        <div class="flex items-center justify-center gap-6" style="margin-bottom:1.5rem;font-size:0.85rem;color:var(--text-muted);">
          <span><strong>Grade:</strong> ${c.grade}</span>
          <span><strong>Issued:</strong> ${formatDate(c.issue_date)}</span>
          <span><strong>Cert #:</strong> ${c.certificate_number}</span>
        </div>
        <a href="/verify-certificate/${c.verification_code}/" target="_blank" class="btn btn-outline btn-sm">Verify Credential Online ↗</a>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<div class="card p-4 text-center">Failed to load certificates.</div>`;
  }
}

// 10. Notice Board & Announcements Module
let allStudentNotices = [];
let currentNoticeCategoryFilter = '';

async function loadStudentNoticesTab() {
  const container = document.getElementById('student-notices-feed');
  if (!container) return;

  container.innerHTML = `<div class="p-4 text-center"><div class="spinner" style="margin:0 auto;"></div></div>`;

  try {
    const data = await api.get('/notices/');
    allStudentNotices = data.results || data;

    // Update count badge
    const badgeEl = document.getElementById('student-notice-badge');
    if (badgeEl && allStudentNotices.length > 0) {
      badgeEl.innerText = `${allStudentNotices.length}`;
    }

    renderStudentNoticesList(allStudentNotices);
  } catch (err) {
    console.error('Error loading notices:', err);
    container.innerHTML = `<div class="card p-4 text-center" style="color:var(--text-muted);">Failed to load notice board circulars. Please check back later.</div>`;
  }
}

function renderStudentNoticesList(notices) {
  const container = document.getElementById('student-notices-feed');
  if (!container) return;

  if (notices.length === 0) {
    container.innerHTML = `
      <div class="card p-5 text-center" style="border:1px dashed var(--border-color);border-radius:16px;">
        <div style="font-size:2.5rem;margin-bottom:0.75rem;">📢</div>
        <h4 style="font-size:1.15rem;font-weight:700;margin-bottom:0.25rem;">No Notices Found</h4>
        <p style="font-size:0.875rem;color:var(--text-muted);margin:0;">There are no circulars matching the selected filter criteria.</p>
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

    const pinnedMarkup = n.is_pinned ? `
      <span class="badge badge-gold" style="font-size:0.68rem;gap:0.2rem;box-shadow:0 0 10px rgba(245,158,11,0.3);">
        📌 PINNED
      </span>
    ` : '';

    const attachmentMarkup = n.attachment_url ? `
      <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px dashed var(--border-color);">
        <a href="${n.attachment_url}" target="_blank" class="btn btn-secondary btn-sm" style="font-size:0.78rem;gap:0.35rem;">
          📎 Download Official Circular / Attachment ↗
        </a>
      </div>
    ` : '';

    return `
      <div class="card p-4" style="border-left:5px solid ${borderAccent};border-radius:16px;box-shadow:var(--shadow-sm);transition:all 0.2s ease;">
        <div class="flex items-center justify-between" style="flex-wrap:wrap;gap:0.5rem;margin-bottom:0.6rem;">
          <div class="flex items-center gap-2">
            <span class="badge ${badgeClass}">${icon} ${n.category_display || n.category}</span>
            ${pinnedMarkup}
          </div>
          <span style="font-size:0.78rem;color:var(--text-muted);font-weight:600;">
            📅 Published: ${formatDate(n.published_date)}
          </span>
        </div>

        <h3 style="font-size:1.18rem;font-weight:800;color:var(--text-main);margin:0 0 0.5rem;line-height:1.35;">
          ${n.title}
        </h3>

        <div style="font-size:0.9rem;color:#334155;line-height:1.65;white-space:pre-line;">
          ${n.content}
        </div>

        ${attachmentMarkup}
      </div>
    `;
  }).join('');
}

function filterStudentNotices(category) {
  currentNoticeCategoryFilter = category;

  // Update button active styles
  document.querySelectorAll('#student-notice-filters button').forEach(btn => {
    if (btn.getAttribute('data-cat') === category) {
      btn.className = 'btn btn-sm btn-primary';
    } else {
      btn.className = 'btn btn-sm btn-secondary';
    }
  });

  applyStudentNoticeFilters();
}

function searchStudentNotices(keyword) {
  applyStudentNoticeFilters();
}

function applyStudentNoticeFilters() {
  const searchInput = document.getElementById('student-notice-search');
  const keyword = (searchInput ? searchInput.value : '').toLowerCase().trim();

  let filtered = allStudentNotices;

  if (currentNoticeCategoryFilter) {
    filtered = filtered.filter(n => n.category === currentNoticeCategoryFilter);
  }

  if (keyword) {
    filtered = filtered.filter(n =>
      n.title.toLowerCase().includes(keyword) ||
      n.content.toLowerCase().includes(keyword) ||
      (n.category_display && n.category_display.toLowerCase().includes(keyword))
    );
  }

  renderStudentNoticesList(filtered);
}
