/* Accessible manual playback for browsers that block autoplay. */
(() => {
  'use strict';
  const video = document.getElementById('brand-video');
  const overlay = document.getElementById('film-play-overlay');
  if (!video || !overlay) return;

  const sync = () => {
    const playing = !video.paused && !video.ended;
    overlay.hidden = playing;
    if (!playing) {
      overlay.disabled = false;
      overlay.textContent = video.ended ? 'Replay video' : 'Play video';
      overlay.setAttribute('aria-label', video.ended ? 'Replay brand video' : 'Play brand video');
    }
  };

  const fail = () => {
    overlay.hidden = false;
    overlay.disabled = false;
    overlay.textContent = 'Retry video';
    overlay.setAttribute('aria-label', 'Retry playing brand video');
  };

  overlay.addEventListener('click', async () => {
    overlay.disabled = true;
    try {
      // Preserve the user's play gesture; calling load() here can reset playback.
      if (video.ended) video.currentTime = 0;
      await video.play();
    } catch (_) {
      fail();
    } finally {
      if (!overlay.hidden) overlay.disabled = false;
    }
  });
  video.addEventListener('playing', sync);
  video.addEventListener('pause', sync);
  video.addEventListener('ended', sync);
  video.addEventListener('error', fail);
  video.querySelector('source')?.addEventListener('error', fail);
  sync();
})();
