import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/Views/HomeView.vue'
import DetailView from '@/Views/DetailView.vue'
import MyPage from '@/Views/MyPage.vue'

const routes = [
  { 
    path: '/', 
    name: 'home', 
    component: HomeView 
  },
  { 
    path: '/detail/:id',
    name: 'detail',
    component: DetailView
   },
  { 
    path: '/mypage', 
    name: 'mypage', 
    component: MyPage }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
