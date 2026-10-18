/* ==========================================================================
   ALPHANET GROUP — Envoi des demandes de devis (Cloudflare Pages Functions)
   --------------------------------------------------------------------------
   Reçoit le formulaire du site, vérifie chaque champ, puis envoie un e-mail
   (version mise en page + version texte) à la boîte contact@ via le serveur
   d'envoi d'OVHcloud. Rien n'est enregistré : la demande n'existe que dans
   l'e-mail reçu.

   Réglages (Cloudflare > Workers & Pages > alphanet-site > Settings >
   Variables and Secrets) :
     SMTP_PASS  (secret, obligatoire) mot de passe de contact@alphanet-group.fr
     SMTP_USER  (facultatif) par défaut contact@alphanet-group.fr
     SMTP_HOST  (facultatif) par défaut ssl0.ovh.net
     SMTP_PORT  (facultatif) par défaut 465 (connexion chiffrée)
   Sans SMTP_PASS, la fonction répond 503 et le site propose l'envoi par la
   messagerie du visiteur.
   ========================================================================== */
import { connect } from 'cloudflare:sockets';

const MAILBOX = 'contact@alphanet-group.fr';
const ALLOWED_ORIGINS = new Set([
  'https://alphanet-group.fr',
  'https://www.alphanet-group.fr',
  'https://alphanet-site.pages.dev',
]);
const PRESTATIONS = new Set([
  'Bureaux / locaux professionnels',
  'Hôtellerie',
  'Copropriété / parties communes',
  'Commerce / lieu recevant du public',
  'Vitrerie',
  'Remise en état / après sinistre',
  'Particulier (domicile)',
  'Autre demande',
]);
const MAX_BODY = 8 * 1024;
const MIN_FILL_MS = 3000;
const SMTP_TIMEOUT_MS = 15000;

const json = (status, payload) => new Response(JSON.stringify(payload), {
  status,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
});

// Les aperçus Cloudflare (https://xxxx.alphanet-site.pages.dev) sont aussi acceptés.
const originAllowed = (origin) => ALLOWED_ORIGINS.has(origin)
  || /^https:\/\/[a-z0-9-]+\.alphanet-site\.pages\.dev$/.test(origin);

/* Vérification des champs ------------------------------------------------- */
const clean = (value, max, multiline = false) => String(value ?? '')
  .replace(multiline ? /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g, ' ')
  .replace(/\r\n?/g, '\n')
  .trim()
  .slice(0, max);

