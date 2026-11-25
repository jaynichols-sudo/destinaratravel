/* Sends a backup copy of each FormSubmit form to /api/inquiry before the
   browser posts to FormSubmit. Durable storage starts when the
   INQUIRY_WEBHOOK environment variable is set on the Cloudflare Pages project. */
(function () {
  function isDestinaraForm(form) {
    if (!form || !form.getAttribute) return false;
    var action = form.getAttribute('action') || '';
    return action.indexOf('formsubmit.co') !== -1;
  }

  function honeyFilled(form) {
    var honey = form.querySelector('[name="_honey"]');
    return !!(honey && String(honey.value || '').trim());
  }

  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!isDestinaraForm(form) || honeyFilled(form)) return;
    try {
      var data = new FormData(form);
      data.set('_backup_page', window.location.pathname || '');
      data.set('_backup_url', (window.location.origin || '') + (window.location.pathname || ''));
      data.set('_backup_time', new Date().toISOString());
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/inquiry', data);
      } else {
        fetch('/api/inquiry', {
          method: 'POST',
          body: data,
          keepalive: true,
          credentials: 'same-origin'
        }).catch(function () {});
      }
    } catch (err) {}
  }, true);
})();
