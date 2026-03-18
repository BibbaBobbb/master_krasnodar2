<template>
  <section class="page">
    <h2>Админ: Список плохих слов</h2>
    <p class="hint">По одному слову на строку. Будут сохранены в нижнем регистре, без пустых строк.</p>

    <textarea
      v-model="raw"
      class="textarea"
      rows="14"
      placeholder="Введите слова, каждое с новой строки"
    />

    <div class="actions">
      <button class="btn" @click="loadList" :disabled="loading">Обновить с сервера</button>
      <button class="btn primary" @click="saveList" :disabled="loading">Сохранить</button>
    </div>

    <p v-if="message" :class="['msg', error ? 'error' : 'ok']">{{ message }}</p>
  </section>
</template>

<script>
export default {
  name: 'AdminProfanity',
  data() {
    return {
      raw: '',
      loading: false,
      message: '',
      error: false,
    };
  },
  methods: {
    async loadList() {
      this.loading = true;
      this.message = '';
      this.error = false;
      try {
        const r = await fetch('/api/profanity');
        const list = await r.json();
        this.raw = Array.isArray(list) ? list.join('\n') : '';
      } catch (e) {
        this.message = 'Не удалось загрузить список';
        this.error = true;
      } finally {
        this.loading = false;
      }
    },
    async saveList() {
      this.loading = true;
      this.message = '';
      this.error = false;
      const list = this.raw
        .split('\n')
        .map(s => String(s).toLowerCase().trim())
        .filter(Boolean);
      try {
        const r = await fetch('/api/profanity', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(list),
        });
        if (!r.ok) throw new Error('save_failed');
        this.message = 'Сохранено';
        this.error = false;
      } catch (e) {
        this.message = 'Ошибка сохранения';
        this.error = true;
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.loadList();
  },
};
</script>

<style scoped>
.page { padding: 20px 0; max-width: 760px; margin: 0 auto; }
.hint { color: #666; margin-bottom: 8px; }
.textarea {
  width: 100%; box-sizing: border-box; padding: 10px 12px;
  border: 1px solid #ddd; border-radius: 8px; font-size: 16px; resize: vertical;
}
.actions { display: flex; gap: 10px; margin-top: 12px; }
.btn {
  background: #2c3e50; color: #fff; border: none; padding: 10px 16px;
  border-radius: 8px; cursor: pointer;
}
.btn.primary { background: #f39c12; color: #fff; }
.btn:disabled { opacity: .6; cursor: not-allowed; }
.msg { margin-top: 10px; font-weight: 600; }
.msg.ok { color: #2e7d32; }
.msg.error { color: #c62828; }
</style>

