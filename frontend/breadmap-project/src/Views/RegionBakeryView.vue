<template>
  <!-- pt-32로 상단 여백을 늘려 헤더와 겹치지 않게 수정 -->
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] pb-20 pt-32">
    
    <!-- 헤더 영역 -->
    <div class="max-w-6xl mx-auto px-6 mb-12 text-center">
      <div class="inline-flex items-center gap-2 bg-[#FFF3DD] border-2 border-[#FFE8CC] px-5 py-2 rounded-full shadow-sm mb-6 animate-bounce-slow">
        <span class="text-2xl">{{ regionIcon }}</span>
        <span class="text-[#C99768] font-jua text-lg">{{ regionName }} 빵지순례</span>
      </div>
      <h1 class="text-4xl md:text-5xl font-jua text-[#6B4A38] leading-tight mb-4">
        {{ regionName }}의 숨은 빵집들 🏠
      </h1>
      <p class="text-[#8B6A55] font-jua text-lg">
        이 지역에서 사랑받는 <span class="text-[#EF6C00] font-bold">{{ bakeries.length }}곳</span>의 빵집을 발견했어요!
      </p>
    </div>

    <!-- 빵집 목록 컨테이너 -->
    <div class="max-w-7xl mx-auto px-6">
      
      <!-- 로딩 중 -->
      <div v-if="isLoading" class="text-center py-20 flex flex-col items-center gap-4">
        <div class="text-6xl animate-bounce">🥖</div>
        <p class="text-[#C99768] font-jua text-2xl">갓 구운 빵집 정보를 가져오는 중...</p>
      </div>

      <!-- 빵집 카드 그리드 -->
      <div v-else-if="bakeries.length > 0">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          <div
            v-for="bakery in paginatedBakeries"
            :key="bakery.id"
            @click="goToBakery(bakery.id)"
            class="group bg-white rounded-[2rem] overflow-hidden border-4 border-transparent hover:border-[#FFE8CC] shadow-lg hover:shadow-[0_12px_24px_rgba(201,151,104,0.15)] hover:-translate-y-2 transition-all duration-300 cursor-pointer flex flex-col h-full"
          >
            <!-- 이미지 영역 -->
            <div class="relative h-56 overflow-hidden bg-[#FFF3DD]">
              <div class="absolute inset-0 flex items-center justify-center text-[#FFE8CC]">
                 <span class="text-4xl">🍞</span>
              </div>
              <img
                :src="bakery.image || 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&h=300&fit=crop'"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 relative z-10"
                :alt="bakery.name"
                @error="handleImageError"
              />
              
              <!-- 평점 뱃지 -->
              <div class="absolute top-4 right-4 z-20 bg-white/95 backdrop-blur-sm px-3 py-1.5 rounded-full flex items-center gap-1 shadow-md border-2 border-[#FFE8CC]">
                <Star class="w-4 h-4 fill-orange-400 text-orange-400" />
                <span class="text-sm font-jua text-[#6B4A38] pt-0.5">{{ bakery.avg_rating ? Number(bakery.avg_rating).toFixed(1) : '0.0' }}</span>
              </div>

              <!-- 호버 오버레이 -->
              <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 flex items-center justify-center">
                 <span class="bg-white/90 text-[#6B4A38] px-4 py-2 rounded-full font-jua text-sm transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                   구경하러 가기 🥐
                 </span>
              </div>
            </div>

            <!-- 텍스트 내용 -->
            <div class="p-6 bg-white relative z-20 flex-1 flex flex-col">
              <h3 class="text-2xl font-jua text-[#6B4A38] mb-2 group-hover:text-[#EF6C00] transition-colors truncate">
                {{ bakery.name }}
              </h3>

              <div class="space-y-2 mb-4 flex-1">
                <p class="text-[#8B6A55] flex items-start gap-2 font-jua text-sm">
                  <MapPin class="w-4 h-4 text-[#C99768] shrink-0 mt-0.5" />
                  <span class="line-clamp-2">{{ bakery.address }}</span>
                </p>
                <p v-if="bakery.business_hours" class="text-[#8B6A55] flex items-center gap-2 font-jua text-sm">
                  <Clock class="w-4 h-4 text-[#C99768] shrink-0" />
                  <span class="truncate">{{ bakery.business_hours }}</span>
                </p>
              </div>

              <!-- 태그 -->
              <div v-if="bakery.representative_tags" class="flex flex-wrap gap-2 mt-auto pt-4 border-t border-[#FFF9F0]">
                <span
                  v-for="(tag, idx) in String(bakery.representative_tags).split(',').slice(0, 3)"
                  :key="idx"
                  class="text-xs px-3 py-1.5 bg-[#FFF3DD] text-[#C99768] rounded-full border border-[#FFE8CC] font-jua"
                >
                  #{{ tag.trim() }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="flex justify-center items-center gap-2 mt-12">
          <!-- 이전 버튼 -->
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="w-10 h-10 rounded-full flex items-center justify-center bg-white border-2 border-[#FFE8CC] text-[#C99768] disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[#FFF3DD] transition-colors font-jua"
          >
            &lt;
          </button>

          <!-- 페이지 번호 -->
          <button
            v-for="page in displayedPages"
            :key="page"
            @click="currentPage = page"
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
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
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
        <h2 class="text-3xl font-jua text-[#6B4A38] mb-3">아직 등록된 빵집이 없어요</h2>
        <p class="text-[#C99768] font-jua text-lg mb-8">다른 맛있는 지역을 탐색해보세요!</p>
        <button
          @click="$router.push({ name: 'home' })"
          class="px-8 py-4 bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] text-white rounded-2xl font-jua text-xl hover:shadow-lg hover:-translate-y-1 transition-all flex items-center justify-center gap-2 mx-auto"
        >
          홈으로 돌아가기 🏠
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, MapPin, Clock } from 'lucide-vue-next'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const bakeries = ref([])
const isLoading = ref(false)

