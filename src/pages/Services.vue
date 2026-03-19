<template>
  <section id="request" class="page">
    <div class="app-form">
      <h2 class="form-title">Оставить заявку</h2>

      <label class="label" for="name">Имя</label>
      <input
        id="name"
        v-model.trim="name"
        :class="['input', { invalid: !isNameValid }]"
        type="text"
        maxlength="10"
        @input="onNameInput"
        placeholder="Ваше имя"
      />

      <label class="label" for="phone">Телефон</label>
      <input
        id="phone"
        v-model.trim="phone"
        :class="['input', { invalid: !isPhoneValid }]"
        type="tel"
        inputmode="tel"
        maxlength="12"
        @input="onPhoneInput"
        placeholder="+7 (___) ___-__-__"
      />

      <label class="label" for="text">Что у Вас сломалось?</label>
      <textarea
        id="text"
        v-model.trim="text"
        :class="['textarea', { invalid: !isTextValid }]"
        rows="6"
        placeholder="Что у Вас сломалось?"
      ></textarea>

      <button
        class="submit"
        :class="{ invalid: !canSubmit }"
        type="button"
        :disabled="!canSubmit || sending"
        @click="submitApplication"
      >
        Отправить
      </button>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ServicesPage',
  data() {
    return {
      name: '',
      phone: '',
      text: '',
      sending: false,
    };
  },
  computed: {
    isNameValid() {
      return typeof this.name === 'string' && this.name.length > 0 && this.name.length <= 10;
    },
    isPhoneValid() {
      // Ожидаем формат +7XXXXXXXXXX (12 символов включая +)
      return typeof this.phone === 'string' && /^\+7\d{10}$/.test(this.phone);
    },
    isTextValid() {
      return typeof this.text === 'string' && this.text.trim().length > 0;
    },
    canSubmit() {
      return this.isNameValid && this.isPhoneValid && this.isTextValid;
    },
  },
  methods: {
    onNameInput() {
      // Разрешаем только буквы (RU/EN), максимум 10
      const onlyLetters = (this.name || '').replace(/[^A-Za-zА-Яа-яЁё]/g, '');
      this.name = onlyLetters.slice(0, 10);
    },
    onPhoneInput() {
      const raw = (this.phone || '').replace(/\D/g, '');
      if (!raw) { this.phone = ''; return; }
      // Нормализуем: 8XXXXXXXXXX -> 7XXXXXXXXXX
      let normalized = raw.startsWith('8') ? '7' + raw.slice(1) : raw;
      // Если не начинается с 7 — добавляем 7 как код РФ
      if (!normalized.startsWith('7')) normalized = '7' + normalized;
      // Берём ровно 10 цифр после кода страны
      const afterCode = normalized.slice(1, 11);
      this.phone = '+7' + afterCode;
    },
    async submitApplication() {
      if (!this.canSubmit) return;
      if (this.sending) return;
      this.sending = true;
      try {
        const resp = await fetch('/api/send-order', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: this.name, phone: this.phone, text: this.text }),
        });
        if (resp.ok) {
          alert('Ваша заявка принята!');
          this.name = '';
          this.phone = '';
          this.text = '';
        } else {
          alert('Попробуйте позже');
        }
      } catch (e) {
        alert('Попробуйте позже');
      } finally {
        this.sending = false;
      }
    },
  },
};
</script>

<style scoped>
.page {
  padding: 8px 0 20px; /* подняли контент выше */
}
.app-form {
  max-width: 640px;
  margin: 0 auto;
}
.form-title {
  text-align: center;
  font-size: 40px;       /* крупнее шрифт заголовка */
  line-height: 1.1;
  margin: -12px 0 12px;  /* сильно подняли вверх */
}
.label {
  display: block;
  margin: 12px 0 6px;
  font-weight: 600;
}
.input,
.textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}
.textarea {
  resize: vertical;
}
.submit {
  margin-top: 14px;
  background: #2c3e50;
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
}
.submit.invalid,
.submit:disabled {
  background: #e74c3c;
  cursor: not-allowed;
}
.input.invalid,
.textarea.invalid {
  border-color: #e74c3c;
  box-shadow: 0 0 0 2px rgba(231, 76, 60, 0.15);
}
.submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

