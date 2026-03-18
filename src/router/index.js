import { createRouter, createWebHistory } from 'vue-router';
import MainInfo from '@/components/MainInfo.vue';

const Services = () => import('@/pages/Services.vue');
const Contacts = () => import('@/pages/Contacts.vue');
const Reviews = () => import('@/pages/Reviews.vue');
const AdminProfanity = () => import('@/pages/AdminProfanity.vue');

const routes = [
  { path: '/', name: 'home', component: MainInfo },
  { path: '/services', name: 'services', component: Services },
  { path: '/reviews', name: 'reviews', component: Reviews },
  { path: '/contacts', name: 'contacts', component: Contacts },
  { path: '/admin/profanity', name: 'admin-profanity', component: AdminProfanity },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { left: 0, top: 0 };
  },
});

export default router;

