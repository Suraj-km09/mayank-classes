/**
 * Mayank Classes Public Website & Course Ecosystem JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initContactForm();
});

// Global Counseling & Demo Modal Handlers
function openGlobalDemoModal(courseName = '') {
  const modal = document.getElementById('global-demo-modal');
  if (!modal) return;
  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
  if (courseName) {
    const sel = document.getElementById('g_course');
    if (sel) {
      let matched = false;
      for (let opt of sel.options) {
        if (courseName.toLowerCase().includes(opt.value.toLowerCase()) || opt.value.toLowerCase().includes(courseName.toLowerCase())) {
          sel.value = opt.value;
          matched = true;
          break;
        }
      }
      if (!matched && sel.options.length > 0) {
        const newOpt = new Option(courseName, courseName, true, true);
        sel.add(newOpt);
      }
    }
  }
}

function closeGlobalDemoModal() {
  const modal = document.getElementById('global-demo-modal');
  if (modal) modal.style.display = 'none';
  document.body.style.overflow = '';
}

// Global ESC key listener to close modals
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeGlobalDemoModal();
    closeBrochureModal();
    closeVideoPreviewModal();
  }
});

async function handleGlobalDemoSubmit(e) {
  e.preventDefault();
  const form = document.getElementById('global-demo-form');
  const submitBtn = form ? form.querySelector('button[type="submit"]') : null;
  const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Confirm Free Demo Request ➔';

  const name = document.getElementById('g_name').value.trim();
  const phone = document.getElementById('g_phone').value.trim();
  const email = document.getElementById('g_email').value.trim();
  const course = document.getElementById('g_course').value;
  const currClass = document.getElementById('g_class').value;
  const msg = document.getElementById('g_message').value.trim();

  if (!name || !phone || !email) {
    showToast('Please fill all required fields.', 'error');
    return;
  }

  const payload = {
    full_name: name,
    email: email,
    phone: phone,
    course_interested: course,
    current_class: currClass,
    message: msg || `Demo class request for ${course}`
  };

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = '⏳ Reserving Seat...';
  }

  try {
    await api.post('/inquiries/', payload);
    showToast('🎉 Demo seat reserved! Our academic counselor will call you within 24 hours.', 'success', 6000);
    closeGlobalDemoModal();
    if (form) form.reset();
  } catch (err) {
    showToast(err.message || 'Submission failed. Please check your phone number and email.', 'error');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  }
}

// Global Brochure Download Modal Handlers
function openBrochureModal() {
  const modal = document.getElementById('brochure-modal');
  if (modal) modal.style.display = 'flex';
}

function closeBrochureModal() {
  const modal = document.getElementById('brochure-modal');
  if (modal) modal.style.display = 'none';
}

async function handleBrochureSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('b_name').value;
  const phone = document.getElementById('b_phone').value;

  const payload = {
    full_name: name,
    email: `${phone}@brochure.mayankclasses.com`,
    phone: phone,
    course_interested: 'Full Syllabus Brochure 2026',
    current_class: 'All',
    message: 'Brochure Download Request'
  };

  try {
    await api.post('/inquiries/', payload);
    showToast(`Thank you ${name}! PDF download started and sent to WhatsApp.`, 'success', 6000);
    closeBrochureModal();
    const form = document.getElementById('brochure-form');
    if (form) form.reset();
    // Trigger download of dummy PDF
    const link = document.createElement('a');
    link.href = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf';
    link.download = 'Mayank-Classes-Curriculum-Brochure-2026.pdf';
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    showToast('Download initiated!', 'info');
    closeBrochureModal();
  }
}

// Global Demo Video Player Modal
function playDemoVideo(title, videoUrl) {
  const modal = document.getElementById('video-preview-modal');
  const titleEl = document.getElementById('video-modal-title');
  const iframeEl = document.getElementById('video-modal-iframe');
  if (!modal || !iframeEl) return;

  if (titleEl) titleEl.innerText = title;
  iframeEl.src = videoUrl;
  modal.style.display = 'flex';
}

function closeVideoPreviewModal() {
  const modal = document.getElementById('video-preview-modal');
  const iframeEl = document.getElementById('video-modal-iframe');
  if (iframeEl) iframeEl.src = '';
  if (modal) modal.style.display = 'none';
}

// Legacy Contact Form Handler
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerText = 'Submitting...';
    }

    const payload = {
      full_name: document.getElementById('inq_name')?.value || 'Guest Student',
      email: document.getElementById('inq_email')?.value || 'student@domain.com',
      phone: document.getElementById('inq_phone')?.value || '+91 9919980246',
      course_interested: document.getElementById('inq_course')?.value || 'Course Inquiry',
      current_class: document.getElementById('inq_class')?.value || 'Class 11',
      message: document.getElementById('inq_message')?.value || 'Inquiry from web portal',
    };

    try {
      await api.post('/inquiries/', payload);
      showToast('Thank you! Our senior academic counselor will call you within 24 hours.', 'success', 6000);
      form.reset();
    } catch (err) {
      showToast(err.message || 'Submission failed. Please check fields.', 'error');
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = 'Request Free Counseling & Demo';
      }
    }
  });
}
