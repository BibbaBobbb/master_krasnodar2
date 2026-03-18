<template>
  <section class="page contacts">
    <h2>Контакты</h2>
    <img :src="face" class="contact-photo" alt="Николай, частный мастер">
    <p class="center">
      <a class="contact" href="mailto:nikolai.anna07.06@mail.ru">email: nikolai.anna07.06@mail.ru</a>
    </p>
    <p class="center">
      <!-- Десктоп: не кликабельно -->
      <span class="contact phone-desktop">телефон: +7(988)-283-00-09</span>
      <!-- Мобилка: кликабельно -->
      <a class="contact phone-mobile" href="tel:+79882830009">телефон: +7(988)-283-00-09</a>
    </p>
    <p class="center">
      <a class="contact" href="https://t.me/Kulikniko" target="_blank" rel="noopener">telegram: @Kulikniko</a>
    </p>
  </section>
</template>

<script>
import face from '@/assets/master_face.jpeg';
export default {
  name: 'ContactsPage',
  data() {
    return { face };
  },
};
</script>

<style scoped>
.page {
  padding: 20px 0;
}
.contact-photo {
  display: block;
  margin: 8px auto 16px;
  max-width: 340px;
  width: 100%;
  border-radius: 10px;
}
.center {
  text-align: center;
  margin: 12px 0; /* больше расстояние между строками */
}
.contact {
  font-weight: 700;
  color: #fff;
  text-decoration: none;
  font-size: 20px;     /* немного больше шрифт */
  line-height: 2;      /* в 2 раза больше межстрочный интервал */
}
.contact:hover {
  color: #ffd59c;
  text-decoration: underline;
}

/* По умолчанию показываем десктопную версию, скрываем мобильную */
.phone-mobile { display: none; }
.phone-desktop { display: inline; }

/* На мобильных — наоборот */
@media (max-width: 768px) {
  .phone-mobile { display: inline; }
  .phone-desktop { display: none; }
  .page { padding: 16px 0; }
  .contact { font-size: 16px; line-height: 1.6; }
  .center { margin: 10px 0; }
  .contact-photo { max-width: 260px; margin: 6px auto 12px; }
}
</style>

