import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/Views/HomeView.vue'
import DetailView from '@/Views/DetailView.vue'
import MyPage from '@/Views/MyPage.vue'
import SignUpView from '@/AccountsViews/SignUp.vue'
import LoginView from '@/AccountsViews/Login.vue'

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
    component: MyPage 
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
