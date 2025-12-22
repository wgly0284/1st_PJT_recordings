<template>
  <main class="flex-grow">
    <!-- Hero Section -->
    <section class="relative min-h-screen flex items-center pt-20 overflow-hidden">
      <!-- 기존 HTML의 Hero 부분 그대로 -->
      <div class="absolute top-0 right-0 w-[60%] h-full bg-[#F0EBE0] -z-10 rounded-l-[100px] hidden md:block"></div>
      <div class="max-w-[1400px] mx-auto px-6 md:px-12 w-full flex flex-col md:flex-row items-center gap-16">
        <!-- Text Content -->
        <div class="md:w-1/2 space-y-10 relative z-10">
          <div class="inline-block border-b border-teal-800 pb-1">
            <span class="text-teal-800 font-bold tracking-widest text-xs uppercase">Premium Bakery Curator</span>
          </div>
          <h1 class="text-6xl md:text-8xl font-playfair font-bold text-teal-900 leading-[0.9]">
            Taste <br>
            <span class="italic text-orange-600 block pl-20">The Moment.</span>
          </h1>
          <p class="text-xl text-gray-500 leading-relaxed max-w-lg font-light">
            단순히 빵을 먹는 것을 넘어, 공간과 맛이 주는 특별한 경험을 찾아 떠납니다. 
            <br><strong class="text-teal-900 font-medium">당신의 취향을 발견하는 여정</strong>을 시작하세요.
          </p>
          <div class="flex flex-col sm:flex-row gap-5 pt-4">
            <button class="group px-8 py-4 bg-teal-900 text-white text-lg rounded-full font-bold transition-all hover:bg-teal-800 hover:scale-105 shadow-xl flex items-center justify-center gap-3">
              <span>Explore Map</span>
              <div class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center group-hover:bg-white/30 transition-colors">
                <ArrowRight class="w-4 h-4" />
              </div>
            </button>
            <button class="px-8 py-4 bg-transparent border-2 border-teal-900/10 text-teal-900 text-lg rounded-full font-bold hover:bg-teal-900 hover:text-white transition-all hover:border-teal-900">
              AI Recommendation
            </button>
          </div>
        </div>
        <!-- Hero Image -->
        <div class="md:w-1/2 relative w-full h-[50vh] md:h-[70vh] z-0">
          <div class="absolute inset-0 rounded-[3rem] overflow-hidden shadow-2xl">
            <img
              src="https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1200&auto=format&fit=crop"
              class="w-full h-full object-cover"
            >
            <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
            <div class="absolute bottom-8 left-8 right-8 bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-3xl text-white">
              <div class="flex justify-between items-end">
                <div>
                  <p class="text-xs font-bold uppercase tracking-widest mb-1 opacity-80">Today's Pick</p>
                  <p class="text-2xl font-playfair font-bold">Onion Bagel, Seongsu</p>
                </div>
                <div class="w-12 h-12 rounded-full border border-white/30 flex items-center justify-center">
                  <ArrowUpRight class="w-5 h-5" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-teal-900/50 animate-bounce">
        <span class="text-[10px] font-bold tracking-widest uppercase">Scroll</span>
        <ArrowDown class="w-4 h-4" />
      </div>
    </section>

    <!-- Curation Section -->
    <section class="py-32 bg-white relative">
      <div class="max-w-[1400px] mx-auto px-6 md:px-12">
        <div class="flex flex-col md:flex-row justify-between items-end mb-20 gap-8 reveal-hidden">
          <div>
            <h2 class="text-4xl md:text-5xl font-playfair font-bold text-teal-900 leading-tight mb-4">
              Weekly <br>
              <span class="italic text-orange-600">Curations</span>
            </h2>
            <p class="text-gray-500 max-w-md">한 주간 가장 사랑받은 베이커리를 엄선하여 소개합니다. 트렌디한 맛의 흐름을 놓치지 마세요.</p>
          </div>
          <a href="#" class="group flex items-center gap-2 text-teal-900 font-bold border-b border-teal-900 pb-1 hover:opacity-70 transition-opacity">
            VIEW ALL <i data-lucide="arrow-right" class="w-4 h-4 group-hover:translate-x-1 transition-transform"></i>
          </a>
        </div>
        <BakeryGrid :bakeries="bakeries" @open-detail="openDetail" />
      </div>
      <div class="h-24 hidden lg:block"></div>
    </section>

    <!-- Featured Section -->
    <section class="py-32 bg-teal-900 text-white relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-full opacity-5">
        <div class="absolute w-[500px] h-[500px] bg-white rounded-full blur-[100px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>
      </div>
      <div class="max-w-[1400px] mx-auto px-6 md:px-12 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-20 reveal-hidden delay-300">
          <div class="md:w-1/2 w-full">
            <div class="relative group">
              <div class="absolute -inset-4 bg-orange-500/20 rounded-[2.5rem] blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
              <img src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=1200&auto=format&fit=crop" class="relative rounded-[2rem] shadow-2xl w-full transform group-hover:scale-[1.02] transition-transform duration-700">
              <div class="absolute -right-8 top-1/2 -translate-y-1/2 bg-white text-teal-900 p-6 rounded-2xl shadow-xl hidden md:block animate-float" style="animation-delay: 1s;">
                <p class="text-xs font-bold uppercase tracking-widest mb-2 text-gray-400">Total Reviews</p>
                <p class="text-4xl font-bold font-playfair">12.5k+</p>
              </div>
            </div>
          </div>
          <div class="md:w-1/2 w-full space-y-8">
            <h2 class="text-5xl md:text-7xl font-playfair font-bold leading-tight">
              Master <br>
              <span class="text-orange-400 italic">The Taste.</span>
            </h2>
            <p class="text-teal-100/80 text-xl leading-relaxed max-w-md font-light">
              당신의 빵지순례 기록이 쌓일수록,<br>더 특별한 혜택과 히든 스팟이 공개됩니다.
            </p>
            <div class="bg-white/5 backdrop-blur-md border border-white/10 p-8 rounded-3xl">
              <div class="flex justify-between items-end mb-4">
                <div>
                  <p class="text-sm text-teal-300 font-bold mb-1">CURRENT LEVEL</p>
                  <p class="text-2xl font-bold">Lv.3 빵수집가</p>
                </div>
                <span class="text-4xl font-bold text-white/20">70%</span>
              </div>
              <div class="w-full bg-black/20 rounded-full h-1.5 overflow-hidden">
                <div class="bg-gradient-to-r from-orange-400 to-orange-600 h-full rounded-full w-[70%]"></div>
              </div>
            </div>
            <button class="px-8 py-4 bg-white text-teal-900 rounded-full font-bold hover:bg-orange-50 transition-colors w-full md:w-auto">
              내 등급 확인하기
            </button>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BakeryGrid from '@/components/common/BakeryGrid.vue'
