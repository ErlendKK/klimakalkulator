import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Projects from '../views/Projects.vue'
import Products from '../views/Products.vue'
import Home from '../views/Home.vue'
import Results from '../views/Results.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/projects',
    name: 'projects',
    component: Projects
  },
  {
    path: '/products',
    name: 'products',
    component: Products
  },
  {
    path: '/results',
    name: 'results',
    component: Results
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router