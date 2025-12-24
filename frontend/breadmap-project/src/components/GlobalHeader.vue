<template>
  <header :class="{'bg-[#F9F7F2]/90 backdrop-blur-md py-4 shadow-sm': isScrolled, 'bg-transparent py-6': !isScrolled}"
          class="fixed top-0 w-full z-50 transition-all duration-500">
    <div class="max-w-[1400px] mx-auto px-6 md:px-12 flex justify-between items-center">
      <!-- Logo -->
      <div @click="goHome" class="flex items-center gap-2 cursor-pointer group">
        <!--
             [변경됨] 기존 이모지 대신 이미지를 사용합니다.
             이미지 크기는 class의 w-10 h-10 등으로 조절하세요.
        -->
        <img
          :src="logoImage"
          alt="Breadtopia Logo"
          class="w-10 h-10 object-contain transition-transform duration-500 group-hover:rotate-12"
        />

        <span class="font-jua text-2xl md:text-3xl font-bold tracking-tight text-[#6B4A38] group-hover:text-[#C99768] transition-colors">
          Breadtopia
        </span>
      </div>

      <!-- Nav Links & Auth (Desktop) -->
      <nav class="hidden md:flex items-center gap-8 text-sm font-bold tracking-wide">
        <router-link
          :to="{ name: 'community' }"
          class="text-[#6B4A38] hover:text-[#F3B37A] transition-colors relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-[#F3B37A] after:transition-all hover:after:w-full font-jua text-base"
        >
          COMMUNITY
        </router-link>
        <router-link
          :to="{ name: 'map' }"
          class="text-[#6B4A38] hover:text-[#F3B37A] transition-colors relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-[#F3B37A] after:transition-all hover:after:w-full font-jua text-base"
        >
          MAPS
        </router-link>

        <!-- Conditional Auth Links -->
        <template v-if="authStore.isAuthenticated">
          <router-link
            to="/mypage"
            class="text-[#6B4A38] hover:text-[#F3B37A] transition-colors relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-[#F3B37A] after:transition-all hover:after:w-full font-jua text-base"
          >
            MY PAGE
          </router-link>
          <button
            @click="handleLogout"
            class="px-6 py-3 bg-[#F3B37A] text-white text-xs font-bold rounded-full hover:bg-[#C99768] transition-all duration-300 shadow-md font-jua"
          >
            LOGOUT
          </button>
        </template>
        <template v-else>
          <router-link
            to="/login"
            class="text-[#6B4A38] hover:text-[#F3B37A] transition-colors relative after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-0 after:h-0.5 after:bg-[#F3B37A] after:transition-all hover:after:w-full font-jua text-base"
          >
            LOGIN
          </router-link>
          <router-link
            to="/signup"
            class="px-6 py-3 bg-[#F3B37A] text-white text-xs font-bold rounded-full hover:bg-[#C99768] transition-all duration-300 shadow-md font-jua"
          >
            SIGN UP
          </router-link>
        </template>
      </nav>

      <!-- Mobile Menu Button -->
      <button class="md:hidden text-[#6B4A38]">
        <i data-lucide="menu" class="w-8 h-8"></i>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute, RouterLink } from 'vue-router'

// [중요] assets 폴더에 있는 로고 이미지를 import 합니다.
// 실제 파일명(예: logo.png)에 맞게 경로를 수정해주세요.
import logoImage from '@/assets/images/logo.png'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const handleLogout = () => {
  authStore.logout()
}

const goHome = () => {
  // 현재 페이지가 홈이면 강제 새로고침
  if (route.path === '/' || route.name === 'home') {
    window.location.href = '/'
  } else {
    // 다른 페이지에서는 일반 라우팅
    router.push('/')
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}
</style>