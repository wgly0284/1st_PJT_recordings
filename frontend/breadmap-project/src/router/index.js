import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/Views/HomeView.vue'
import DetailView from '@/Views/DetailView.vue'
import MyPage from '@/Views/MyPage.vue'
import SignUpView from '@/AccountsViews/SignUp.vue'
import LoginView from '@/AccountsViews/Login.vue'
import MyReviews from '@/components/MyPage/MyReviews.vue'
import ReviewDetail from '@/components/ReviewDetail.vue'
import NewReview from '@/components/MyPage/NewReview.vue'
import CommunityMain from '@/components/community/CommunityMain.vue'

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
    path: '/mypage/editprofile',
    name: 'editprofile',
    component: EditProfile
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
  },
  {
    path: '/myreview',
    name: 'myreview',
    component: MyReviews
  },
  {
    path: '/myreview/:id',
    name: 'myreview_id',
    component: ReviewDetail
  },
  {
    path: '/myreview/new',
    name: 'newReview',
    component: NewReview
  },
  {
    path: '/community',
    name: 'community',
    component: CommunityMain
  }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
