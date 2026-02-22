import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import LoginPage from '../views/LoginPage.vue'
// ...existing code...
import RegisterPage from '../views/RegisterPage.vue'
import { useAuthStore } from '../stores/auth.store'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  // ...existing code...
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'), 
    meta: { requiresAuth: true }, // Set to true when auth is implemented
  },
  {
    path: '/lecture/:id',
    name: 'LectureTake',
    component: () => import('../views/LecturePage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/achievements',
    name: 'Achievements',
    component: () => import('../views/AchievementsPage.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: () => import('../views/RankingPage.vue'),
    meta: { requiresAuth: true },
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Authentication guard
router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta?.requiresAuth

  // If route requires authentication
  if (requiresAuth && !authStore.isLoggedIn) {
    // Redirect to login page
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // If user is authenticated and tries to access login/register, redirect to dashboard
  if ((to.name === 'Login' || to.name === 'Register') && authStore.isLoggedIn) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