// 페이지네이션 관련
const currentPage = ref(1)
const itemsPerPage = 12 // 페이지당 12개 표시

// 지역 정보 (부산광역시 기준)
const regionData = {
  sasang: { name: '사상구', searchKeyword: '사상', icon: '🥖' },
  busanjin: { name: '부산진구', searchKeyword: '부산진', icon: '🥐' },
  jung: { name: '중구', searchKeyword: '중구', icon: '🍞' },
  dong: { name: '동구', searchKeyword: '동구', icon: '🥯' },
  buk: { name: '북구', searchKeyword: '북구', icon: '🥨' },
  suyeong: { name: '수영구', searchKeyword: '수영', icon: '🧁' },
  haeundae: { name: '해운대구', searchKeyword: '해운대', icon: '🍰' },
  nam: { name: '남구', searchKeyword: '남구', icon: '🎂' }
}

const region = computed(() => route.params.region || 'sasang')
const regionName = computed(() => regionData[region.value]?.name || '빵집 탐색')
const regionIcon = computed(() => regionData[region.value]?.icon || '🥐')
const searchKeyword = computed(() => regionData[region.value]?.searchKeyword || regionData[region.value]?.name || '')

// 페이지네이션 계산
const totalPages = computed(() => Math.ceil(bakeries.value.length / itemsPerPage))

const paginatedBakeries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return bakeries.value.slice(start, end)
})

const displayedPages = computed(() => {
  const pages = []
  const maxPagesToShow = 5

  if (totalPages.value <= maxPagesToShow) {
    // 전체 페이지가 5개 이하면 모두 표시
    for (let i = 1; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    // 현재 페이지 기준으로 앞뒤 2개씩 표시
    let startPage = Math.max(1, currentPage.value - 2)
    let endPage = Math.min(totalPages.value, currentPage.value + 2)

    // 시작이 1이면 끝을 5로
    if (startPage === 1) {
      endPage = Math.min(totalPages.value, maxPagesToShow)
    }

    // 끝이 마지막이면 시작을 조정
    if (endPage === totalPages.value) {
      startPage = Math.max(1, totalPages.value - maxPagesToShow + 1)
    }

    for (let i = startPage; i <= endPage; i++) {
      pages.push(i)
    }
  }

  return pages
})

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&h=300&fit=crop'
}

const fetchBakeries = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/stores/', {
      params: { search: searchKeyword.value }
    })

    // 응답 데이터를 bakeries에 저장
    if (Array.isArray(response.data)) {
      bakeries.value = response.data
    } else if (response.data && typeof response.data === 'object') {
      bakeries.value = response.data.results || response.data.stores || []
    } else {
      bakeries.value = []
    }
  } catch (error) {
    console.error('빵집 목록 불러오기 실패:', error)
    bakeries.value = []
  } finally {
    isLoading.value = false
  }
}

const goToBakery = (id) => {
  router.push({ name: 'detail', params: { id } })
}

// 페이지 변경 시 스크롤을 맨 위로
watch(currentPage, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

// 지역 변경 시 페이지를 1로 초기화
watch(() => route.params.region, () => {
  currentPage.value = 1
  fetchBakeries()
})

onMounted(() => {
  fetchBakeries()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

@keyframes bounceSlow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.animate-bounce-slow {
  animation: bounceSlow 3s infinite ease-in-out;
}
</style>