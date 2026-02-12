import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/login', name: 'Login', component: () => import('./views/LoginView.vue') },
  { path: '/register', name: 'Register', component: () => import('./views/RegisterView.vue') },
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: () => import('./views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/employees', name: 'Employees', component: () => import('./views/EmployeesView.vue'), meta: { requiresAuth: true } },
  { path: '/employees/:id', name: 'EmployeeDetail', component: () => import('./views/EmployeeDetailView.vue'), meta: { requiresAuth: true } },
  { path: '/departments', name: 'Departments', component: () => import('./views/DepartmentsView.vue'), meta: { requiresAuth: true } },
  { path: '/positions', name: 'Positions', component: () => import('./views/PositionsView.vue'), meta: { requiresAuth: true } },
  { path: '/events', name: 'Events', component: () => import('./views/EventsView.vue'), meta: { requiresAuth: true } },
  { path: '/reports', name: 'Reports', component: () => import('./views/ReportsView.vue'), meta: { requiresAuth: true } },
  { path: '/admin', name: 'Admin', component: () => import('./views/AdminView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/guide', name: 'Guide', component: () => import('./views/GuideView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
