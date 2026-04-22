import { createRouter, createWebHistory } from 'vue-router'
import ChatPage from './ChatPage.vue'
import AdminLogin from './AdminLogin.vue'
import AdminDashboard from './AdminDashboard.vue'

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/chat', name: 'chat', component: ChatPage },
  { path: '/admin/login', name: 'admin-login', component: AdminLogin },
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    try {
      const res = await fetch('/api/admin/check')
      const data = await res.json()
      if (data.logged_in) {
        next()
      } else {
        next('/admin/login')
      }
    } catch (e) {
      next('/admin/login')
    }
  } else if (to.path === '/admin/login') {
    try {
      const res = await fetch('/api/admin/check')
      const data = await res.json()
      if (data.logged_in) {
        next('/admin')
      } else {
        next()
      }
    } catch (e) {
      next()
    }
  } else {
    next()
  }
})

export default router