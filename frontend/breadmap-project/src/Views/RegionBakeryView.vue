<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] pb-20">
    <!-- 헤더 -->
    <div class="bg-[#1D4E45] text-white py-12 px-6 shadow-xl">
      <div class="max-w-6xl mx-auto text-center">
        <div class="text-5xl mb-4">{{ regionIcon }}</div>
        <h1 class="text-3xl font-bold mb-2">{{ regionName }}</h1>
        <p class="text-teal-200">이 지역의 인기 빵집 {{ bakeries.length }}곳</p>
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
      <div v-else-if="bakeries.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="bakery in bakeries"
          :key="bakery.id"
          @click="goToBakery(bakery.id)"
          class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-3 transition-all duration-300 cursor-pointer group"
        >
          <!-- 이미지 -->
          <div class="relative h-56 overflow-hidden bg-gray-100">
            <img
              :src="bakery.image || 'https://source.unsplash.com/random/400x300/?bakery,bread'"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              @error="handleImageError"
            />
            <!-- 평점 뱃지 -->
            <div class="absolute top-4 right-4 bg-white/95 backdrop-blur-sm px-3 py-2 rounded-full flex items-center gap-1.5 shadow-lg">
              <Star class="w-5 h-5 fill-orange-400 text-orange-400" />
              <span class="text-sm font-bold text-gray-800">{{ bakery.avg_rating || '0.0' }}</span>
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, MapPin, Clock } from 'lucide-vue-next'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const bakeries = ref([])
const isLoading = ref(false)

// 지역 정보
const regionData = {
  gangnam: { name: '강남', icon: '🥖' },
  apgujeong: { name: '압구정', icon: '🥐' },
  seongsu: { name: '성수', icon: '🍞' },
  itaewon: { name: '이태원', icon: '🥯' },
  hongdae: { name: '홍대', icon: '🥨' },
  jamsil: { name: '잠실', icon: '🧁' },
  gangbuk: { name: '강북', icon: '🍰' },
  yeonnam: { name: '연남', icon: '🎂' }
}

const region = computed(() => route.params.region || 'gangnam')
const regionName = computed(() => regionData[region.value]?.name || '빵집 탐색')
const regionIcon = computed(() => regionData[region.value]?.icon || '🥐')

const handleImageError = (e) => {
  e.target.src = 'https://source.unsplash.com/random/400x300/?bakery'
}

const fetchBakeries = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://127.0.0.1:8000/stores/', {
      params: { search: regionName.value }
    })
    bakeries.value = response.data
  } catch (error) {
    console.error('빵집 목록 불러오기 실패:', error)
  } finally {
    isLoading.value = false
  }
}

const goToBakery = (id) => {
  router.push({ name: 'map', query: { store_id: id } })
}

onMounted(() => {
  fetchBakeries()
})
</script>
