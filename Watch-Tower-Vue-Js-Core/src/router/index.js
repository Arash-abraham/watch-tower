import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import TargetsPage from '../components/TargetsPage.vue'
import AppsPage from '../components/AppsPage.vue'
import DashboardPage from '../components/DashboardPage.vue'
import MonitorsPage from '../components/MonitorsPage.vue'
import AlertsPage from '../components/AlertsPage.vue'

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
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router