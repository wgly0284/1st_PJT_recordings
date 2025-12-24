<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios' // 실제 API 사용 시 주석 해제
import { useAuthStore } from '@/stores/auth' // 실제 Auth 사용 시 주석 해제
import { MapPin, ArrowRight, Sparkles } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore() // 실제 사용 시 주석 해제
const recommendation = ref(null)
const isLoading = ref(true)

// 1. 비로그인(게스트)용 샘플 데이터
const guestSampleData = {
  id: 1,
  name: 'Breadtopia 본점',
  address: '부산진구 전포대로 123번길',
  image: 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=800',
  reason: '이달의 인기',
  matched_keywords: ['소금빵', '분위기좋은'],
  tags: ['데이트', '커피맛집'],
  description: '아직 로그인을 하지 않으셨군요! 회원가입 하시면 취향에 딱 맞는 빵집을 매일 아침 AI가 추천해드려요. 지금은 가장 인기 있는 곳을 보여드릴게요.'
}

// 2. 로그인 사용자용 샘플 데이터 (API 실패 시에만 보여줄 백업 데이터)
// ⚠️ 이 데이터는 API가 정상 작동하면 표시되지 않습니다.
const userSampleData = {
  id: 1,
  name: '달콤한 오후 (API 연결 실패)',
  address: '부산 수영구 광안해변로 22',
  image: 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&q=80',
  reason: '취향 저격',
  matched_keywords: ['크루아상', '조용한'],
  tags: ['작업하기좋은', '디저트'],
  description: '서버 연결에 실패하여 샘플 데이터를 보여드리고 있습니다. API가 정상 작동하면 회원가입 시 입력한 취향 기반 추천을 받을 수 있습니다.'
}

const fetchDailyRecommendation = async () => {
  // 1. 토큰 체크: 로그인을 안 했으면 게스트 데이터 보여줌
  if (!authStore.token) {
    console.log('ℹ️ 비로그인 상태: 게스트 샘플 데이터 표시')
    recommendation.value = guestSampleData
    isLoading.value = false
    return
  }

  // 2. 로그인 상태: 실제 API 호출하여 사용자 취향 기반 추천 받기
  try {
    console.log('🔄 회원가입 시 입력한 취향 기반으로 빵집 추천 요청 중...')
    const res = await apiClient.get('/stores/daily-recommendation/')
    console.log('✅ AI 추천 성공:', res.data)
    recommendation.value = res.data
  } catch (e) {
    // API 호출 실패 시 백업 샘플 데이터 표시
    console.error('🔥 API 호출 실패:', e.message)
    console.log('ℹ️ 백업 샘플 데이터를 표시합니다.')

    recommendation.value = userSampleData
  } finally {
    isLoading.value = false
  }
}

// 상세 페이지 이동 함수
const goToDetail = () => {
  if (recommendation.value && recommendation.value.id) {
    // 404 에러 방지를 위해, ID가 유효한지 확인하고 이동합니다.
    console.log(`이동 시도: ID ${recommendation.value.id}번 빵집 상세 페이지`)
    router.push({ 
      name: 'detail', 
      params: { id: recommendation.value.id } 
    })
  } else {
    console.warn('이동할 빵집 ID가 없습니다.')
  }
}

onMounted(() => {
  fetchDailyRecommendation()
})
</script>

<template>
  <!-- 로딩 상태일 때 표시할 스켈레톤 혹은 빈 공간 -->
  <div v-if="isLoading" class="w-full max-w-[1000px] mx-auto px-6 mb-16 h-[300px] bg-gray-100 rounded-[2.5rem] animate-pulse"></div>

  <!-- 데이터가 있을 때 표시 -->
  <div v-else-if="recommendation" class="w-full max-w-[1000px] mx-auto px-6 mb-16 relative z-20 animate-fade-in-up">
    <div class="bg-white rounded-[2.5rem] shadow-xl overflow-hidden border-4 border-[#F3B37A]/20 flex flex-col md:flex-row relative group hover:border-[#F3B37A]/50 transition-colors duration-500">
      
      <!-- AI Badge -->
      <div class="absolute top-0 left-0 bg-gradient-to-r from-[#F3B37A] to-[#FF8A65] text-white px-6 py-2 rounded-br-2xl font-jua z-20 shadow-md flex items-center gap-2">
        <Sparkles class="w-4 h-4 animate-pulse" />
        <span>{{ recommendation.reason === '이달의 인기' ? 'Guest 추천' : '오늘의 AI 추천' }}</span>
      </div>

      <!-- Image Section -->
      <div class="md:w-5/12 h-64 md:h-auto relative overflow-hidden bg-gradient-to-br from-amber-50 to-orange-50">
        <!-- 이미지가 있을 때 -->
        <img
          v-if="recommendation.image"
          :src="recommendation.image"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 cursor-pointer"
          alt="bakery"
          @click="goToDetail"
          @error="e => e.target.style.display = 'none'"
        >

        <!-- 이미지가 없을 때 -->
        <div v-else class="w-full h-full flex flex-col items-center justify-center p-8 text-center cursor-pointer" @click="goToDetail">
          <img
            src="@/assets/images/logo.png"
            alt="기본 로고"
            class="w-24 h-24 object-contain opacity-30 mb-4"
          />
          <p class="text-sm font-bold text-gray-400 mb-2">이미지가 등록되지 않았어요</p>
          <p class="text-xs text-gray-400">제보하기를 통해 이미지를 등록해주세요 📸</p>
        </div>

        <div v-if="recommendation.image" class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent md:bg-gradient-to-r pointer-events-none"></div>
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
          
          <!-- 제목 클릭 시에도 이동하도록 커서 및 이벤트 추가 -->
          <h3 
            class="text-3xl md:text-4xl font-jua text-[#5D4037] mb-3 leading-tight cursor-pointer hover:text-[#F3B37A] transition-colors"
            @click="goToDetail"
          >
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
          {{ recommendation.description }}
        </p>

        <button
          @click="goToDetail"
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