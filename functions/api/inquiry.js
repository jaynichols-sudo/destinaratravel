/**
 * Backup intake for destinaratravel.com forms.
 *
 * The browser still posts each form to FormSubmit, which emails
 * info@destinaratravel.com. This function receives a copy at the same time.
 *
 * To keep that copy, set INQUIRY_WEBHOOK on the Cloudflare Pages project
 * (Settings, Environment variables) to a Zapier, Make, n8n, or Google Apps
 * Script URL that accepts JSON. No webhook means the copy is accepted and
 * then discarded; this file does not invent a store that needs credentials.
 */

const DROP_FIELDS = new Set(['_honey', '_captcha', '_template', '_next']);
const MAX_VALUE = 5000;

export async function onRequestPost(context) {
  const { request, env } = context;

  try {
    const payload = await parseBody(request);
    if (!payload) {
      return json({ ok: false, error: 'unsupported body' }, 400);
    }

    if (String(payload._honey || '').trim()) {
      return new Response(null, { status: 204 });
    }

    const record = { received_at: new Date().toISOString() };
    for (const [key, value] of Object.entries(payload)) {
      if (DROP_FIELDS.has(key) || value == null) continue;
      const str = String(value).trim();
      if (!str) continue;
      record[key] = str.slice(0, MAX_VALUE);
    }

    const webhook = env && typeof env.INQUIRY_WEBHOOK === 'string' ? env.INQUIRY_WEBHOOK.trim() : '';
    if (webhook) {
      if (!isAllowedWebhook(webhook)) {
        return json({ ok: false, error: 'backup webhook is not a valid https URL' }, 500);
      }
      const res = await fetch(webhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(record),
      });
      if (!res.ok) {
        return json({ ok: false, error: 'backup webhook failed' }, 502);
      }
    }

    return json({ ok: true, stored: Boolean(webhook) });
  } catch (err) {
    return json({ ok: false, error: 'server error' }, 500);
  }
}

async function parseBody(request) {
  const ctype = (request.headers.get('Content-Type') || '').toLowerCase();
  if (ctype.includes('application/json')) {
    const data = await request.json();
    if (!data || typeof data !== 'object' || Array.isArray(data)) return null;
    return data;
  }

  const form = await request.formData();
  const data = {};
  for (const [key, value] of form.entries()) {
    if (typeof value === 'string') data[key] = value;
  }
  return data;
}

function isAllowedWebhook(url) {
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'https:';
  } catch (err) {
    return false;
  }
}

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: { 'Content-Type': 'application/json' },
  });
}
