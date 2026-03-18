<template>
  <section class="page">
    <h2>Отзывы</h2>

    <form class="review-form" @submit.prevent="submitReview">
      <div v-if="showKindnessWarning" class="warning" role="alert" aria-live="assertive">
        <span class="warn-icon">!</span>
        <span class="warn-text">Будьте добрее!</span>
      </div>

      <label class="label">Ваша оценка:</label>
      <div class="stars" @mouseleave="hoverRating = 0">
        <button
          v-for="n in 5"
          :key="n"
          type="button"
          class="star"
          :aria-label="`Оценка ${n}`"
          @mouseenter="hoverRating = n"
          @click="rating = n"
        >
          {{ (hoverRating || rating) >= n ? '★' : '☆' }}
        </button>
      </div>

      <label class="label" for="name">Имя:</label>
      <input id="name" v-model.trim="name" class="input" type="text" placeholder="Ваше имя" />

      <label class="label" for="text">Отзыв:</label>
      <textarea
        id="text"
        v-model.trim="text"
        class="textarea"
        rows="6"
        placeholder="Здесь будет Ваш отзыв :)"
      ></textarea>

      <label class="label" for="photo">Фото выполненной работы:</label>
      <input
        id="photo"
        ref="fileInput"
        class="input"
        type="file"
        accept="image/*"
        @change="onFileChange"
      />

      <button class="submit" type="submit" :disabled="!canSubmit">Отправить отзыв</button>
    </form>

    <div v-if="reviews.length" class="review-list">
      <div class="reviews-toolbar">
        <label for="sort" class="label small">Сортировка:</label>
        <select id="sort" v-model="sortMode" class="input select">
          <option value="date_desc">По дате: новые сначала</option>
          <option value="date_asc">По дате: старые сначала</option>
          <option value="rating_desc">По оценке: от 5 к 1</option>
          <option value="rating_asc">По оценке: от 1 к 5</option>
        </select>
      </div>
      <h3 class="list-title">Оставленные отзывы</h3>
      <article v-for="r in orderedReviews" :key="r.id" class="review">
        <header class="review-header">
          <div class="review-name">{{ r.name }}</div>
          <div class="review-meta">
            <span class="review-stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
            <span class="review-date">{{ formatDate(r.createdAt) }}</span>
          </div>
        </header>
        <p class="review-text">{{ r.text }}</p>
        <img v-if="r.imageDataUrl" :src="r.imageDataUrl" alt="Фото к отзыву" class="review-image" />
      </article>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ReviewsPage',
  data() {
    return {
      rating: 0,
      hoverRating: 0,
      name: '',
      text: '',
      selectedFile: null,
      reviews: [],
      sortMode: 'date_desc',
      showKindnessWarning: false,
    };
  },
  computed: {
    canSubmit() {
      return this.rating > 0 && this.name.length > 0 && this.text.length > 0;
    },
    orderedReviews() {
      const arr = [...this.reviews];
      switch (this.sortMode) {
        case 'date_asc':
          return arr.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
        case 'rating_desc':
          return arr.sort((a, b) => b.rating - a.rating || new Date(b.createdAt) - new Date(a.createdAt));
        case 'rating_asc':
          return arr.sort((a, b) => a.rating - b.rating || new Date(a.createdAt) - new Date(b.createdAt));
        case 'date_desc':
        default:
          return arr.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      }
    },
  },
  methods: {
    onFileChange(e) {
      const file = e.target.files && e.target.files[0] ? e.target.files[0] : null;
      this.selectedFile = file;
    },
    readFileAsDataUrl(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = (err) => reject(err);
        reader.readAsDataURL(file);
      });
    },
    formatDate(iso) {
      try {
        return new Date(iso).toLocaleString('ru-RU');
      } catch (e) {
        return iso;
      }
    },
    normalizeText(s) {
      return (s || '')
        .toLowerCase()
        .replace(/\s+/g, ' ')
        .trim();
    },
    containsProfanity(text) {
      const t = this.normalizeText(text);
      const bad = [
        'хуй','хуе','хуя','пизд','бля','еба','ебл','ебу','сука','мраз','гандон','дерьмо','говн','мудак','с*ка','шлюх','пидор','нахер','нахуй'
      ];
      return bad.some(w => t.includes(w));
    },
    tryNotifyTelegram(review) {
      const msg = `Нецензурный отзыв:
Имя: ${review.name}
Оценка: ${review.rating}
Текст: ${review.text}
Дата: ${this.formatDate(review.createdAt)}`;
      const tgDeep = `tg://resolve?domain=Kulikniko&text=${encodeURIComponent(msg)}`;
      const tgShare = `https://t.me/share/url?text=${encodeURIComponent(msg)}`;
      const win = window.open(tgDeep, '_blank');
      if (!win) {
        window.location.href = tgShare;
      } else {
        setTimeout(() => {
          try { win.location.href = tgShare; } catch (e) { console.warn('Telegram share redirect failed', e); }
        }, 800);
      }
    },
    async submitReview() {
      // 1) Фильтр мата на клиенте
      if (this.containsProfanity(this.name) || this.containsProfanity(this.text)) {
        this.showKindnessWarning = true;
        const badReview = {
          name: this.name,
          text: this.text,
          rating: this.rating,
          createdAt: new Date().toISOString(),
        };
        this.tryNotifyTelegram(badReview);
        this.hoverRating = 0;
        return;
      } else {
        this.showKindnessWarning = false;
      }
      // 2) Читаем файл в base64 (если есть)
      let imageDataUrl = '';
      if (this.selectedFile) {
        try {
          imageDataUrl = await this.readFileAsDataUrl(this.selectedFile);
        } catch (e) {
          console.warn('Failed to read attached image, continue without image', e);
        }
      }
      // 3) Правило публикации: публикуем только 4 и 5 звёзд; 1–3 — только в Telegram
      const ratingNum = Number(this.rating);
      if (ratingNum < 4) {
        const reviewForTg = {
          name: this.name,
          text: this.text,
          rating: this.rating,
          createdAt: new Date().toISOString(),
        };
        this.tryNotifyTelegram(reviewForTg);
        // очистка формы
        this.rating = 0;
        this.hoverRating = 0;
        this.name = '';
        this.text = '';
        this.selectedFile = null;
        if (this.$refs.fileInput) this.$refs.fileInput.value = '';
        alert('Спасибо за отзыв!');
        return;
      }
      // 4) Публикуем локально (и сохраняем в localStorage)
      const review = {
        id: Date.now().toString(),
        name: this.name,
        text: this.text,
        rating: this.rating,
        imageDataUrl,
        createdAt: new Date().toISOString(),
      };
      this.reviews.unshift(review);
      try {
        localStorage.setItem('reviews', JSON.stringify(this.reviews));
      } catch (e) {
        console.warn('Persisting reviews to localStorage failed', e);
      }
      // очистка формы
      this.rating = 0;
      this.hoverRating = 0;
      this.name = '';
      this.text = '';
      this.selectedFile = null;
      if (this.$refs.fileInput) this.$refs.fileInput.value = '';
      alert('Спасибо за отзыв!');
    },
  },
  created() {
    // загружаем локальные отзывы
    try {
      const raw = localStorage.getItem('reviews');
      this.reviews = raw ? JSON.parse(raw) : [];
    } catch (e) {
      this.reviews = [];
    }
  },
};
</script>

