<template>
  <div class="bg-white min-h-screen pt-20">
    <div class="max-w-[1200px] mx-auto px-6 py-20">
      <button @click="$router.push('/')" class="mb-10 flex items-center gap-2 text-gray-500 hover:text-teal-800 transition-colors font-medium group">
        <div class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center group-hover:bg-teal-800 group-hover:text-white group-hover:border-teal-800 transition-all">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
        </div>
        <span>Back to List</span>
      </button>

      <div class="grid lg:grid-cols-2 gap-16 items-start">
        <!-- Image Gallery (Sticky) -->
        <div class="lg:sticky lg:top-24 space-y-6">
          <div class="aspect-[4/3] rounded-[2rem] overflow-hidden shadow-2xl">
            <img :src="selectedBakery.image" class="w-full h-full object-cover">
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div class="aspect-square rounded-2xl overflow-hidden" v-for="i in 3" :key="i">
              <img :src="`https://source.unsplash.com/random/200x200/?pastry,${i}`" class="w-full h-full object-cover hover:opacity-80 transition-opacity cursor-pointer">
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="pt-4">
          <span class="text-orange-600 font-bold tracking-wider text-sm uppercase mb-3 block">Premium Bakery</span>
          <h2 class="text-5xl md:text-6xl font-playfair font-bold text-teal-900 mb-6 leading-tight">{{ selectedBakery.bakeryName }}</h2>
          
          <div class="flex flex-wrap gap-4 mb-10 text-sm">
            <span class="px-4 py-2 border border-gray-200 rounded-full text-gray-600 flex items-center gap-2">
              <i data-lucide="map-pin" class="w-4 h-4"></i> {{ selectedBakery.location }}
            </span>
            <span class="px-4 py-2 border border-gray-200 rounded-full text-gray-600 flex items-center gap-2">
              <i data-lucide="star" class="w-4 h-4 text-orange-500 fill-current"></i> {{ selectedBakery.rating }}
            </span>
          </div>

          <p class="text-xl text-gray-600 leading-relaxed mb-12 font-light">
            프랑스산 유기농 밀가루와 AOP 버터를 사용하여 매일 아침 구워냅니다. 
            겉은 바삭하고 속은 촉촉한 식감의 조화를 느껴보세요.
          </p>

          <!-- AI Summary -->
          <div class="bg-[#F9F7F2] rounded-[2rem] p-10 relative mb-12 overflow-hidden group">
            <div class="absolute top-0 right-0 p-10 opacity-10 group-hover:opacity-20 transition-opacity duration-700">
              <i data-lucide="quote" class="w-32 h-32 text-teal-900"></i>
            </div>
            
            <div class="relative z-10">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-8 h-8 rounded-full bg-teal-800 flex items-center justify-center text-white">
                  <i data-lucide="sparkles" class="w-4 h-4"></i>
                </div>
                <h3 class="font-bold text-teal-900 text-lg">AI Review Summary</h3>
              </div>
              
              <div v-if="!aiSummary">
                <button @click="generateAISummary" class="w-full py-5 bg-white border-2 border-dashed border-teal-800/20 rounded-2xl text-teal-800 font-bold hover:bg-teal-50 hover:border-teal-800/40 transition-all flex items-center justify-center gap-2">
                  <span>분석 리포트 생성하기</span>
                  <i data-lucide="loader" class="w-4 h-4 animate-spin hidden"></i>
                </button>
              </div>
              <div v-else>
                <p class="text-lg text-teal-900 font-medium leading-relaxed mb-6">"{{ aiSummary.text }}"</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="tag in aiSummary.keywords" :key="tag" class="px-4 py-2 bg-white rounded-full text-sm text-teal-800 font-bold shadow-sm">#{{ tag }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Menu -->
          <div>
            <h3 class="font-bold text-teal-900 mb-6 text-xl">Signature Menu</h3>
            <div class="space-y-4">
              <div v-for="menu in selectedBakery.menu" :key="menu.name" class="flex justify-between items-center p-6 rounded-2xl border border-gray-100 hover:border-teal-800/20 hover:shadow-lg transition-all cursor-pointer bg-white group">
                <div class="flex items-center gap-6">
                  <div class="w-20 h-20 rounded-xl bg-gray-100 overflow-hidden">
                    <img :src="menu.img" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
                  </div>
                  <div>
                    <h4 class="text-lg font-bold text-gray-900 mb-1">{{ menu.name }}</h4>
                    <p class="text-sm text-gray-400">Limited Daily Quantity</p>
                  </div>
                </div>
                <span class="text-lg font-bold text-teal-800">{{ menu.price }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const aiSummary = ref(null)

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

const selectedBakery = computed(() => {
  return bakeries.value.find(b => b.id == route.params.id) || bakeries.value[0]
})

const generateAISummary = () => {
  setTimeout(() => {
    aiSummary.value = {
      text: "겉은 바삭하고 속은 촉촉한 완벽한 밸런스. 한 입 베어 물면 퍼지는 진한 버터 향이 일품입니다. 주말에는 웨이팅이 있으니 오픈런을 추천합니다.",
      keywords: ["겉바속촉", "버터풍미", "오픈런필수"]
    }
  }, 800)
}

onMounted(() => {
  lucide.createIcons()
})
</script>
