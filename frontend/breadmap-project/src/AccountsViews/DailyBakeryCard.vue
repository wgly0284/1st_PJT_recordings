<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { MapPin, ArrowRight, Sparkles } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const recommendation = ref(null)
const isLoading = ref(true)

// 기본 이미지
const defaultImage = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&q=80'

const fetchDailyRecommendation = async () => {
  if (!authStore.token) {
    isLoading.value = false
    return
  }

  try {
    // 백엔드 엔드포인트 (아래 백엔드 코드를 구현해야 동작합니다)
    const res = await apiClient.get('/stores/daily-recommendation/')
    recommendation.value = res.data
  } catch (e) {
    // 404 또는 다른 에러가 발생하면 조용히 실패 (화면에 안 그림)
    if (e.response?.status === 404) {
      console.log('ℹ️ daily-recommendation 엔드포인트가 아직 구현되지 않았습니다.')
    } else {
      console.log('ℹ️ AI 추천 로드 실패:', e.message)
    }
    recommendation.value = null
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchDailyRecommendation()
})
</script>

<template>
  <div v-if="recommendation" class="w-full max-w-[1000px] mx-auto px-6 mb-16 relative z-20 animate-fade-in-up">
    <div class="bg-white rounded-[2.5rem] shadow-xl overflow-hidden border-4 border-[#F3B37A]/20 flex flex-col md:flex-row relative group hover:border-[#F3B37A]/50 transition-colors duration-500">
      
      <!-- AI Badge -->
      <div class="absolute top-0 left-0 bg-gradient-to-r from-[#F3B37A] to-[#FF8A65] text-white px-6 py-2 rounded-br-2xl font-jua z-20 shadow-md flex items-center gap-2">
        <Sparkles class="w-4 h-4 animate-pulse" />
        <span>오늘의 AI 추천</span>
      </div>

      <!-- Image Section -->
      <div class="md:w-5/12 h-64 md:h-auto relative overflow-hidden">
        <img 
          :src="recommendation.image || defaultImage" 
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
          alt="bakery"
        >
        <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent md:bg-gradient-to-r"></div>
      </div>

      <!-- Content Section -->
      <div class="md:w-7/12 p-8 md:p-10 flex flex-col justify-center relative bg-[url('https://www.transparenttextures.com/patterns/cream-paper.png')]">
        
        <div class="mb-6">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-[#FF8A65] font-bold text-xs tracking-widest uppercase bg-[#FFCCBC]/20 px-2 py-1 rounded">
              {{ recommendation.reason || '취향 저격' }}
            </span>
            <span class="text-gray-400 text-xs">|</span>
            <span class="text-gray-500 text-xs font-medium flex items-center gap-1">
              <MapPin class="w-3 h-3" /> {{ recommendation.address }}
            </span>
          </div>
          
          <h3 class="text-3xl md:text-4xl font-jua text-[#5D4037] mb-3 leading-tight">
            {{ recommendation.name }}
          </h3>
          
          <div class="flex flex-wrap gap-2 mt-3">
            <span v-for="tag in recommendation.matched_keywords" :key="tag" 
                  class="px-3 py-1 bg-[#FFF3E0] text-[#EF6C00] rounded-full text-xs font-bold border border-[#FFE0B2]">
              #{{ tag }}
            </span>
            <span v-for="tag in (recommendation.tags || []).slice(0, 3)" :key="tag"
                  class="px-3 py-1 bg-gray-100 text-gray-500 rounded-full text-xs">
              #{{ tag }}
            </span>
          </div>
        </div>

        <p class="text-[#8D6E63] text-sm leading-relaxed mb-8 line-clamp-2 font-medium">
          {{ recommendation.description || '회원님의 빵 취향을 분석하여 AI가 선정한 오늘의 추천 빵집입니다. 따뜻한 빵 냄새와 함께 행복한 하루 보내세요!' }}
        </p>

        <button
          @click="router.push({ name: 'detail', params: { id: recommendation.id } })"
          class="self-start px-8 py-3 bg-[#5D4037] text-white rounded-2xl font-bold hover:bg-[#4E342E] transition-all shadow-lg hover:shadow-xl hover:-translate-y-1 flex items-center gap-2 group/btn"
        >
          <span>보러 가기</span>
          <ArrowRight class="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
.font-jua { font-family: 'Jua', sans-serif; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}
</style>