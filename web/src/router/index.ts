import { createRouter, createWebHistory } from 'vue-router'

import NotFound from '@/views/NotFound.vue'
import UserLayout from '@/views/UserLayout.vue'
import AdminLayout from '@/views/AdminLayout.vue'
import LoginView from '@/views/LoginView.vue'
import AdminHomeView from '@/views/AdminHomeView.vue'
import AdminPastesView from '@/views/AdminPastesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'userLayout',
      component: UserLayout
    },
    {
      path: '/:shortcode',
      name: 'view',
      component: UserLayout
    },
    {
      path: '/admin',
      component: AdminLayout,
      children: [
        {
          path: '',
          name: 'admin.dashboard',
          component: AdminHomeView,
        },
        {
          path: 'pastes',
          name: 'admin.pastes',
          component: AdminPastesView,
        },
      ],
    },
    {
      path: '/login',
      name: 'login-view',
      component: LoginView,
    },
    {
      path: '/:pathMatch(.*)*',
      component: NotFound
    },
  ],
})

export default router