const EMAIL_RE = /^[^\s@<>"(),;:\\[\]]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*\.[A-Za-z]{2,24}$/;
const PHONE_RE = /^[0-9 +.\-]{10,20}$/;

function validate(input) {
  const data = {
    nom: clean(input.nom, 80),
    societe: clean(input.societe, 100),
    telephone: clean(input.telephone, 20),
    email: clean(input.email, 120),
    type: clean(input.type, 60),
    message: clean(input.message, 1500, true),
  };
  const errors = [];
  if (!data.nom) errors.push('nom');
  if (!PHONE_RE.test(data.telephone)) errors.push('telephone');
  if (!EMAIL_RE.test(data.email)) errors.push('email');
  if (!PRESTATIONS.has(data.type)) errors.push('type');
  return { data, errors };
}

/* Construction de l'e-mail -------------------------------------------------- */
const escapeHtml = (text) => text.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const utf8Base64 = (text) => {
  const bytes = new TextEncoder().encode(text);
  let binary = '';
  for (let i = 0; i < bytes.length; i += 0x8000) binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(binary);
};
const wrap76 = (b64) => b64.replace(/.{1,76}/g, '$&\r\n').trimEnd();
const encodeWord = (text) => (/^[\x20-\x7E]*$/.test(text) ? text : `=?UTF-8?B?${utf8Base64(text)}?=`);

const parisDate = (date) => new Intl.DateTimeFormat('fr-FR', {
  timeZone: 'Europe/Paris', dateStyle: 'full', timeStyle: 'short',
}).format(date);

function textVersion(d, when) {
  const lines = [
    'NOUVELLE DEMANDE DE DEVIS',
    'Reçue depuis le site alphanet-group.fr',
    '',
    `Prestation : ${d.type}`,
    '',
    'CONTACT',
    `Nom : ${d.nom}`,
    d.societe ? `Société / organisme : ${d.societe}` : null,
    `Téléphone : ${d.telephone}`,
    `E-mail : ${d.email}`,
    '',
    'BESOIN',
    d.message || '(aucun détail indiqué)',
    '',
    '—',
    `Envoyé le ${when}. Pour répondre au client, utilisez simplement « Répondre ».`,
  ];
  return lines.filter((line) => line !== null).join('\r\n');
}

function htmlVersion(d, when) {
  const e = Object.fromEntries(Object.entries(d).map(([k, v]) => [k, escapeHtml(v)]));
  const tel = d.telephone.replace(/[^0-9+]/g, '');
  const message = d.message ? e.message.replace(/\n/g, '<br>') : '<span style="color:#7a8aa3">Aucun détail indiqué.</span>';
  const row = (label, value) => `
          <tr>
            <td style="padding:10px 0;border-bottom:1px solid #e6edf6;color:#5b6b84;font-size:13px;width:150px;vertical-align:top">${label}</td>
            <td style="padding:10px 0;border-bottom:1px solid #e6edf6;color:#0c1a30;font-size:15px;font-weight:600">${value}</td>
          </tr>`;
  const replySubject = encodeURIComponent('Votre demande de devis — Alphanet Group');
  return `<!doctype html>
<html lang="fr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Demande de devis</title></head>
<body style="margin:0;padding:0;background:#eef4fb;font-family:Arial,Helvetica,sans-serif">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eef4fb;padding:24px 12px">
    <tr><td align="center">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #dbe5f1">
        <tr><td style="background:#1f5ad6;padding:22px 28px">
          <div style="color:#cfe0ff;font-size:12px;letter-spacing:2px;text-transform:uppercase;font-weight:700">Alphanet Group</div>
          <div style="color:#ffffff;font-size:22px;font-weight:700;margin-top:6px">Nouvelle demande de devis</div>
          <div style="color:#dbe7ff;font-size:13px;margin-top:4px">Reçue depuis le site alphanet-group.fr</div>
        </td></tr>
        <tr><td style="padding:24px 28px 8px">
          <div style="display:inline-block;background:#e8f0ff;color:#1f5ad6;font-weight:700;font-size:14px;padding:8px 14px;border-radius:999px">${e.type}</div>
        </td></tr>
        <tr><td style="padding:8px 28px 0">
          <div style="color:#1f5ad6;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin:12px 0 4px">Contact</div>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${row('Nom', e.nom)}${d.societe ? row('Société / organisme', e.societe) : ''}${row('Téléphone', `<a href="tel:${tel}" style="color:#1f5ad6;text-decoration:none">${e.telephone}</a>`)}${row('E-mail', `<a href="mailto:${e.email}" style="color:#1f5ad6;text-decoration:none">${e.email}</a>`)}
          </table>
        </td></tr>
        <tr><td style="padding:20px 28px 0">
          <div style="color:#1f5ad6;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;margin-bottom:8px">Besoin</div>
          <div style="background:#f5f8fc;border-left:4px solid #1f5ad6;border-radius:8px;padding:14px 16px;color:#0c1a30;font-size:15px;line-height:1.55">${message}</div>
        </td></tr>
        <tr><td style="padding:24px 28px">
          <table role="presentation" cellpadding="0" cellspacing="0"><tr>
            <td style="background:#1f5ad6;border-radius:8px"><a href="mailto:${e.email}?subject=${replySubject}" style="display:inline-block;padding:12px 20px;color:#ffffff;font-weight:700;font-size:14px;text-decoration:none">Répondre au client</a></td>
            <td style="width:10px"></td>
            <td style="border:1px solid #1f5ad6;border-radius:8px"><a href="tel:${tel}" style="display:inline-block;padding:11px 20px;color:#1f5ad6;font-weight:700;font-size:14px;text-decoration:none">Appeler</a></td>
          </tr></table>
        </td></tr>
        <tr><td style="background:#f5f8fc;padding:14px 28px;color:#7a8aa3;font-size:12px;border-top:1px solid #e6edf6">
          Envoyé le ${escapeHtml(when)} depuis le formulaire de devis. Le bouton « Répondre » de votre messagerie écrit directement au client.
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;
}

function buildMessage(d, now) {
  const when = parisDate(now);
  const boundary = `alt-${crypto.randomUUID()}`;
  const subject = ['Demande de devis', d.type, d.societe || d.nom].join(' — ');
  const headers = [
    `From: ${encodeWord('Site Alphanet Group')} <${MAILBOX}>`,
    `To: <${MAILBOX}>`,
    // Nom toujours encodé : une virgule ou un guillemet ne peut pas casser l'en-tête.
    `Reply-To: =?UTF-8?B?${utf8Base64(d.nom)}?= <${d.email}>`,
    `Subject: ${encodeWord(subject)}`,
    `Date: ${now.toUTCString().replace('GMT', '+0000')}`,
    `Message-ID: <${crypto.randomUUID()}@alphanet-group.fr>`,
    'MIME-Version: 1.0',
    `Content-Type: multipart/alternative; boundary="${boundary}"`,
  ];
  const part = (type, content) => [
    `--${boundary}`,
    `Content-Type: ${type}; charset=utf-8`,
    'Content-Transfer-Encoding: base64',
    '',
    wrap76(utf8Base64(content)),
  ].join('\r\n');
  return [
    headers.join('\r\n'),
    '',
    part('text/plain', textVersion(d, when)),
    part('text/html', htmlVersion(d, when)),
    `--${boundary}--`,
    '',
  ].join('\r\n');
}

/* Envoi SMTP (connexion chiffrée vers OVHcloud) ----------------------------- */
async function smtpSend({ host, port, secure, user, pass, from, to, message }) {
  const socket = connect({ hostname: host, port }, { secureTransport: secure ? 'on' : 'off' });
  const writer = socket.writable.getWriter();
  const reader = socket.readable.getReader();
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();
  let buffer = '';

  // Lit une réponse complète du serveur (les réponses sur plusieurs lignes finissent par « 250 texte »).
  const readReply = async () => {
    for (;;) {
      const lines = buffer.split('\r\n');
      for (let i = 0; i < lines.length - 1; i += 1) {
        if (/^\d{3}(?: |$)/.test(lines[i])) {
          buffer = lines.slice(i + 1).join('\r\n');
          return Number(lines[i].slice(0, 3));
        }
      }
      const { value, done } = await reader.read();
      if (done) throw new Error('connexion fermée par le serveur');
      buffer += decoder.decode(value, { stream: true });
    }
  };
  const send = (line) => writer.write(encoder.encode(`${line}\r\n`));
  const expect = async (codes, step) => {
    const code = await readReply();
    if (!codes.includes(code)) throw new Error(`${step} refusé (${code})`);
  };

  try {
    await expect([220], 'accueil');
    await send('EHLO alphanet-group.fr');
    await expect([250], 'EHLO');
    await send(`AUTH PLAIN ${utf8Base64(`\u0000${user}\u0000${pass}`)}`);
    await expect([235], 'authentification');
    await send(`MAIL FROM:<${from}>`);
    await expect([250], 'expéditeur');
    await send(`RCPT TO:<${to}>`);
    await expect([250, 251], 'destinataire');
    await send('DATA');
    await expect([354], 'DATA');
    // Une ligne qui commence par un point doit être doublée (règle SMTP).
    await writer.write(encoder.encode(`${message.replace(/^\./gm, '..')}\r\n.\r\n`));
    await expect([250], 'envoi');
    await send('QUIT');
  } finally {
    try { await socket.close(); } catch { /* déjà fermée */ }
  }
}

const withTimeout = (promise, ms) => Promise.race([
  promise,
  new Promise((_, reject) => { setTimeout(() => reject(new Error('délai dépassé')), ms); }),
]);

/* Point d'entrée -------------------------------------------------------------- */
export async function onRequestPost({ request, env }) {
  if (!originAllowed(request.headers.get('Origin') || '')) return json(403, { ok: false, error: 'origin' });
  if (!(request.headers.get('Content-Type') || '').startsWith('application/json')) return json(415, { ok: false, error: 'type' });

  const raw = await request.text();
  if (raw.length > MAX_BODY) return json(413, { ok: false, error: 'size' });
  let input;
  try { input = JSON.parse(raw); } catch { return json(400, { ok: false, error: 'json' }); }
  if (!input || typeof input !== 'object') return json(400, { ok: false, error: 'json' });

  // Pièges à robots : champ invisible rempli, ou formulaire envoyé trop vite.
  // On répond « ok » sans rien envoyer, pour ne pas renseigner le robot.
  const elapsed = Number(input.t);
  if (clean(input.site_web, 200) || !Number.isFinite(elapsed) || elapsed < MIN_FILL_MS) return json(200, { ok: true });

  const { data, errors } = validate(input);
  if (errors.length) return json(422, { ok: false, error: 'fields', fields: errors });

  if (!env.SMTP_PASS) return json(503, { ok: false, error: 'config' });

  try {
    await withTimeout(smtpSend({
      host: env.SMTP_HOST || 'ssl0.ovh.net',
      port: Number(env.SMTP_PORT) || 465,
      secure: env.SMTP_SECURE !== 'off',
      user: env.SMTP_USER || MAILBOX,
      pass: env.SMTP_PASS,
      from: env.SMTP_USER || MAILBOX,
      to: MAILBOX,
      message: buildMessage(data, new Date()),
    }), SMTP_TIMEOUT_MS);
  } catch (error) {
    console.error('Envoi du devis impossible :', error.message);
    return json(502, { ok: false, error: 'send' });
  }
  return json(200, { ok: true });
}

export const onRequest = () => json(405, { ok: false, error: 'method' });
