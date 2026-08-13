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
  routes
})

export default router