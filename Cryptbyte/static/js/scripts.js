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

});
