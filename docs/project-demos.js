'use strict';
const api = 'https://wdcg-agentguard-api.emirperla96.workers.dev';
async function referenceCheck(path, button) {
  const output = document.querySelector('#guard-result');
  const buttons = [...document.querySelectorAll('#guard-health, #guard-audit')];
  buttons.forEach(b => { b.disabled = true; });
  output.textContent = 'Checking the reference service…';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(api + path, {signal: controller.signal, credentials: 'omit', referrerPolicy: 'no-referrer'});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    const label = path === '/health' ? 'Reference health response (not a production certification)' : 'Reference audit response (inspect its reported verification result)';
    output.textContent = `${label}\n${JSON.stringify(data, null, 2)}`;
  } catch (error) {
    output.textContent = `UNAVAILABLE — ${error.name === 'AbortError' ? 'request timed out' : error.message}. No live result is verified. No simulated result has been substituted.`;
  } finally { clearTimeout(timer); buttons.forEach(b => { b.disabled = false; }); }
}
document.querySelector('#guard-health')?.addEventListener('click', e => referenceCheck('/health', e.currentTarget));
document.querySelector('#guard-audit')?.addEventListener('click', e => referenceCheck('/audit/verify', e.currentTarget));
document.querySelector('#approve-demo')?.addEventListener('click', () => {
  document.querySelector('#approval-state').textContent = 'Human approval — explicitly selected in this illustration';
  document.querySelector('#deployment-state').textContent = 'Deployment — not connected; no deployment performed';
  document.querySelector('#approval-result').textContent = 'Local illustration approved. No real approval token was issued and nothing was deployed.';
});
document.querySelector('#reset-approval')?.addEventListener('click', () => {
  document.querySelector('#approval-state').textContent = 'Human approval — pending';
  document.querySelector('#deployment-state').textContent = 'Deployment — blocked in this illustration';
  document.querySelector('#approval-result').textContent = 'Illustration reset. Nothing has been deployed.';
});
const documents = [
  'Agent policy defines which tools are allowed and when human approval is needed.',
  'Retrieval combines knowledge documents and query matching before generating an answer.',
  'Evaluation measures task success, tool errors and decision latency against declared thresholds.',
  'Vault access restricts tools and credentials to scoped roles.',
  'Regulatory case review requires qualified human verification of evidence.'
];
document.querySelector('#sample-search')?.addEventListener('click', () => {
  const terms = [...new Set(document.querySelector('#sample-query').value.toLowerCase().match(/[a-z0-9]+/g) || [])];
  const results = documents.map((text, index) => ({text, index, score: terms.filter(term => (text.toLowerCase().match(/[a-z0-9]+/g) || []).includes(term)).length})).filter(x => x.score > 0).sort((a,b) => b.score - a.score || a.index - b.index);
  const output = document.querySelector('#sample-results'); output.replaceChildren();
  for (const result of results) { const item = document.createElement('li'); item.textContent = `${result.text} — ${result.score} matching query word(s)`; output.append(item); }
  if (!results.length) { const item = document.createElement('li'); item.textContent = terms.length ? 'No matching sample documents.' : 'Enter at least one word.'; output.append(item); }
});
let eventNumber = 0;
document.querySelector('#vault-evaluate')?.addEventListener('click', () => {
  const role = document.querySelector('#vault-role').value;
  const tool = document.querySelector('#vault-tool').value;
  const allowed = tool === 'read' || role === 'operator';
  document.querySelector('#vault-result').textContent = `ILLUSTRATION ${++eventNumber}\nRole: ${role}\nAction: ${tool}\nSample policy: ${allowed ? 'ALLOW' : 'DENY'}\nNo tool was executed. This event number is not a cryptographic proof.`;
});
