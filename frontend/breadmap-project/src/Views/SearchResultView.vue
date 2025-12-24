<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] pb-20 pt-10">
    
    <!-- 검색 헤더 영역 -->
    <div class="max-w-4xl mx-auto px-6 mb-10">
      <div class="text-center mb-8">
        <div class="inline-flex items-center gap-2 bg-[#FFF3DD] border-2 border-[#FFE8CC] px-4 py-2 rounded-full shadow-sm mb-4">
          <span class="text-xl">🔍</span>
          <span class="text-[#C99768] font-jua">빵집 찾기</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-jua text-[#6B4A38] leading-tight">
          어떤 빵집을 찾으시나요?
        </h1>
      </div>

      <!-- 검색바 -->
      <div class="relative max-w-2xl mx-auto">
        <input
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="text"
          placeholder="빵집 이름, 메뉴, 지역을 검색해보세요 🥐"
          class="w-full py-5 px-8 pr-16 rounded-full bg-white/80 backdrop-blur-sm border-4 border-[#FFE8CC] text-[#6B4A38] placeholder-[#C99768]/70 font-jua text-xl focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all shadow-lg focus:shadow-[0_8px_20px_rgba(201,151,104,0.15)]"
        />
        <button
          @click="handleSearch"
          class="absolute right-3 top-1/2 -translate-y-1/2 w-12 h-12 bg-gradient-to-br from-[#F3B37A] to-[#EF6C00] rounded-full flex items-center justify-center hover:scale-105 active:scale-95 transition-all shadow-md group"
        >
          <Search class="w-6 h-6 text-white group-hover:rotate-12 transition-transform" />
        </button>
      </div>
      
      <p v-if="keyword" class="text-center mt-6 font-jua text-lg text-[#8B6A55]">
        "<span class="text-[#EF6C00]">{{ keyword }}</span>" 검색 결과가 
        <span class="bg-[#FFF3DD] px-2 py-0.5 rounded-lg border border-[#FFE8CC]">{{ bakeries.length }}</span>건 있어요!
      </p>
    </div>

    <!-- 검색 결과 리스트 -->
    <div class="max-w-7xl mx-auto px-6">
      <!-- 로딩 중 -->
      <div v-if="isLoading" class="text-center py-20 flex flex-col items-center gap-6">
        <img :src="loadingImage" alt="식빵쥐" class="w-32 h-32 object-contain animate-bounce" />
        <p class="text-[#C99768] font-jua text-2xl">열심히 빵을 굽고 있어요! 조금만 기다려주세요!</p>
      </div>

      <!-- 결과 있음 -->
      <div v-else-if="bakeries.length > 0">
        <!-- 그리드: 한 줄에 4개 (lg 이상) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="bakery in paginatedBakeries"
            :key="bakery.id"
            @click="goToBakery(bakery.id)"
            class="group bg-white rounded-[2rem] overflow-hidden border-4 border-transparent hover:border-[#FFE8CC] shadow-lg hover:shadow-[0_12px_24px_rgba(201,151,104,0.15)] hover:-translate-y-2 transition-all duration-300 cursor-pointer"
          >
            <!-- 이미지 영역 -->
            <div class="relative h-48 overflow-hidden">
              <div class="absolute inset-0 bg-gray-100 flex items-center justify-center text-[#FFE8CC]">
                 <!-- 이미지 로딩 전 배경 -->
                 <span class="text-4xl">🍞</span>
              </div>
              <img
                :src="bakery.image || 'https://source.unsplash.com/random/400x300/?bakery,bread'"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 relative z-10"
                @error="handleImageError"
              />
              <!-- 평점 뱃지 -->
              <div class="absolute top-3 right-3 z-20 bg-white/95 backdrop-blur px-2.5 py-1 rounded-full flex items-center gap-1 shadow-md border-2 border-[#FFE8CC]">
                <Star class="w-3.5 h-3.5 fill-orange-400 text-orange-400" />
                <span class="text-xs font-jua text-[#6B4A38] pt-0.5">{{ bakery.avg_rating || '0.0' }}</span>
              </div>
              <!-- 그라데이션 오버레이 -->
              <div class="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent pointer-events-none z-10"></div>
            </div>

            <!-- 텍스트 내용 -->
            <div class="p-5 bg-white relative z-20">
              <h3 class="text-xl font-jua text-[#6B4A38] mb-1 group-hover:text-[#EF6C00] transition-colors truncate">
                {{ bakery.name }}
              </h3>
              <p class="text-[#8B6A55] mb-3 flex items-start gap-1.5 font-jua text-sm min-h-[2.5em]">
                <MapPin class="w-3.5 h-3.5 text-[#C99768] shrink-0 mt-0.5" />
                <span class="line-clamp-2 text-xs">{{ bakery.address }}</span>
              </p>
              
              <!-- 태그 -->
              <div v-if="bakery.representative_tags" class="flex flex-wrap gap-1.5">
                <span
                  v-for="tag in String(bakery.representative_tags).split(',').slice(0, 2)"
                  :key="tag"
                  class="text-xs px-2.5 py-1 bg-[#FFF3DD] text-[#C99768] rounded-full border border-[#FFE8CC] font-jua"
                >
                  #{{ tag.trim() }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 페이지네이션 컨트롤 -->
        <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-12">
          <!-- 이전 버튼 -->
          <button 
            @click="changePage(currentPage - 1)" 
            :disabled="currentPage === 1"
            class="w-10 h-10 rounded-full flex items-center justify-center bg-white border-2 border-[#FFE8CC] text-[#C99768] disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#FFF3DD] transition-colors font-jua"
          >
            &lt;
          </button>

          <!-- 페이지 번호 (5개씩 끊어서 표시) -->
          <button 
            v-for="page in displayedPages" 
            :key="page"
            @click="changePage(page)"
            :class="[
              'w-10 h-10 rounded-full font-jua transition-all border-2 flex items-center justify-center pt-1',
              currentPage === page 
                ? 'bg-[#EF6C00] border-[#EF6C00] text-white shadow-lg transform scale-110' 
                : 'bg-white border-[#FFE8CC] text-[#C99768] hover:bg-[#FFF3DD]'
            ]"
          >
            {{ page }}
          </button>

          <!-- 다음 버튼 -->
          <button 
            @click="changePage(currentPage + 1)" 
            :disabled="currentPage === totalPages"
            class="w-10 h-10 rounded-full flex items-center justify-center bg-white border-2 border-[#FFE8CC] text-[#C99768] disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#FFF3DD] transition-colors font-jua"
          >
            &gt;
          </button>
        </div>
      </div>

      <!-- 결과 없음 -->
      <div v-else class="text-center py-20 bg-white/50 rounded-[3rem] border-4 border-dashed border-[#FFE8CC] backdrop-blur-sm max-w-4xl mx-auto">
        <div class="text-7xl mb-6">🥐</div>
        <h2 class="text-3xl font-jua text-[#6B4A38] mb-3">검색 결과가 없어요</h2>
        <p class="text-[#C99768] font-jua text-lg mb-8">다른 키워드로 다시 검색해보시겠어요?</p>
        <button
          @click="$router.push('/')"
          class="px-8 py-4 bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] text-white rounded-2xl font-jua text-xl hover:shadow-lg hover:-translate-y-1 transition-all flex items-center justify-center gap-2 mx-auto"
        >
          홈으로 돌아가기 🏠
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Star, MapPin } from 'lucide-vue-next'
import axios from 'axios'
import loadingImage from '@/assets/images/식빵쥐.png'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const keyword = ref('')
const bakeries = ref([])
const isLoading = ref(false)

