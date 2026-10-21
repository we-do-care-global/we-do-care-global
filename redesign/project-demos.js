'use strict';
// Bounded, deterministic demonstrations. Nothing here executes a real agent tool,
// calls a real model or returns a simulated result in place of a live one.

const api = 'https://wdcg-agentguard-api.emirperla96.workers.dev';

async function referenceCheck(path) {
  const output = document.querySelector('#guard-result');
  const buttons = [...document.querySelectorAll('#guard-health, #guard-audit')];
  buttons.forEach(b => { b.disabled = true; });
  output.textContent = 'Checking the reference service…';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(api + path, { signal: controller.signal, credentials: 'omit', referrerPolicy: 'no-referrer' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const label = path === '/health'
      ? 'Reference health response (not a production certification)'
      : 'Reference audit response (inspect its reported verification result)';
    output.textContent = `${label}\n${JSON.stringify(data, null, 2)}`;
    output.classList.add('is-hit');
  } catch (error) {
    output.textContent = `UNAVAILABLE — ${error.name === 'AbortError' ? 'request timed out' : error.message}. No live result is verified. No simulated result has been substituted.`;
    output.classList.remove('is-hit');
  } finally {
    clearTimeout(timer);
    buttons.forEach(b => { b.disabled = false; });
  }
}

document.querySelector('#guard-health')?.addEventListener('click', () => referenceCheck('/health'));
document.querySelector('#guard-audit')?.addEventListener('click', () => referenceCheck('/audit/verify'));

document.querySelector('#approve-demo')?.addEventListener('click', () => {
  const approval = document.querySelector('#approval-state');
  const deployment = document.querySelector('#deployment-state');
  const result = document.querySelector('#approval-result');
  if (approval) approval.textContent = 'Human approval — explicitly selected in this illustration';
  if (deployment) deployment.textContent = 'Deployment — not connected; no deployment performed';
  if (result) {
    result.textContent = 'Local illustration approved. No real approval token was issued and nothing was deployed.';
    result.classList.add('is-hit');
  }
});

document.querySelector('#reset-approval')?.addEventListener('click', () => {
  const approval = document.querySelector('#approval-state');
  const deployment = document.querySelector('#deployment-state');
  const result = document.querySelector('#approval-result');
  if (approval) approval.textContent = 'Human approval — pending';
  if (deployment) deployment.textContent = 'Deployment — blocked in this illustration';
  if (result) {
    result.textContent = 'Illustration reset. Nothing has been deployed.';
    result.classList.remove('is-hit');
  }
});

const documents = [
  'Agent policy defines which tools are allowed and when human approval is needed.',
  'Retrieval combines knowledge documents and query matching before generating an answer.',
  'Evaluation measures task success, tool errors and decision latency against declared thresholds.',
  'Vault access restricts tools and credentials to scoped roles.',
  'Regulatory case review requires qualified human verification of evidence.'
];

document.querySelector('#sample-search')?.addEventListener('click', () => {
  const field = document.querySelector('#sample-query');
  const terms = [...new Set((field.value || '').toLowerCase().match(/[a-z0-9]+/g) || [])];
  const results = documents
    .map((text, index) => ({
      text,
      index,
      score: terms.filter(term => (text.toLowerCase().match(/[a-z0-9]+/g) || []).includes(term)).length
    }))
    .filter(x => x.score > 0)
    .sort((a, b) => b.score - a.score || a.index - b.index);

  const output = document.querySelector('#sample-results');
  output.replaceChildren();
  for (const result of results) {
    const item = document.createElement('li');
    item.textContent = `${result.text} — ${result.score} matching query word${result.score === 1 ? '' : 's'}`;
    output.append(item);
  }
  if (!results.length) {
    const item = document.createElement('li');
    item.textContent = terms.length ? 'No matching sample documents.' : 'Enter at least one word.';
    output.append(item);
  }
});

let eventNumber = 0;
document.querySelector('#vault-evaluate')?.addEventListener('click', () => {
  const role = document.querySelector('#vault-role').value;
  const tool = document.querySelector('#vault-tool').value;
  const allowed = tool === 'read' || role === 'operator';
  const output = document.querySelector('#vault-result');
  output.textContent = `ILLUSTRATION ${++eventNumber}\nRole: ${role}\nAction: ${tool}\nSample policy: ${allowed ? 'ALLOW' : 'DENY'}\nNo tool was executed. This event number is not a cryptographic proof.`;
  output.classList.add('is-hit');
});
