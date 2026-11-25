/* Prefills the consultation form from the query string, e.g. /consultation.html?interest=nyawa */
(function () {
  var params = new URLSearchParams(window.location.search);
  var interest = (params.get('interest') || params.get('destination') || '').toLowerCase().trim();
  if (!interest) return;
  var known = {
    nyawa: {
      destination: 'nyawa Private Retreat Villas, Bali',
      details: 'I am interested in staying at nyawa Private Retreat Villas in Bali.'
    }
  };
  var pick = known[interest];
  var label = pick ? pick.destination : interest.replace(/[^a-z0-9 ,&'-]/g, ' ').replace(/\s+/g, ' ').slice(0, 80);
  if (!label) return;
  var form = document.querySelector('form[action*="formsubmit.co"] [name="Destinations"]');
  form = form ? form.form : null;
  if (!form) return;
  var dest = form.elements['Destinations'];
  if (dest && !dest.value) dest.value = label;
  var details = form.elements['Details'];
  if (details && !details.value && pick) details.value = pick.details;
  var hidden = document.createElement('input');
  hidden.type = 'hidden';
  hidden.name = 'Interest';
  hidden.value = interest.replace(/[^a-z0-9 _-]/g, '').slice(0, 40);
  form.appendChild(hidden);
  var note = document.createElement('p');
  note.textContent = 'Asking about: ' + label + '. Add your dates and we will check availability.';
  note.style.cssText = 'background:#f0ebe4;border-radius:10px;padding:12px 16px;margin:0 0 18px;color:#0D5C5C;font-weight:600';
  form.insertBefore(note, form.firstChild);
})();
