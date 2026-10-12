import { createRouter, createWebHistory } from 'vue-router'
import { jwtDecode } from "jwt-decode";

import NotFound from '@/views/NotFound.vue'
import UserLayout from '@/views/UserLayout.vue'
import AdminLayout from '@/views/AdminLayout.vue'
import LoginView from '@/views/LoginView.vue'
import AdminHomeView from '@/views/AdminHomeView.vue'
import AdminPastesView from '@/views/AdminPastesView.vue'
import AdminBrandingView from '@/views/AdminBrandingView.vue'

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
        {
          path: 'branding',
          name: 'admin.branding',
          component: AdminBrandingView
        }
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

// Check to see if the token looks, and is valid. Only for protectedRoutes.
router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true

  let login_route = { name: "login-view", query: { redirect: to.fullPath } }

  const token = localStorage.getItem("token")
  if (!token) {
    return login_route
  }

  let decoded
  try {
    decoded = jwtDecode(token)
  } catch (err) {
    console.error(err)
    return login_route
  }

  const exp = decoded?.exp
  if (!exp) {
    return login_route
  }

  const now = Math.floor(Date.now() / 1000)

  // Means the token has been expired.
  if (now >= exp) {
    localStorage.removeItem("token")
    return login_route
  }


  const response = await fetch("/api/management/am-i-admin",{
    headers: {
      Authorization: `Bearer ${token}`
    }
  })


  if (!response.ok) {
    return login_route
  }

  return true
})


export default router
