import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/Content/HomePage.vue'
import TargetsPage from '../components/Content/TargetsPage.vue'
import AppsPage from '../components/Content/AppsPage.vue'
import DashboardPage from '../components/Content/DashboardPage.vue'
import MonitorsPage from '../components/Content/MonitorsPage.vue'
import AlertsPage from '../components/Content/AlertsPage.vue'
import setting from '../components/Content/setting.vue'

const routes = [
  { 
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage
  },
  {
    path: '/apps',
    name: 'apps',
    component: AppsPage
  },
  {
    path: '/targets',
    name: 'targets',
    component: TargetsPage
  },
  {
    // Full dossier for a single program: complete in-scope and
    // out-of-scope lists with client-side pagination (no truncation).
    path: '/programs/:id',
    name: 'program-detail',
    component: () => import('../components/Content/ProgramDetailPage.vue'),
    props: true
  },
  {
    path: '/monitors',
    name: 'monitors',
    component: MonitorsPage
  },
  {
    path: '/alerts',
    name: 'alerts',
    component: AlertsPage
  },
  {
    path: '/setting',
    name: 'setting',
    component: setting
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, top: 96, behavior: 'smooth' }
    return { top: 0 }
  }
})

export default router