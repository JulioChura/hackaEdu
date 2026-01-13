import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Optional: global guard example (auth/role) — actual auth check to be implemented in app
router.beforeEach((to, from, next) => {
  // In development we allow navigation without auth so you can work on routes
  if (import.meta.env && import.meta.env.DEV) return next()

  const requiresAuth = to.meta?.requiresAuth
  const roleRequired = to.meta?.role

  // If route requires auth, you should check your auth state (placeholder logic)
  if (requiresAuth) {
    // Example placeholder: read role from localStorage (replace with real store)
    const userRole = localStorage.getItem('role') || null
    const isAuthenticated = !!userRole

    if (!isAuthenticated) return next({ name: 'Home' })
    if (roleRequired && userRole !== roleRequired) return next({ name: 'Home' })
  }

  next()
})

export default router
