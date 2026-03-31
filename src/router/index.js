import { createRouter, createWebHistory } from 'vue-router';
import MainInfo from '@/components/MainInfo.vue';

const Services = () => import('@/pages/Services.vue');
const Contacts = () => import('@/pages/Contacts.vue');
const Reviews = () => import('@/pages/Reviews.vue');
const AdminProfanity = () => import('@/pages/AdminProfanity.vue');
const AdminReviews = () => import('@/pages/AdminReviews.vue');

const routes = [
  { path: '/', name: 'home', component: MainInfo },
  { path: '/services', name: 'services', component: Services },
  { path: '/reviews', name: 'reviews', component: Reviews },
  { path: '/contacts', name: 'contacts', component: Contacts },
  { path: '/admin/profanity', name: 'admin-profanity', component: AdminProfanity },
  { path: '/admin/reviews', name: 'admin-reviews', component: AdminReviews },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 1) Если есть сохранённая позиция (назад/вперёд) — восстанавливаем
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' };
    }
    if (savedPosition) {
      return { ...savedPosition, behavior: 'smooth' };
    }
    // 2) Без hash — скроллим к ключевым секциям по маршруту
    // Это помогает, когда секция уже на странице, но переход без #якоря
    if (to.name === 'services') {
      return { el: '#request', behavior: 'smooth' };
    }
    if (to.name === 'reviews') {
      return { el: '#reviews', behavior: 'smooth' };
    }
    if (to.name === 'contacts') {
      return { el: '#contacts', behavior: 'smooth' };
    }
    // Домой — к началу
    return { left: 0, top: 0, behavior: 'smooth' };
  },
});

export default router;

