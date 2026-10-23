/**
 * Cryptbyte Solutions - Global Scripts
 * Handles: navbar scroll/toggle, scroll animations
 */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Navbar: scroll shadow ────────────────────────────────────────────────
  const navbar = document.getElementById('main-navbar');

  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 30);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load
  }

  // ─── Navbar: mobile toggle ────────────────────────────────────────────────
  const toggle = document.getElementById('navbar-toggle');
  const navLinks = document.getElementById('navbar-nav');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      const isOpen = navLinks.classList.toggle('open');
      toggle.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', isOpen);
    });

    // Close on link click
    navLinks.querySelectorAll('.navbar__link').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', false);
      });
    });
  }

  // ─── Active nav link (based on scroll position) ───────────────────────────
  const sections    = document.querySelectorAll('section[id]');
  const navLinkEls  = document.querySelectorAll('.navbar__link[data-section]');

  const activateLink = () => {
    let current = '';
    sections.forEach(section => {
      const top = section.offsetTop - 100;
      if (window.scrollY >= top) current = section.id;
    });
    navLinkEls.forEach(link => {
      link.classList.toggle('active', link.dataset.section === current);
    });
  };

  window.addEventListener('scroll', activateLink, { passive: true });

  // ─── Scroll animations (IntersectionObserver) ─────────────────────────────
  const animateEls = document.querySelectorAll('[data-animate]');

  if (animateEls.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const delay = entry.target.dataset.delay || 0;
            setTimeout(() => {
              entry.target.classList.add('is-visible');
            }, Number(delay));
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    animateEls.forEach(el => observer.observe(el));
  } else {
    // Fallback: show all immediately
    animateEls.forEach(el => el.classList.add('is-visible'));
  }

  // ─── Hero stat counter animation ──────────────────────────────────────────
  const counters = document.querySelectorAll('[data-counter]');

  if (counters.length) {
    const countObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el      = entry.target;
        const target  = parseFloat(el.dataset.counter);
        const suffix  = el.dataset.suffix || '';
        const isFloat = String(target).includes('.');
        let start     = 0;
        const step    = target / 60;
        const timer   = setInterval(() => {
          start += step;
          if (start >= target) {
            start = target;
            clearInterval(timer);
          }
          el.textContent = (isFloat ? start.toFixed(1) : Math.ceil(start)) + suffix;
        }, 16);
        countObserver.unobserve(el);
      });
    }, { threshold: 0.5 });

    counters.forEach(c => countObserver.observe(c));
  }

  // ─── Universal Seamless Back Navigation ────────────────────────────────────
  document.addEventListener('click', (e) => {
    const backBtn = e.target.closest('[data-back="true"], .btn-back, [id$="-back"], [id$="-back-btn"]');
    if (!backBtn) return;

    e.preventDefault();
    const fallback = backBtn.getAttribute('href') || '/';

    // 1. If opened in a new tab or popup from another page on the same origin
    if (window.opener && !window.opener.closed) {
      try {
        if (window.opener.location.origin === window.location.origin) {
          window.close();
          return;
        }
      } catch (err) {}
    }

    // 2. If there is a valid same-origin referrer
    if (document.referrer) {
      try {
        const refUrl = new URL(document.referrer);
        if (refUrl.origin === window.location.origin) {
          // If referrer is a different page, return to it (preserves queries, search & page)
          if (refUrl.pathname !== window.location.pathname) {
            window.location.href = document.referrer;
            return;
          }
          // If referrer is the exact same page (e.g. form re-rendered after validation error),
          // navigate to fallback destination to avoid error loops
          window.location.href = fallback;
          return;
        }
      } catch (err) {}
    }

    // 3. If browser history contains previous entries
    if (window.history.length > 1) {
      window.history.back();
      return;
    }

    // 4. Default fallback redirect
    window.location.href = fallback;
  });

  // ---------------------------------------------------------------------------
  // Project Category Filter Tabs
  // ---------------------------------------------------------------------------
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('[data-category]');

  if (filterBtns.length && projectCards.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cat = btn.dataset.filter;
        projectCards.forEach(card => {
          const match = cat === 'all' || card.dataset.category === cat;
          card.style.opacity = match ? '1' : '0.25';
          card.style.transform = match ? 'scale(1)' : 'scale(0.97)';
          card.style.pointerEvents = match ? 'auto' : 'none';
        });
      });
    });
  }

  // ---------------------------------------------------------------------------
  // Dashboard Login Password Visibility Toggle
  // ---------------------------------------------------------------------------
  const toggleBtn = document.getElementById('toggle-pw-btn');
  const pwInput = document.getElementById('id_password');
  const eyeIcon = document.getElementById('eye-icon');
  const eyeOffIcon = document.getElementById('eye-off-icon');

  if (toggleBtn && pwInput) {
    toggleBtn.addEventListener('click', () => {
      const isPassword = pwInput.type === 'password';
      pwInput.type = isPassword ? 'text' : 'password';
      if (eyeIcon && eyeOffIcon) {
        eyeIcon.classList.toggle('d-none', isPassword);
        eyeOffIcon.classList.toggle('d-none', !isPassword);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Article Share / Copy Link
  // ---------------------------------------------------------------------------
  document.addEventListener('click', (e) => {
    const copyBtn = e.target.closest('[data-copy-link="true"], .article-share-btn[title="Copy Link"]');
    if (!copyBtn) return;

    e.preventDefault();
    if (navigator.clipboard && window.location.href) {
      navigator.clipboard.writeText(window.location.href)
        .then(() => {
          alert('Article link copied to clipboard!');
        })
        .catch(() => {
          prompt('Copy article link:', window.location.href);
        });
    } else {
      prompt('Copy article link:', window.location.href);
    }
  });

  // ---------------------------------------------------------------------------
  // Blog Newsletter Subscription Form
  // ---------------------------------------------------------------------------
  document.addEventListener('submit', (e) => {
    const newsletterForm = e.target.closest('.blog-newsletter__form, [data-newsletter-form]');
    if (!newsletterForm) return;

    e.preventDefault();
    const emailInput = newsletterForm.querySelector('input[type="email"]');
    if (emailInput && emailInput.value.trim()) {
      alert('Thank you for subscribing to Cryptbyte Insights!');
      newsletterForm.reset();
    }
  });

  // ---------------------------------------------------------------------------
  // Dashboard Filter Select Auto-Submit
  // ---------------------------------------------------------------------------
  document.addEventListener('change', (e) => {
    const selectEl = e.target.closest('select[data-auto-submit="true"], select.dash-select');
    if (!selectEl) return;

    if (selectEl.form) {
      selectEl.form.submit();
    }
  });

});
