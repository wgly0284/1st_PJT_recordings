<template>
  <header :class="{'bg-[#F9F7F2]/90 backdrop-blur-md py-4 shadow-sm': isScrolled, 'bg-transparent py-6': !isScrolled}" 
          class="fixed top-0 w-full z-50 transition-all duration-500">
    <div class="max-w-[1400px] mx-auto px-6 md:px-12 flex justify-between items-center">
<!-- Logo -->
           <router-link to="/" class="flex items-center
      gap-2 cursor-pointer group">
             <div class="w-10 h-10 rounded-full bg-teal-
      800 flex items-center justify-center text-white
      transition-transform duration-500
      group-hover:rotate-12">
               <span class="text-base">🥖</span>
             </div>
            <span class="font-playfair text-xl md:text
      -2xl font-bold tracking-tight text-teal-900
      group-hover:opacity-80 transition-opacity">Bread
      Pilgrimage</span>
          </router-link>
   
          <!-- Nav Links & Auth (Desktop) -->
          <nav class="hidden md:flex items-center gap-8
      text-sm font-bold tracking-wide text-gray-600">
            <router-link :to="{ name: 'community' }" class="hover:text-teal-800
      transition-colors relative after:content-[''] after
      :absolute after:-bottom-2 after:left-0 after:w-0
      after:h-0.5 after:bg-teal-800 after:transition-all
      hover:after:w-full">COMMUNITY</router-link>
            <router-link :to="{ name: 'map' }" class="hover:text-teal-800
      transition-colors relative after:content-[''] after
      :absolute after:-bottom-2 after:left-0 after:w-0
      after:h-0.5 after:bg-teal-800 after:transition-all
      hover:after:w-full">MAPS</router-link>
   
            <!-- Conditional Auth Links -->
            <template v-if="authStore.isAuthenticated">
              <router-link to="/mypage" class="hover:
      text-teal-800 transition-colors relative after:
      content-[''] after:absolute after:-bottom-2 after
      :left-0 after:w-0 after:h-0.5 after:bg-teal-800
      after:transition-all hover:after:w-full">MY PAGE</
      router-link>
              <button @click="handleLogout" class="px-6
      py-3 bg-teal-900 text-white text-xs font-bold
      rounded-full hover:bg-teal-800 transition-all
      duration-300">
                LOGOUT
              </button>
            </template>
            <template v-else>
              <router-link to="/login" class="hover:
      text-teal-800 transition-colors relative after:
      content-[''] after:absolute after:-bottom-2 after
      :left-0 after:w-0 after:h-0.5 after:bg-teal-800
      after:transition-all hover:after:w-full">LOGIN</
      router-link>
              <router-link to="/signup" class="px-6 py-
      3 bg-teal-900 text-white text-xs font-bold
      rounded-full hover:bg-teal-800 transition-all
      duration-300">
                SIGN UP
              </router-link>
            </template>
          </nav>
   
          <!-- Mobile Menu Button -->
          <button class="md:hidden text-teal-900">
            <i data-lucide="menu" class="w-8 h-8"></i>
          </button>
        </div>
      </header>
    </template>
   
    <script setup>
    import { ref, onMounted, onUnmounted } from 'vue'
    import { useAuthStore } from '@/stores/auth'
    import { RouterLink } from 'vue-router'
   
    const authStore = useAuthStore()
    const isScrolled = ref(false)
   
    const handleScroll = () => {
      isScrolled.value = window.scrollY > 50
    }
   
    const handleLogout = () => {
      authStore.logout()
    }
   
    onMounted(() => {
      window.addEventListener('scroll', handleScroll)
    })
    onUnmounted(() => {
      window.removeEventListener('scroll',
      handleScroll)
    })
    </script>