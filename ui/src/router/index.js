import { createRouter, createWebHistory } from 'vue-router'

// Import your components
import Home from '../components/Home.vue'

const routes = [
  {
    path: '/home',
    name: 'Home1',
    component: Home
  },
  {
    path: '/',
    name: 'Home2',
    component: Home
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
