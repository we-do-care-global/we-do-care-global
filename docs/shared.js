'use strict';
document.body.classList.add('enhanced');
const menu = document.querySelector('.menu');
const nav = document.querySelector('#main-nav');
if (menu && nav) {
  menu.hidden = false;
  function closeMenu() { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
  menu.addEventListener('click', () => { const open = nav.classList.toggle('open'); menu.setAttribute('aria-expanded', String(open)); });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); } });
  document.addEventListener('click', e => { if (!nav.contains(e.target) && !menu.contains(e.target)) closeMenu(); });
  window.matchMedia('(min-width: 769px)').addEventListener('change', e => { if (e.matches) closeMenu(); });
}
