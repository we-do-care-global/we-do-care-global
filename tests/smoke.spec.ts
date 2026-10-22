import { expect, test } from '@playwright/test';

const pages = [
  '/',
  '/agentguard.html',
  '/agentvault.html',
  '/agent-eval.html',
  '/omniguard.html',
  '/enterprise-hybrid-rag.html',
  '/foundationcentar.html',
];

for (const path of pages) {
  test(`page ${path} renders with a heading and no uncaught errors`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    const response = await page.goto(path, { waitUntil: 'load' });
    expect(response?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveCount(1);
    expect(errors).toEqual([]);
  });
}

test('homepage project cards link to working pages', async ({ page, request }) => {
  await page.goto('/');
  const links = page.locator('article.card a[href]');
  await expect(links).toHaveCount(6);
  for (const link of await links.all()) {
    const href = await link.getAttribute('href');
    expect(href).toBeTruthy();
    const url = new URL(href!, page.url());
    expect(url.origin).toBe(new URL(page.url()).origin);
    const response = await request.get(url.toString());
    expect(response.status(), url.toString()).toBe(200);
  }
});

test('brand video is not preloaded and starts after page load', async ({ page }) => {
  await page.addInitScript(() => {
    (window as any).__brandVideoPlayCalls = 0;
    HTMLMediaElement.prototype.play = function () {
      (window as any).__brandVideoPlayCalls++;
      return Promise.resolve();
    };
    (window as any).requestIdleCallback = (callback: IdleRequestCallback) => {
      window.setTimeout(() => callback({ didTimeout: false, timeRemaining: () => 50 }), 50);
      return 1;
    };
  });
  await page.goto('/', { waitUntil: 'load' });
  const video = page.locator('#brand-video');
  await expect(video).toHaveAttribute('preload', 'none');
  await expect(video).toHaveAttribute('poster', /brand-poster\.jpg/);
  await expect.poll(() => page.evaluate(() => (window as any).__brandVideoPlayCalls)).toBeGreaterThan(0);
});

test('reduced motion suppresses automatic brand-video playback', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.addInitScript(() => {
    (window as any).__brandVideoPlayCalls = 0;
    HTMLMediaElement.prototype.play = function () {
      (window as any).__brandVideoPlayCalls++;
      return Promise.resolve();
    };
  });
  await page.goto('/', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  expect(await page.evaluate(() => (window as any).__brandVideoPlayCalls)).toBe(0);
});

test('Save-Data suppresses automatic brand-video playback', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'connection', {
      configurable: true,
      value: { saveData: true },
    });
    (window as any).__brandVideoPlayCalls = 0;
    HTMLMediaElement.prototype.play = function () {
      (window as any).__brandVideoPlayCalls++;
      return Promise.resolve();
    };
  });
  await page.goto('/', { waitUntil: 'load' });
  await page.waitForTimeout(500);
  expect(await page.evaluate(() => (window as any).__brandVideoPlayCalls)).toBe(0);
});
