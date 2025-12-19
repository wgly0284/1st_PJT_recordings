<template>
  <header :class="{'bg-[#F9F7F2]/90 backdrop-blur-md py-4 shadow-sm': isScrolled, 'bg-transparent py-6': !isScrolled}" 
          class="fixed top-0 w-full z-50 transition-all duration-500">
    <!-- 기존 헤더 HTML 그대로 -->
    <div class="max-w-[1400px] mx-auto px-6 md:px-12 flex justify-between items-center">
      <!-- Logo + Nav + CTA -->
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isScrolled = ref(false)
const currentTab = ref('home')

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  lucide.createIcons()
  window.addEventListener('scroll', handleScroll)
})
</script>
