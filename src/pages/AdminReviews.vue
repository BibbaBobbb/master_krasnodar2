<template>
  <section class="page">
    <h2>Админ: Отзывы</h2>

    <div class="key-box" v-if="!apiKey">
      <label class="label" for="adminkey">API Key</label>
      <input id="adminkey" v-model.trim="keyInput" class="input" type="password" placeholder="Введите X-API-Key" />
      <button class="btn primary" @click="saveKey">Сохранить</button>
    </div>

    <div v-else class="toolbar">
      <span class="muted">Ключ загружен</span>
      <button class="btn" @click="changeKey">Сменить ключ</button>
      <button class="btn" @click="loadReviews">Обновить</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="loading" class="muted">Загрузка…</div>

    <ul v-if="reviews.length" class="list">
      <li v-for="r in reviews" :key="r.id" class="item">
        <header class="head">
          <strong>{{ r.name }}</strong>
          <span class="meta">★ {{ r.rating }} • {{ formatDate(r.createdAt) }}</span>
        </header>
        <p class="text">{{ r.text }}</p>
        <img v-if="r.imageDataUrl" :src="r.imageDataUrl" alt="Фото к отзыву" class="img" />
        <div class="actions">
          <button class="btn danger" @click="remove(r.id)">Удалить</button>
        </div>
      </li>
    </ul>

    <p v-else-if="!loading" class="muted">Отзывов нет.</p>
  </section>
</template>

<script>
export default {
  name: 'AdminReviews',
  data() {
    return {
      reviews: [],
      loading: false,
      error: '',
      apiKey: '',
      keyInput: '',
      robotsMetaEl: null,
    };
  },
  methods: {
    formatDate(iso) {
      try { return new Date(iso).toLocaleString('ru-RU'); } catch (e) { return iso; }
    },
    saveKey() {
      if (!this.keyInput) return;
      localStorage.setItem('adminApiKey', this.keyInput);
      this.apiKey = this.keyInput;
      this.keyInput = '';
      this.loadReviews();
    },
    changeKey() {
      localStorage.removeItem('adminApiKey');
      this.apiKey = '';
      this.reviews = [];
    },
    async loadReviews() {
      this.error = '';
      this.loading = true;
      try {
        const resp = await fetch('/api/reviews');
        const rows = await resp.json();
        this.reviews = Array.isArray(rows) ? rows : [];
      } catch (e) {
        this.error = 'Не удалось загрузить отзывы';
      } finally {
        this.loading = false;
      }
    },
    async remove(id) {
      if (!this.apiKey) { this.error = 'Нет API ключа'; return; }
      if (!confirm('Удалить отзыв?')) return;
      this.error = '';
      try {
        const resp = await fetch(`/api/reviews/${id}`, {
          method: 'DELETE',
          headers: { 'X-API-Key': this.apiKey },
        });
        if (!resp.ok) throw new Error('delete_failed');
        await this.loadReviews();
      } catch (e) {
        this.error = 'Не удалось удалить';
      }
    },
    ensureNoindex() {
      const m = document.createElement('meta');
      m.setAttribute('name', 'robots');
      m.setAttribute('content', 'noindex,nofollow');
      document.head.appendChild(m);
      this.robotsMetaEl = m;
    },
    removeNoindex() {
      if (this.robotsMetaEl && this.robotsMetaEl.parentNode) {
        this.robotsMetaEl.parentNode.removeChild(this.robotsMetaEl);
        this.robotsMetaEl = null;
      }
    },
  },
  mounted() {
    this.apiKey = localStorage.getItem('adminApiKey') || '';
    this.ensureNoindex();
    if (this.apiKey) this.loadReviews();
  },
  unmounted() {
    this.removeNoindex();
  },
};
</script>

<style scoped>
.page { padding: 16px 0; max-width: 900px; margin: 0 auto; color: #fff; }
.label { display: block; margin: 8px 0 4px; font-weight: 600; }
.input { width: 100%; padding: 10px 12px; border-radius: 8px; border: 1px solid #ddd; }
.btn { background: #2c3e50; color: #fff; border: none; padding: 8px 12px; border-radius: 8px; cursor: pointer; }
.btn.primary { background: #f39c12; }
.btn.danger { background: #c0392b; }
.muted { color: #cfd6de; font-size: 14px; }
.error { color: #ffb3b3; margin: 8px 0; }
.key-box { background: rgba(0,0,0,.2); padding: 12px; border-radius: 8px; }
.toolbar { display: flex; gap: 8px; align-items: center; margin: 8px 0; }
.list { list-style: none; margin: 12px 0 0; padding: 0; }
.item { background: #e9e9e9; color: #000; border: 1px solid #dcdcdc; border-radius: 12px; padding: 10px 12px; margin-bottom: 10px; }
.head { display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.meta { color: #333; font-size: 13px; }
.text { margin: 6px 0; white-space: pre-wrap; }
.img { max-width: 100%; display: block; border-radius: 8px; margin-top: 6px; }
.actions { margin-top: 8px; display: flex; gap: 8px; }
</style>

