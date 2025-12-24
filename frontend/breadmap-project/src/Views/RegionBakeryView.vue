<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] pb-20">
    <!-- 헤더 -->
    <div class="bg-[#1D4E45] text-white py-12 px-6 shadow-xl">
      <div class="max-w-6xl mx-auto text-center">
        <div class="text-5xl mb-4">{{ regionIcon }}</div>
        <h1 class="text-3xl font-bold mb-2">{{ regionName }}</h1>
        <p class="text-teal-200">이 지역의 인기 빵집 총 {{ bakeries.length }}곳 ({{ currentPage }}/{{ totalPages }} 페이지)</p>
      </div>
    </div>

    <!-- 빵집 목록 -->
    <div class="max-w-6xl mx-auto px-6 py-12">
      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-teal-800 border-t-transparent mx-auto"></div>
        <p class="mt-4 text-teal-800 font-bold">빵집을 불러오는 중...</p>
      </div>

      <!-- 빵집 카드 그리드 -->
      <div v-else-if="bakeries.length > 0" class="space-y-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="bakery in paginatedBakeries"
            :key="bakery.id"
            @click="goToBakery(bakery.id)"
            class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-3 transition-all duration-300 cursor-pointer group"
          >
          <!-- 이미지 -->
          <div class="relative h-56 overflow-hidden bg-gray-100">
            <img
              :src="bakery.image || 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&h=300&fit=crop'"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              :alt="bakery.name"
              @error="handleImageError"
            />
            <!-- 평점 뱃지 -->
            <div class="absolute top-4 right-4 bg-white/95 backdrop-blur-sm px-3 py-2 rounded-full flex items-center gap-1.5 shadow-lg">
              <Star class="w-5 h-5 fill-orange-400 text-orange-400" />
              <span class="text-sm font-bold text-gray-800">{{ bakery.avg_rating ? Number(bakery.avg_rating).toFixed(1) : 'N/A' }}</span>
            </div>
            <!-- 호버 오버레이 -->
            <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center">
              <span class="text-white font-bold text-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                자세히 보기 →
              </span>
            </div>
          </div>

          <!-- 내용 -->
          <div class="p-6">
            <h3 class="text-xl font-bold text-[#1D4E45] mb-3 group-hover:text-orange-600 transition-colors line-clamp-1">
              {{ bakery.name }}
            </h3>

            <div class="space-y-2 mb-4">
              <p class="text-sm text-gray-600 flex items-start gap-2">
                <MapPin class="w-4 h-4 text-teal-600 mt-0.5 shrink-0" />
                <span class="line-clamp-1">{{ bakery.address }}</span>
              </p>
              <p v-if="bakery.business_hours" class="text-sm text-gray-600 flex items-center gap-2">
                <Clock class="w-4 h-4 text-teal-600 shrink-0" />
                <span>{{ bakery.business_hours }}</span>
              </p>
            </div>

            <!-- 태그 -->
            <div v-if="bakery.representative_tags" class="flex flex-wrap gap-2">
              <span
                v-for="(tag, idx) in bakery.representative_tags.split(',').slice(0, 3)"
                :key="idx"
                class="text-xs px-3 py-1 bg-orange-50 text-orange-700 rounded-full border border-orange-200 font-medium"
              >
                #{{ tag.trim() }}
              </span>
            </div>
          </div>
        </div>
        </div>

        <!-- 페이지네이션 -->
        <div class="flex justify-center items-center gap-2 mt-8">
          <!-- 이전 버튼 -->
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-4 py-2 rounded-lg border-2 border-orange-200 text-orange-600 font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-orange-50 transition-colors"
          >
            ← 이전
          </button>

          <!-- 페이지 번호 -->
          <button
            v-for="page in displayedPages"
            :key="page"
            @click="currentPage = page"
            :class="[
              'w-10 h-10 rounded-lg font-bold transition-all',
              currentPage === page
                ? 'bg-orange-500 text-white shadow-lg scale-110'
                : 'bg-white border-2 border-orange-200 text-orange-600 hover:bg-orange-50'
            ]"
          >
            {{ page }}
          </button>

          <!-- 다음 버튼 -->
          <button
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 rounded-lg border-2 border-orange-200 text-orange-600 font-bold disabled:opacity-30 disabled:cursor-not-allowed hover:bg-orange-50 transition-colors"
          >
            다음 →
          </button>
        </div>
      </div>

      <!-- 결과 없음 -->
      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">🥐</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">아직 등록된 빵집이 없습니다</h2>
        <p class="text-gray-600 mb-6">다른 지역을 탐색해보세요!</p>
        <button
          @click="$router.push({ name: 'home' })"
          class="px-6 py-3 bg-teal-600 text-white rounded-full font-bold hover:bg-teal-700 transition-colors"
        >
          홈으로 돌아가기
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
    // 검색 키워드로 검색 (예: "사상", "북구" 등)
    console.log(`🔍 검색 시작: 지역=${regionName.value}, 키워드="${searchKeyword.value}"`)

    const response = await axios.get('http://127.0.0.1:8000/stores/', {
      params: { search: searchKeyword.value }
    })

    console.log('📦 API 응답 데이터:', response.data)
    console.log('📊 응답 데이터 타입:', typeof response.data)
    console.log('📋 응답 데이터 길이:', Array.isArray(response.data) ? response.data.length : 'Array가 아님')

    // 응답 데이터를 bakeries에 저장
    if (Array.isArray(response.data)) {
      bakeries.value = response.data
      console.log(`✅ ${regionName.value} 지역 빵집 ${bakeries.value.length}개 로드 완료`)
    } else if (response.data && typeof response.data === 'object') {
      // 만약 data가 객체로 감싸져 있다면
      bakeries.value = response.data.results || response.data.stores || []
      console.log(`✅ ${regionName.value} 지역 빵집 ${bakeries.value.length}개 로드 완료 (중첩 객체)`)
    } else {
      console.warn('⚠️ 예상치 못한 응답 형식:', response.data)
      bakeries.value = []
    }
  } catch (error) {
    console.error('❌ 빵집 목록 불러오기 실패:', error)
    console.error('에러 상세:', error.response?.data || error.message)
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
