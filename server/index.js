const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json({ limit: '5mb' })); // allow base64 images

const dataDir = path.join(__dirname, 'data');
const reviewsPath = path.join(dataDir, 'reviews.json');
const profanityPath = path.join(dataDir, 'profanity.json');

function ensureDataFiles() {
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
  if (!fs.existsSync(reviewsPath)) fs.writeFileSync(reviewsPath, '[]', 'utf8');
  if (!fs.existsSync(profanityPath)) {
    fs.writeFileSync(
      profanityPath,
      JSON.stringify(
        [
          'хуй','хуе','хуя','пизд','бля','еба','ебл','ебу','сука','мраз','гандон',
          'дерьмо','говн','мудак','с*ка','шлюх','пидор','нахер','нахуй', 'плохой'
        ],
        null,
        2
      ),
      'utf8'
    );
  }
}
ensureDataFiles();

function loadJson(p) {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    return Array.isArray(p) ? [] : [];
  }
}
function saveJson(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2), 'utf8');
}

function normalizeText(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
}

function containsProfanity(text, list) {
  const t = normalizeText(text);
  return list.some((w) => t.includes(w));
}

async function notifyTelegramAdmin(message) {
  const token = process.env.TG_BOT_TOKEN;
  const chatId = process.env.TG_CHAT_ID; // numeric chat id or @username not supported by API
  if (!token || !chatId) return;
  const url = `https://api.telegram.org/bot${token}/sendMessage`;
  try {
    await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text: message }),
    });
  } catch (e) {
    console.warn('Telegram notify failed', e);
  }
}

// Reviews API
app.get('/api/reviews', (req, res) => {
  const reviews = loadJson(reviewsPath);
  res.json(reviews);
});

app.post('/api/reviews', async (req, res) => {
  const { name, text, rating, imageDataUrl } = req.body || {};
  if (!name || !text || !rating) {
    return res.status(400).json({ error: 'invalid_input' });
  }
  const badList = loadJson(profanityPath);
  if (containsProfanity(name, badList) || containsProfanity(text, badList)) {
    const createdAt = new Date().toISOString();
    const msg =
      `Нецензурный отзыв:\nИмя: ${name}\nОценка: ${rating}\nТекст: ${text}\nДата: ${new Date(createdAt).toLocaleString('ru-RU')}`;
    await notifyTelegramAdmin(msg);
    return res.status(422).json({ error: 'profanity', message: 'Будьте добрее!' });
  }
  const ratingNum = Number(rating);
  // Правило публикации: публикуем только 4 и 5 звёзд; 1–3 звезды — только в Telegram
  if (ratingNum < 4) {
    const createdAt = new Date().toISOString();
    const msg =
      `Отзыв (не опубликован):\nИмя: ${name}\nОценка: ${rating}\nТекст: ${text}\nДата: ${new Date(createdAt).toLocaleString('ru-RU')}`;
    await notifyTelegramAdmin(msg);
    return res.status(202).json({ status: 'redirected', message: 'Спасибо за отзыв!' });
  }
  const review = {
    id: Date.now().toString(),
    name,
    text,
    rating,
    imageDataUrl: imageDataUrl || '',
    createdAt: new Date().toISOString(),
  };
  const reviews = loadJson(reviewsPath);
  reviews.push(review);
  saveJson(reviewsPath, reviews);
  res.status(201).json(review);
});

app.delete('/api/reviews/:id', (req, res) => {
  const { id } = req.params;
  const reviews = loadJson(reviewsPath);
  const next = reviews.filter((r) => r.id !== id);
  saveJson(reviewsPath, next);
  res.json({ ok: true });
});

// Profanity list API
app.get('/api/profanity', (req, res) => {
  res.json(loadJson(profanityPath));
});

app.put('/api/profanity', (req, res) => {
  const list = Array.isArray(req.body) ? req.body : req.body?.list;
  if (!Array.isArray(list)) return res.status(400).json({ error: 'invalid_list' });
  saveJson(profanityPath, list.map((s) => String(s).toLowerCase().trim()).filter(Boolean));
  res.json({ ok: true });
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
});

