<template>
  <section id="services" class="master-box">
    <h2 class="seo-h2">Ремонт в Краснодаре — сантехника, электрика и бытовая техника</h2>
    <h2>Услуги</h2>
    <p>Я ваш частный мастер: сантехник и электрик.</p>
    <p>Выполню сантехнические и электромонтажные работы с выездом на дом. Быстро, качественно, с гарантией.</p>

    <h3>Что делаю?</h3>
    <ul class="bullets">
      <li>установка и замена смесителей, унитазов, раковин, ванн, душевых кабин;</li>
      <li>устранение засоров и протечек;</li>
      <li>монтаж и ремонт электропроводки;</li>
      <li>замена и установка розеток, выключателей, светильников;</li>
      <li>подключение бытовой техники;</li>
      <li>и ещё многое другое…</li>
    </ul>

    <h3>Почему стоит выбрать меня:</h3>
    <ul class="bullets">
      <li>опыт работы — 10 лет;</li>
      <li>привожу все необходимые инструменты;</li>
      <li>фиксированные цены — без скрытых платежей;</li>
      <li>даю гарантию на выполненные работы;</li>
      <li>выезжаю в день обращения;</li>
      <li>работаю без выходных — помогу даже в экстренной ситуации.</li>
    </ul>

    <p><strong>Без выходных с 08:00 до 22:00.</strong> Районы выезда: по договоренности.</p>
  </section>
</template>

<script>
export default {
  name: 'MainInfo',
};
</script>

<style scoped>
.master-photo {
  display: block;
  margin: 0 auto 16px;
  max-width: 440px; /* в 2 раза больше */
  width: 100%;
  border-radius: 8px;
}
.bullets {
  margin: 8px 0 16px;
  padding-left: 20px;
}
.master-box h2 {
  font-size: 36px;
}
.seo-h2 {
  font-size: 0; /* компактный незаметный заголовок с ключом, без визуального сдвига */
  height: 0;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
.master-box p,
.master-box .bullets li {
  font-size: 20px;       /* базовый размер больше */
  line-height: 1.75;     /* комфортный интерлиньяж */
  font-weight: 600;      /* жирнее шрифт */
}
.master-box .bullets li + li {
  margin-top: 6px;       /* немного расстояния между пунктами */
}

@media (max-width: 768px) {
  .master-photo {
    max-width: 280px;
    margin-bottom: 12px;
  }
  .master-box h2 {
    font-size: 24px;
  }
  .master-box p,
  .master-box .bullets li {
    font-size: 18px;
    line-height: 1.7;
    font-weight: 600;    /* жирнее шрифт на мобильном */
  }
}

/* Тексты этого блока — белые, увеличенные на десктопе */
.master-box { color: #fff; }
.master-box h2 { color: #fff; }
@media (min-width: 769px) {
  .master-box h2 { font-size: 44px; }
  .master-box p, .master-box .bullets li { color: #fff; font-size: 24px; line-height: 1.85; font-weight: 700; }
}
</style>