<style scoped>
.page {
  padding: 20px;
  background: transparent;
  color: #fff;         /* белый шрифт под шапкой (форма/заголовки) */
  border-radius: 12px;
}
.review-form { max-width: 640px; margin: 0 auto; }
.label { display: block; margin: 12px 0 6px; font-weight: 600; }
.stars { display: flex; gap: 8px; margin-bottom: 12px; justify-content: center; }
.star {
  font-size: 34px; line-height: 1; cursor: pointer; background: none; border: none; padding: 0; color: #f39c12;
}
.input, .textarea {
  width: 100%; box-sizing: border-box; padding: 10px 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px;
}
.textarea { resize: vertical; }
.submit {
  margin-top: 14px; background: #2c3e50; color: #fff; border: none; padding: 10px 16px; border-radius: 8px; cursor: pointer;
}
.submit:disabled { opacity: .6; cursor: not-allowed; }

.review-list { max-width: 760px; margin: 16px auto 0; }
.list-title { text-align: center; margin: 0 0 6px; }
.review {
  background: #e9e9e9; /* единый серый прямоугольник для всего отзыва */
  border: 1px solid #dcdcdc;
  border-radius: 12px;
  padding: 4px 10px 8px;   /* меньше сверху под именем, больше снизу под текстом */
  margin: 6px 0;       /* меньше расстояние между отзывами */
}
.review-header { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap; margin: 0; }
.review-name { font-weight: 700; color: #000; background: transparent !important; }
.review-meta { color: #000; font-size: 14px; display: flex; gap: 10px; align-items: center; background: transparent !important; }
.review-stars { color: #f39c12; font-weight: 700; }
.review p { margin: 0; }
.review-text { margin: 2px 0 8px; line-height: 1.6; white-space: pre-wrap; color: #000; background: transparent !important; }
.review { color: #000; } /* вся информация отзыва чёрным */
.review-image { max-width: 100%; width: 100%; height: auto; border-radius: 8px; margin: 4px 0 0; }
.review > *:last-child { margin-bottom: 0; }
/* На всякий случай уберём любые заливки внутри отзыва */
.review *:not(.review) {
  background: transparent;
}

.reviews-toolbar { display: flex; align-items: center; justify-content: flex-end; gap: 8px; margin-bottom: 8px; }
.select { width: auto; padding-right: 28px; }

.warning {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #ffe6e6;
  color: #c0392b;
  border: 1px solid #e74c3c;
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 10px;
  font-weight: 700;
}
.warn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #e74c3c;
  color: #fff;
  font-weight: 900;
}
</style>

