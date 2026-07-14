import { createRouter, createWebHistory } from 'vue-router'
import { jwtDecode } from "jwt-decode";

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
      meta: { requiresAuth: true },
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


router.beforeEach((to) => {
  if (!to.meta.requiresAuth) return true

  const token = localStorage.getItem("token")
  if (!token) {
    return { path: "/login", query: { redirect: to.fullPath } }
  }

  let decoded
  try {
    decoded = jwtDecode(token)
  } catch (err) {
    console.error(err)
    return { path: "/login", query: { redirect: to.fullPath } }
  }

  const exp = decoded?.exp
  if (!exp) {
    return { path: "/login", query: { redirect: to.fullPath } }
  }

  const now = Math.floor(Date.now() / 1000)

  // Means the token has been expired.
  if (now >= exp) {
    localStorage.removeItem("token")
    return { path: "/login", query: { redirect: to.fullPath } }
  }

  return true
})


export default router