import { ArrowRight, ArrowDown, ArrowUpRight } from 'lucide-vue-next'

const router = useRouter()

const bakeries = ref([
  {
    id: 1,
    bakeryName: "Butter House",
    name: "Classic Salt Bread",
    location: "Busan, Jeonpo",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&q=80&w=800",
    tags: ["Butter", "Crispy"],
    menu: [{ name: "Salt Bread", price: "3.5", img: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=200" }]
  },
  {
    id: 2,
    bakeryName: "Monsieur Croissant",
    name: "Matcha Croissant",
    location: "Seoul, Seongsu",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1530610476181-d8ceb28bc272?auto=format&fit=crop&q=80&w=800",
    tags: ["French", "Pastry"],
    menu: [{ name: "Matcha Croissant", price: "5.2", img: "https://images.unsplash.com/photo-1530610476181-d8ceb28bc272?q=80&w=200" }]
  },
  {
    id: 3,
    bakeryName: "Sunday Bagel",
    name: "Blueberry Sand",
    location: "Seoul, Yeonnam",
    rating: 4.5,
    image: "https://images.unsplash.com/photo-1620916297397-a4a5402a3c6c?auto=format&fit=crop&q=80&w=800",
    tags: ["NYC", "Bagel"],
    menu: []
  },
  {
    id: 4,
    bakeryName: "Wheat & Grain",
    name: "Sourdough",
    location: "Jeju, Aewol",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=800",
    tags: ["Vegan", "Healthy"],
    menu: []
  }
])

const openDetail = (bakery) => {
  router.push(`/detail/${bakery.id}`)
}
</script>
