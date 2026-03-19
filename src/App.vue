<template>
  <div id="layout">
    <header>
      <h1 style="position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0;">Мастер на час в Краснодаре — ремонт Краснодар: ремонт бытовой техники и сантехники САНТЕХСТРОЙ</h1>
      <h1 class="hero-title">СантехЭлектро</h1>
      <nav>
        <!-- router-link заменяет обычные <a> -->
        <router-link to="/#services">Услуги</router-link>
        <router-link to="/services#request">Оставить заявку</router-link>
        <router-link to="/reviews#reviews">Отзывы</router-link>
        <router-link to="/contacts#contacts">Контакты</router-link>
      </nav>
    </header>

    <main class="container">
      <router-view />
    </main>

    <footer>
      <p>Краснодар. Без выходных с 8:00 до 22:00.</p>
      <p class="seo-footer">Наши услуги "Муж на час" и "Мастер на час" доступны во всех районах Краснодара (ФМР, ЮМР, Центр, ГМР). Мы специализируемся на качественном ремонте бытовой техники, сантехнических и электромонтажных работах с гарантией. Ремонт Краснодар, Ремонт КРД.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
export {};
</script>

<style>
html { scroll-behavior: smooth; }
/* 1. БАЗОВЫЕ НАСТРОЙКИ */
body { 
    font-family: 'Segoe UI', Roboto, sans-serif; 
    margin: 0; 
    /* Фон ниже шапки с более явной вуалью для «разбавления» */
    background: linear-gradient(rgba(255,255,255,0.25), rgba(255,255,255,0.25)), url('@/../public/фото3.jpg') center/cover no-repeat fixed; 
    color: #333; 
}

/* 2. ШАПКА */
header { 
    background: linear-gradient(rgba(44,62,80,0.65), rgba(44,62,80,0.65)), url('/фото инстурментов.jpg') center/cover no-repeat;
    padding: 50px 20px; 
    text-align: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 100px; /* Ещё выше над контентом */
}

.hero-title { 
    color: #f39c12; 
    font-size: 60px; /* Вернули прежний размер */
    margin-bottom: 30px; 
    text-transform: uppercase; 
    letter-spacing: 3px; 
}

/* 3. НАВИГАЦИЯ (БОЛЬШИЕ КНОПКИ) */
nav {
    display: flex;
    justify-content: center;
    gap: 120px; /* Расстояние между кнопками, чтобы влезали в один ряд */
    flex-wrap: nowrap; /* На десктопе в один ряд */
}

/* Стиль для router-link (во Vue они превращаются в <a>) */
nav a { 
    display: inline-block;
    color: white; 
    text-decoration: none; 
    background: #f39c12; 
    padding: 16px 38px; /* Чуть уменьшили кнопки */
    border-radius: 44px; 
    font-size: 20px;    /* Чуть уменьшили шрифт */
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 6px 15px rgba(243, 156, 18, 0.3);
    border: 2px solid transparent;
}

nav a:hover { 
    background: #e67e22; 
    transform: translateY(-3px) scale(1.05); /* Эффект парения */
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* СТИЛЬ ДЛЯ НАЖАТОЙ КНОПКИ (Vue автоматически добавляет этот класс) */
.router-link-active {
    background: #2c3e50 !important; 
    color: #f39c12 !important;
    border: 2px solid #f39c12 !important;
}

/* 4. КОНТЕНТ (СЕКЦИИ) */
.container { 
    max-width: 1000px; 
    margin: 40px auto; 
    background: transparent; 
    padding: 40px; 
    border-radius: 15px; 
    box-shadow: none; 
}

/* Тексты под шапкой — белые */
.container,
.container h1,
.container h2,
.container h3,
.container p,
.container li,
.container a {
    color: #fff;
}

h2 { 
    color: #2c3e50; 
    border-left: 6px solid #f39c12; 
    padding-left: 20px; 
    font-size: 30px;
}

/* 5. ПОДВАЛ */
footer { 
    background: #2c3e50; 
    color: white; 
    text-align: center; 
    padding: 40px; 
    margin-top: 60px; 
}
.seo-footer {
    max-width: 1000px;
    margin: 8px auto 0;
    font-size: 13px; /* 12–14px */
    color: #cfd6de; /* светло‑серый */
    line-height: 1.5;
}

/* 6. МОБИЛЬНАЯ ВЕРСИЯ */
@media (max-width: 768px) {
    nav {
        flex-wrap: wrap;   /* На мобиле можно переносить */
        gap: 12px;
    }
    nav a { 
        width: 90%; /* На телефоне кнопки во всю ширину */
        text-align: center;
        padding: 10px 0;
        font-size: 15px;
    }
    .hero-title { font-size: 28px; }
    .container {
        margin: 20px auto;
        padding: 20px;
    }
}

</style>
