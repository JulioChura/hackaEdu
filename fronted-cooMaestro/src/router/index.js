import { createRouter, createWebHistory } from 'vue-router'

// Public / Auth
const Home = () => import('../views/Home.vue')

// Teacher views
const TeacherDashboard = () => import('../views/teacher/dashboard/TeacherDashboard.vue')
const TeacherCourses = () => import('../views/teacher/courses/TeacherCourses.vue')

// Teacher layout (parent for teacher routes)
const TeacherLayout = () => import('../views/teacher/Teacher.vue')

// Student views (placeholders)
const StudentDashboard = () => import('../views/student/dashboard/StudentDashboard.vue')
const StudentCourses = () => import('../views/student/courses/StudentCourses.vue')

// Generic courses page (optional)
const Courses = () => import('../views/teacher/courses/TeacherCourses.vue')

const routes = [
  // Public / auth
  { path: '/', name: 'Home', component: Home },

  // Teacher area
  {
    path: '/teacher',
    name: 'Teacher',
    component: TeacherLayout,
    meta: { requiresAuth: true, role: 'teacher' },
    children: [
      { path: '', redirect: { name: 'TeacherDashboard' } },
      { path: 'dashboard', name: 'TeacherDashboard', component: TeacherDashboard, meta: { role: 'teacher' } },
      { path: 'courses', name: 'TeacherCourses', component: TeacherCourses, meta: { role: 'teacher' } },
      { path: 'courses/:id', name: 'TeacherCourseDetail', component: TeacherCourses, meta: { role: 'teacher' }, props: true },
    ],
  },

  // Student area
  {
    path: '/student',
    name: 'Student',
    meta: { requiresAuth: true, role: 'student' },
    children: [
      { path: '', redirect: { name: 'StudentDashboard' } },
      { path: 'dashboard', name: 'StudentDashboard', component: StudentDashboard, meta: { role: 'student' } },
      { path: 'courses', name: 'StudentCourses', component: StudentCourses, meta: { role: 'student' } },
      { path: 'courses/:id', name: 'StudentCourseDetail', component: StudentCourses, meta: { role: 'student' }, props: true },
    ],
  },

  // Generic/public courses listing
  { path: '/courses', name: 'Courses', component: Courses },

  // Fallback -> home
  { path: '/:pathMatch(.*)*', redirect: '/' },
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
