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
    const localOrigin = new URL(page.url()).origin;
    // The published site uses some absolute first-party URLs; resolve them
    // to our local fixture instead of contacting the live website.
    expect([localOrigin, 'https://wedocare-global.com']).toContain(url.origin);
    const localUrl = new URL(url.pathname + url.search, localOrigin);
    const response = await request.get(localUrl.toString());
    expect(response.status(), localUrl.toString()).toBe(200);
  }
});

test('brand video defers playback until after load and idle', async ({ page }) => {
  await page.addInitScript(() => {
    (window as any).__brandVideoPlayCalls = 0;
    (window as any).__idleCallbacks = [];
    Object.defineProperty(navigator, 'connection', { configurable: true, value: { saveData: false } });
    const originalMatchMedia = window.matchMedia.bind(window);
    window.matchMedia = (query: string) => {
      if (query === '(prefers-reduced-motion: reduce)') {
        return { ...originalMatchMedia(query), matches: false, addEventListener: () => {} } as MediaQueryList;
      }
      return originalMatchMedia(query);
    };
    HTMLMediaElement.prototype.play = function () {
      (window as any).__brandVideoPlayCalls++;
      return Promise.resolve();
    };
    (window as any).requestIdleCallback = (callback: IdleRequestCallback) => {
      (window as any).__idleCallbacks.push(callback);
      return (window as any).__idleCallbacks.length;
    };
  });
  await page.goto('/', { waitUntil: 'load' });
  const video = page.locator('#brand-video');
  await expect(video).toHaveAttribute('preload', 'none');
  await expect(video).toHaveAttribute('poster', /brand-poster\\.jpg/);
  expect(await page.evaluate(() => (window as any).__brandVideoPlayCalls)).toBe(0);
  await expect.poll(() => page.evaluate(() => (window as any).__idleCallbacks.length)).toBeGreaterThan(0);
  await page.evaluate(() => {
    for (const callback of (window as any).__idleCallbacks.splice(0)) {
      callback({ didTimeout: false, timeRemaining: () => 50 });
    }
  });
  await expect.poll(() => page.evaluate(() => (window as any).__brandVideoPlayCalls)).toBe(1);
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
