/* HubSpot public form embed: no private API key or backend credentials. */
(function () {
  'use strict';
  var attempted = false;
  var timeoutId;
  function fallback(message) {
    var status = document.getElementById('assessment-form-status');
    if (status) {
      status.textContent = message;
      status.hidden = false;
    }
  }
  function mount() {
    if (attempted) return;
    var target = document.getElementById('hubspot-assessment-form');
    if (!target) return;
    if (!window.hbspt || !window.hbspt.forms || typeof window.hbspt.forms.create !== 'function') {
      fallback('The inquiry form is unavailable. Please use the email contact link below.');
      return;
    }
    attempted = true;
    clearTimeout(timeoutId);
    try {
      window.hbspt.forms.create({
        portalId: '149282104',
        formId: '646cc721-5cbf-45ad-95e8-174ade6b5221',
        target: '#hubspot-assessment-form',
        onFormReady: function () {
          clearTimeout(timeoutId);
          var status = document.getElementById('assessment-form-status');
          if (status) status.hidden = true;
        }
      });
      timeoutId = setTimeout(function () {
        if (!target.querySelector('form, iframe')) {
          fallback('The inquiry form could not be displayed. Please use the email contact link below.');
        }
      }, 10000);
    } catch (error) {
      fallback('The inquiry form could not be displayed. Please use the email contact link below.');
    }
  }
  function init() {
    var script = document.getElementById('hubspot-embed-script');
    if (!script) {
      fallback('The inquiry form is unavailable. Please use the email contact link below.');
      return;
    }
    if (window.hbspt && window.hbspt.forms) {
      mount();
    } else {
      script.addEventListener('load', mount, { once: true });
      script.addEventListener('error', function () {
        fallback('The inquiry form could not be loaded. Please use the email contact link below.');
      }, { once: true });
      setTimeout(function () {
        if (!attempted) fallback('The inquiry form is taking too long to load. Please use the email contact link below.');
      }, 10000);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
}());