// 페이지네이션 상태
const currentPage = ref(1)
const itemsPerPage = 12 // 4개 * 3줄 = 12개
const pageGroupSize = 5 // 한 번에 보여줄 페이지 번호 개수 (1~5, 6~10)

const handleImageError = (e) => {
  e.target.src = 'https://source.unsplash.com/random/400x300/?bread,dessert'
}

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return

  keyword.value = searchQuery.value
  isLoading.value = true

  try {
    const response = await axios.get('http://127.0.0.1:8000/stores/', {
      params: { search: searchQuery.value }
    })
    bakeries.value = response.data
    currentPage.value = 1 // 검색 시 1페이지로 리셋
  } catch (error) {
    console.error('검색 실패:', error)
  } finally {
    isLoading.value = false
  }
}

// [중요] 상세 페이지로 이동하는 함수
const goToBakery = (id) => {
  if (!id) {
    console.error("유효하지 않은 빵집 ID입니다.")
    return
  }
  // router/index.js에서 설정된 'detail' 라우트로 이동 (path: '/detail/:id')
  router.push({ name: 'detail', params: { id } })
}

// Computed Properties for Pagination
const totalPages = computed(() => Math.ceil(bakeries.value.length / itemsPerPage))

const paginatedBakeries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return bakeries.value.slice(start, end)
})

// 페이지 번호 5개씩 끊어서 표시
const displayedPages = computed(() => {
  const currentGroup = Math.ceil(currentPage.value / pageGroupSize)
  
  const startPage = (currentGroup - 1) * pageGroupSize + 1
  const endPage = Math.min(currentGroup * pageGroupSize, totalPages.value)
  
  const pages = []
  for (let i = startPage; i <= endPage; i++) {
    pages.push(i)
  }
  return pages
})

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
    handleSearch()
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}
</style>