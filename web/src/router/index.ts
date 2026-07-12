import { createRouter, createWebHistory } from 'vue-router'

import NotFound from '@/views/NotFound.vue'
import UserLayout from '@/views/UserLayout.vue'
import AdminLayout from '@/views/AdminLayout.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import LoginView from '@/views/LoginView.vue'

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
          component: AdminDashboard,
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
