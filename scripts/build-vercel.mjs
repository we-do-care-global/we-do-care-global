import { cpSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

// Build from the same site as GitHub Pages without modifying its source or DNS.
const output = resolve('.vercel-site');
rmSync(output, { recursive: true, force: true });
mkdirSync(output, { recursive: true });
cpSync('docs', output, { recursive: true });
writeFileSync(`${output}/analytics-init.js`,
  "window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };\n");

let pages = 0;
for (const file of readdirSync(output)) {
  if (!file.endsWith('.html') || file.startsWith('google')) continue;
  const path = `${output}/${file}`;
  const html = readFileSync(path, 'utf8');
  if (!html.includes('</head>')) throw new Error(`Missing head in ${file}`);
  if (/vercel\/insights|vercel-insights\.com|analytics-init\.js/.test(html)) {
    throw new Error(`Existing analytics in ${file}; review before injecting`);
  }
  writeFileSync(path, html.replace('</head>',
    '<script defer src="/analytics-init.js"></script>\n' +
    '<script defer src="/_vercel/insights/script.js"></script>\n</head>'));
  pages++;
}
console.log(`Prepared ${pages} HTML pages with one Web Analytics integration each.`);
