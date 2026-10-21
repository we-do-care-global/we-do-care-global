'use strict';
// Shared chrome: mobile navigation, reveal-on-scroll, current-year stamp.
document.body.classList.add('enhanced');

const menuBtn = document.querySelector('.menu-btn');
const nav = document.querySelector('#main-nav');
if (menuBtn && nav) {
  menuBtn.hidden = false;
  const close = () => {
    document.body.classList.remove('nav-open');
    menuBtn.setAttribute('aria-expanded', 'false');
  };
  menuBtn.addEventListener('click', () => {
    const open = document.body.classList.toggle('nav-open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
      close();
      menuBtn.focus();
    }
  });
  document.addEventListener('click', e => {
    if (!nav.contains(e.target) && !menuBtn.contains(e.target)) close();
  });
}

const reveal = document.querySelectorAll('.reveal');
if (reveal.length) {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduced.matches || !('IntersectionObserver' in window)) {
    reveal.forEach(el => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          obs.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveal.forEach(el => io.observe(el));
  }
}
