import { createRouter, createWebHistory } from 'vue-router'
import ChatPage from './ChatPage.vue'
import AdminLogin from './AdminLogin.vue'
import AdminDashboard from './AdminDashboard.vue'

const routes = [
  { path: '/', name: 'chat', component: ChatPage },
  { path: '/admin/login', name: 'admin-login', component: AdminLogin },
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router