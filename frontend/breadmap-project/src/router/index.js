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
import EditProfile from '@/components/MyPage/EditProfile.vue'
import MapPage from '@/Views/MapPage.vue'
import { useAuthStore } from '@/stores/auth'

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
    path: '/stores/:storeId?/newReview', // ? 추가: storeId를 선택적 파라미터로
    name: 'newReview',
    component: NewReview,
  },
  {
    path: '/community',
    name: 'community',
    component: CommunityMain
  },
  {
    path: '/map',
    name: 'map',
    component: MapPage,
    meta: { hideNavbar: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 👇 인증 가드 추가 (로그인 필수 페이지 보호)
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 보호할 페이지들 (name으로 체크)
  const protectedRoutes = ['mypage', 'editprofile', 'myreview', 'myreview_id', 'newReview']
  
  if (protectedRoutes.includes(to.name)) {
    if (!authStore.isAuthenticated) {
      // 로그인 페이지로 + 원래 페이지 기억
      next({ 
        name: 'login', 
        query: { redirect: to.fullPath } 
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
