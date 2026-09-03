/**
 * ==========================================================================
 * MAYANK CLASSES - HIGH-FIDELITY ANIMATION & INTERACTION ENGINE
 * 90% Animation: 3D Orbit Parallax, Ambient Cursor Spotlight, Card Glows,
 * Automated Number Counters & Magnetic Micro-interactions.
 * ==========================================================================
 */

(function () {
  'use strict';

  function initAll() {
    try { initSmartNavbar(); } catch (e) { console.error('Navbar error:', e); }
    try { initCursorGlow(); } catch (e) {}
    try { initOrbitParallax(); } catch (e) {}
    try { initSpotlightGlow(); } catch (e) {}
    try { initScrollCounters(); } catch (e) {}
    try { initScrollReveals(); } catch (e) {}
    try { initMagneticButtons(); } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  /* 1. Dynamic Ambient Grid Cursor Light */
  function initCursorGlow() {
    const glow = document.getElementById('mc-cursor-glow');
    if (!glow) return;

    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let currentX = targetX;
    let currentY = targetY;

    window.addEventListener('mousemove', (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
    }, { passive: true });

    function render() {
      currentX += (targetX - currentX) * 0.08;
      currentY += (targetY - currentY) * 0.08;
      glow.style.left = `${currentX}px`;
      glow.style.top = `${currentY}px`;
      requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
  }

  /* 2. Hero Planetary Orbit Parallax & 3D Tilt (True 3D Billboarding - 100% Level & Straight View) */
  function initOrbitParallax() {
    const orbitWrapper = document.getElementById('mc-orbit-wrapper');
    const orbitPlane = document.getElementById('mc-orbit-plane');
    if (!orbitWrapper || !orbitPlane) return;

    // Natural 3D isometric resting angles
    const baseRotX = 40;
    const baseRotY = -8;
    const baseRotZ = 6;

    let targetRotX = baseRotX;
    let targetRotY = baseRotY;
    let currentRotX = baseRotX;
    let currentRotY = baseRotY;

    orbitWrapper.addEventListener('mousemove', (e) => {
      const rect = orbitWrapper.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      targetRotX = baseRotX - y * 16;
      targetRotY = baseRotY + x * 18;
    });

    orbitWrapper.addEventListener('mouseleave', () => {
      targetRotX = baseRotX;
      targetRotY = baseRotY;
    });

    // 9 Satellites with balanced spacing & comfortable, graceful orbital speed
    const satDefs = [
      // Ring 1 (radius 130px) - Gentle, calm speed
      { sel: '.mc-sat-neet', radius: 130, speed: 0.0042, angle: 0.8, baseZ: 26 },
      { sel: '.mc-sat-jee', radius: 130, speed: 0.0042, angle: 0.8 + Math.PI, baseZ: 26 },
      // Ring 2 (radius 195px) - Reverse orbit
      { sel: '.mc-sat-foundation', radius: 195, speed: -0.0030, angle: 0.4, baseZ: 34 },
      { sel: '.mc-sat-material', radius: 195, speed: -0.0030, angle: 0.4 + (2 * Math.PI / 3), baseZ: 34 },
      { sel: '.mc-sat-mcsat', radius: 195, speed: -0.0030, angle: 0.4 + (4 * Math.PI / 3), baseZ: 34 },
      // Ring 3 (radius 265px) - Outer wide orbit
      { sel: '.mc-sat-olympiad', radius: 265, speed: 0.0022, angle: 0.2, baseZ: 42 },
      { sel: '.mc-sat-tests', radius: 265, speed: 0.0022, angle: 0.2 + Math.PI / 2, baseZ: 42 },
      { sel: '.mc-sat-faculty', radius: 265, speed: 0.0022, angle: 0.2 + Math.PI, baseZ: 42 },
      { sel: '.mc-sat-notices', radius: 265, speed: 0.0022, angle: 0.2 + (3 * Math.PI / 2), baseZ: 42 },
    ];

    const satellites = satDefs.map(d => {
      const el = orbitPlane.querySelector(d.sel);
      return el ? { ...d, el } : null;
    }).filter(Boolean);

    let isPaused = false;
    orbitWrapper.addEventListener('mouseenter', () => { isPaused = true; });
    orbitWrapper.addEventListener('mouseleave', () => { isPaused = false; });

    let lastTime = performance.now();

    function updateFrame(now) {
      const deltaMs = now - lastTime;
      lastTime = now;
      // Normalize delta (clamped to prevent jumps on tab unfocus)
      const timeFactor = Math.min(Math.max(deltaMs / 16.667, 0.5), 2.5);

      // Smooth cursor parallax tilt
      currentRotX += (targetRotX - currentRotX) * 0.06;
      currentRotY += (targetRotY - currentRotY) * 0.06;
      orbitPlane.style.transform = `rotateX(${currentRotX.toFixed(2)}deg) rotateY(${currentRotY.toFixed(2)}deg) rotateZ(${baseRotZ}deg)`;

      // Animate satellites with high subpixel precision and smooth continuous depth
      const isMobile = window.innerWidth <= 768;
      const radiusScale = isMobile ? 0.52 : 1;

      satellites.forEach(sat => {
        if (!isPaused) {
          sat.angle += sat.speed * timeFactor;
        }

        const r = sat.radius * radiusScale;
        const sinA = Math.sin(sat.angle);
        const cosA = Math.cos(sat.angle);

        const x = cosA * r;
        const y = sinA * r;

        // Harmonic continuous depth wave: ZERO discrete jumps, 100% silky smooth
        const depthZ = sat.baseZ + (sinA * 22);

        // Smooth zIndex threshold with hysteresis to prevent edge flickering
        const zIndex = sinA > 0.05 ? 65 : (sinA < -0.05 ? 20 : 45);

        // Keep 100% straight, level, and facing the camera directly
        sat.el.style.transform = `translate(calc(-50% + ${x.toFixed(2)}px), calc(-50% + ${y.toFixed(2)}px)) translateZ(${depthZ.toFixed(1)}px) rotateZ(${-baseRotZ}deg) rotateY(${-currentRotY.toFixed(2)}deg) rotateX(${-currentRotX.toFixed(2)}deg)`;
        sat.el.style.zIndex = zIndex;
      });

      requestAnimationFrame(updateFrame);
    }
    requestAnimationFrame(updateFrame);

    // Interactive Satellite click jumps to target section
    document.querySelectorAll('.mc-orbit-sat').forEach(sat => {
      sat.addEventListener('click', (e) => {
        e.stopPropagation();
        const targetId = sat.getAttribute('data-target');
        if (targetId) {
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetEl.style.transform = 'translateY(-10px) scale(1.02)';
            targetEl.style.borderColor = 'var(--mc-coral)';
            setTimeout(() => {
              targetEl.style.transform = '';
              targetEl.style.borderColor = '';
            }, 1200);
          }
        }
      });
    });
  }

  /* 3. Card Mouse Spotlight Glow */
  function initSpotlightGlow() {
    const cards = document.querySelectorAll('.mc-spotlight-card, .mc-course-card, .mc-dash-card');
    cards.forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  }

  /* 4. Automated Count-up Stats Ticker */
  function initScrollCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-counter'), 10) || 0;
          const suffix = el.getAttribute('data-suffix') || '';
          animateNumber(el, target, suffix);
          obs.unobserve(el);
        }
      });
    }, { threshold: 0.3 });

    counters.forEach(el => observer.observe(el));
  }

  function animateNumber(element, target, suffix) {
    const duration = 1600;
    const startTime = performance.now();

    function step(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(target * ease);
      element.textContent = current + suffix;

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.textContent = target + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  /* 5. Universal Cinematic Scroll Reveal Engine */
  function initScrollReveals() {
    // Automatically select section headers, cards, grids, and banners across all pages
    const autoSelectors = [
      '.mc-section-header',
      '.mc-page-hero-card',
      '.mc-finder-card',
      '.mc-filter-card',
      '.mc-course-card',
      '.mc-catalog-card',
      '.mc-spotlight-card:not(.mc-marquee-card)',
      '.mc-photo-card:not(.mc-photo-marquee-card)',
      '.mc-dash-card',
      '.mc-card',
      '.mc-faculty-card',
      '.mc-topper-card',
      '.mc-hub-category-card',
      '.mc-about-card',
      '.mc-timeline-step',
      '.mc-curved-banner',
      '.mc-contact-card',
      '.mc-contact-form-wrap',
      '.mc-result-stat-card',
      '.mc-study-material-card',
      '.mc-recorded-card',
      '.mc-auth-card',
      '.mc-stat-item',
      '.mc-faq-item',
      '.mc-reveal',
      '.mc-reveal-up',
      '.mc-reveal-left',
      '.mc-reveal-right',
      '.mc-reveal-zoom'
    ];

    const allTargets = new Set();
    autoSelectors.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => {
        // Exclude elements inside continuous marquee tracks
        if (!el.closest('.mc-marquee-track') && !el.closest('.mc-photo-marquee-track')) {
          allTargets.add(el);
        }
      });
    });

    const vh = window.innerHeight || document.documentElement.clientHeight;

    // Apply reveal classes and compute cascading stagger delays for siblings
    allTargets.forEach(el => {
      if (!el.classList.contains('mc-reveal-left') && 
          !el.classList.contains('mc-reveal-right') && 
          !el.classList.contains('mc-reveal-zoom') &&
          !el.classList.contains('mc-reveal-up')) {
        el.classList.add('mc-reveal');
      }

      // Automatically apply stagger delays to child cards in grids
      const parentGrid = el.parentElement;
      if (parentGrid && (parentGrid.classList.contains('mc-courses-grid') ||
                         parentGrid.classList.contains('mc-catalog-grid') ||
                         parentGrid.classList.contains('mc-features-grid') ||
                         parentGrid.classList.contains('mc-faculty-grid') ||
                         parentGrid.classList.contains('mc-toppers-grid') ||
                         parentGrid.classList.contains('mc-hub-grid') ||
                         parentGrid.classList.contains('mc-hero-stats') ||
                         parentGrid.classList.contains('mc-photos-grid'))) {
        const siblings = Array.from(parentGrid.children);
        const index = siblings.indexOf(el);
        const delay = Math.min((index % 4) * 0.1, 0.4);
        el.style.transitionDelay = `${delay}s`;
      }

      // Only reveal elements immediately if they are in the initial viewport above the fold
      const rect = el.getBoundingClientRect();
      if (rect.top < vh - 20 && rect.bottom > 0) {
        el.classList.add('is-revealed');
        el.classList.add('active');
      }
    });

    // Dual-trigger system: IntersectionObserver + Real-time scroll listener
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          entry.target.classList.add('active');
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: '0px 0px -30px 0px',
      threshold: 0.02
    });

    allTargets.forEach(el => {
      if (!el.classList.contains('is-revealed')) {
        observer.observe(el);
      }
    });

    // Real-time scroll event listener for instantaneous fluid entrance reveals on scroll
    let ticking = false;
    const onScrollCheck = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const currentVh = window.innerHeight || document.documentElement.clientHeight;
          allTargets.forEach(el => {
            if (!el.classList.contains('is-revealed')) {
              const r = el.getBoundingClientRect();
              if (r.top < currentVh - 20 && r.bottom > 0) {
                el.classList.add('is-revealed');
                el.classList.add('active');
                try { observer.unobserve(el); } catch (e) {}
              }
            }
          });
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScrollCheck, { passive: true });
  }

  /* 6. Magnetic Buttons */
  function initMagneticButtons() {
    const buttons = document.querySelectorAll('.mc-btn-primary, .mc-btn-suggest, .btn-enroll');
    buttons.forEach(btn => {
      btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.16}px, ${y * 0.16}px)`;
      });

      btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
      });
    });
  }

  /* 7. Smart Auto-Hide / Auto-Reveal Navbar on Scroll */
  function initSmartNavbar() {
    const wrapper = document.getElementById('site-nav-wrapper');
    if (!wrapper) return;

    let lastScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;
    let isHidden = false;
    let ticking = false;

    function onScrollUpdate() {
      const currentScrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

      // Never hide navbar if mobile drawer is currently open
      const drawer = document.getElementById('mobile-nav-drawer');
      if (drawer && drawer.classList.contains('active')) {
        wrapper.classList.remove('nav-hidden');
        ticking = false;
        return;
      }

      // 1. At the very top (within 20px) -> show full header naturally
      if (currentScrollY <= 20) {
        wrapper.classList.remove('nav-hidden');
        wrapper.classList.remove('nav-compact');
        wrapper.classList.add('nav-at-top');
        isHidden = false;
        lastScrollY = currentScrollY;
        ticking = false;
        return;
      }

      const diff = currentScrollY - lastScrollY;

      // Filter out micro trackpad vibrations
      if (Math.abs(diff) < 5) {
        ticking = false;
        return;
      }

      if (diff > 0 && currentScrollY > 60) {
        // Scrolling DOWN -> Smoothly glide out of view
        if (!isHidden) {
          wrapper.classList.remove('nav-at-top');
          wrapper.classList.remove('nav-compact');
          wrapper.classList.add('nav-hidden');
          isHidden = true;
        }
      } else if (diff < 0) {
        // Scrolling UP -> Smoothly glide back into view with frosted glass navbar
        if (isHidden || !wrapper.classList.contains('nav-compact')) {
          wrapper.classList.remove('nav-hidden');
          wrapper.classList.remove('nav-at-top');
          wrapper.classList.add('nav-compact');
          isHidden = false;
        }
      }

      lastScrollY = currentScrollY;
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(onScrollUpdate);
        ticking = true;
      }
    }, { passive: true });

    // Establish initial position immediately
    onScrollUpdate();
  }

  /* 8. Marquee Carousel Motion Controls */
  window.setMarqueeDirection = function (dir) {
    const track = document.getElementById('mc-marquee-track');
    const btnLeft = document.getElementById('btn-marquee-left');
    const btnRight = document.getElementById('btn-marquee-right');
    if (!track) return;

    if (dir === 'right') {
      track.classList.add('track-reverse');
      if (btnRight) btnRight.classList.add('active');
      if (btnLeft) btnLeft.classList.remove('active');
    } else {
      track.classList.remove('track-reverse');
      if (btnLeft) btnLeft.classList.add('active');
      if (btnRight) btnRight.classList.remove('active');
    }
  };

  window.toggleMarqueePause = function (btn) {
    const track = document.getElementById('mc-marquee-track');
    if (!track) return;

    const computedStyle = window.getComputedStyle(track);
    const isPaused = computedStyle.animationPlayState === 'paused' || track.style.animationPlayState === 'paused';

    if (isPaused) {
      track.style.animationPlayState = 'running';
      if (btn) btn.innerHTML = '⏸️ Pause';
    } else {
      track.style.animationPlayState = 'paused';
      if (btn) btn.innerHTML = '▶️ Resume';
    }
  };

  /* 9. Photo Gallery Marquee Motion Controls */
  window.setPhotoMarqueeDirection = function (dir) {
    const track = document.getElementById('mc-photo-marquee-track');
    const btnLeft = document.getElementById('btn-photo-marquee-left');
    const btnRight = document.getElementById('btn-photo-marquee-right');
    if (!track) return;

    if (dir === 'right') {
      track.classList.add('track-reverse');
      if (btnRight) btnRight.classList.add('active');
      if (btnLeft) btnLeft.classList.remove('active');
    } else {
      track.classList.remove('track-reverse');
      if (btnLeft) btnLeft.classList.add('active');
      if (btnRight) btnRight.classList.remove('active');
    }
  };

  window.togglePhotoMarqueePause = function (btn) {
    const track = document.getElementById('mc-photo-marquee-track');
    if (!track) return;

    const computedStyle = window.getComputedStyle(track);
    const isPaused = computedStyle.animationPlayState === 'paused' || track.style.animationPlayState === 'paused';

    if (isPaused) {
      track.style.animationPlayState = 'running';
      if (btn) btn.innerHTML = '⏸️ Pause';
    } else {
      track.style.animationPlayState = 'paused';
      if (btn) btn.innerHTML = '▶️ Resume';
    }
  };

})();

