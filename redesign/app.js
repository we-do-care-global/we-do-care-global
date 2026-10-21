'use strict';
// Progressive enhancement for the landing page: system filtering, starting-point
// chooser, inquiry preparation and the brand film transport control.

const filterGroup = document.querySelector('.filters');
if (filterGroup) {
  filterGroup.hidden = false;
  filterGroup.querySelectorAll('[data-filter]').forEach(button => {
    button.addEventListener('click', () => {
      filterGroup.querySelectorAll('button').forEach(other => {
        other.classList.toggle('active', other === button);
        other.setAttribute('aria-pressed', String(other === button));
      });
      let visible = 0;
      document.querySelectorAll('.card').forEach(card => {
        card.hidden = button.dataset.filter !== 'all' && card.dataset.group !== button.dataset.filter;
        if (!card.hidden) visible++;
      });
      const status = document.querySelector('#filter-status');
      if (status) status.textContent = `${visible} ${visible === 1 ? 'system' : 'systems'} shown.`;
    });
  });
}

const choices = document.querySelector('.choices');
const recommendations = [
  ['AgentGuard', 'agentguard', 'SECURITY', 'Start with the boundaries around what your agents can do. Review policies and audit behaviour before connecting privileged tools.'],
  null,
  ['Enterprise Hybrid-RAG', 'enterprise-hybrid-rag', 'RETRIEVAL', 'Start with your knowledge sources. Compare lexical and semantic retrieval against representative questions before choosing a configuration.'],
  ['Agent Eval', 'agent-eval', 'EVALUATION', 'Define acceptance criteria, assemble representative tasks and inspect failures before increasing autonomy.'],
  null,
  ['Pharma Intelligence OS', 'pharma-intelligence-os', 'REGULATORY INTELLIGENCE', 'Explore case review and regulatory evidence while keeping qualified human review central.']
];
if (choices) {
  choices.hidden = false;
  choices.querySelectorAll('[data-choice]').forEach(button => {
    button.addEventListener('click', () => {
      choices.querySelectorAll('button').forEach(other => {
        other.classList.toggle('selected', other === button);
        other.setAttribute('aria-pressed', String(other === button));
      });
      const entry = recommendations[Number(button.dataset.choice)];
      if (!entry) return;
      const [name, slug, category, description] = entry;
      const panel = document.querySelector('#recommendation');
      panel.replaceChildren();
      const label = document.createElement('div');
      label.className = 'label';
      label.textContent = `YOUR STARTING POINT / ${category}`;
      const heading = document.createElement('h3');
      heading.textContent = name;
      const paragraph = document.createElement('p');
      paragraph.textContent = description;
      const link = document.createElement('a');
      link.className = 'btn btn-sm';
      link.href = `${slug}.html`;
      link.textContent = `Explore ${name} ↗`;
      panel.append(label, heading, paragraph, link);
    });
  });
}

const form = document.querySelector('#contact-form');
if (form) {
  form.querySelectorAll('[data-enhanced]').forEach(button => { button.hidden = false; });
  form.addEventListener('submit', e => e.preventDefault());
  const status = document.querySelector('#form-status');
  function inquiry() {
    if (!form.reportValidity()) return null;
    const data = new FormData(form);
    const subject = `We Do Care Global inquiry: ${data.get('interest')}`;
    const body = `Name: ${String(data.get('name')).trim()}\nEmail: ${String(data.get('email')).trim()}\nInterest: ${data.get('interest')}\n\n${String(data.get('message')).trim()}`;
    const text = `To: emir@wedocare-global.com\nSubject: ${subject}\n\n${body}`;
    document.querySelector('#prepared-inquiry').value = text;
    document.querySelector('#inquiry-preview').hidden = false;
    return { subject, body, text };
  }
  document.querySelector('#prepare-inquiry').addEventListener('click', () => {
    const draft = inquiry();
    if (!draft) return;
    const url = `mailto:emir@wedocare-global.com?subject=${encodeURIComponent(draft.subject)}&body=${encodeURIComponent(draft.body)}`;
    if (url.length > 1800) {
      status.textContent = 'Your inquiry is ready below. For long messages, copy or download it and paste it into your email service. Nothing has been sent.';
      return;
    }
    status.textContent = 'Your email app should open with a draft. Nothing has been sent. If it does not open, copy or download the inquiry below.';
    window.location.href = url;
  });
  document.querySelector('#copy-inquiry').addEventListener('click', async () => {
    const draft = inquiry();
    if (!draft) return;
    try {
      await navigator.clipboard.writeText(draft.text);
      status.textContent = 'Inquiry copied. Paste it into your email service and send it when ready. Nothing has been sent.';
    } catch {
      const field = document.querySelector('#prepared-inquiry');
      field.focus();
      field.select();
      status.textContent = 'Automatic copying was unavailable. The inquiry text is selected; copy it manually. Nothing has been sent.';
    }
  });
  document.querySelector('#download-inquiry').addEventListener('click', () => {
    const draft = inquiry();
    if (!draft) return;
    const url = URL.createObjectURL(new Blob([draft.text], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'we-do-care-inquiry.txt';
    document.body.append(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = 'Inquiry download prepared on your device. Nothing has been sent.';
  });
}

const video = document.querySelector('#brand-video');
const motion = document.querySelector('#motion-toggle');
if (video && motion) {
  motion.hidden = false;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const update = () => {
    motion.textContent = video.paused ? 'Play motion ▷' : 'Pause motion Ⅱ';
    motion.setAttribute('aria-label', video.paused ? 'Play brand animation' : 'Pause brand animation');
  };
  const play = () => video.play().catch(update);
  video.addEventListener('play', update);
  video.addEventListener('pause', update);
  motion.addEventListener('click', () => { if (video.paused) play(); else video.pause(); });
  reduced.addEventListener('change', e => { if (e.matches) video.pause(); });
  const unavailable = () => {
    motion.textContent = 'Video unavailable';
    motion.disabled = true;
    motion.setAttribute('aria-label', 'Brand video unavailable');
  };
  video.addEventListener('error', unavailable);
  video.querySelector('source')?.addEventListener('error', unavailable);
  update();
  if (!reduced.matches && !navigator.connection?.saveData) play();
}
