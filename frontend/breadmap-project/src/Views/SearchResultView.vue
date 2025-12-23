<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] pb-20">
    <!-- 검색 헤더 -->
    <div class="bg-[#1D4E45] text-white py-8 px-6 shadow-xl">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-2xl font-bold mb-4">검색 결과</h1>
        <!-- 검색바 -->
        <div class="relative">
          <input
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text"
            placeholder="빵집, 메뉴, 지역을 검색하세요"
            class="w-full py-3 px-4 pr-12 rounded-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-400"
          />
          <button
            @click="handleSearch"
            class="absolute right-2 top-1/2 -translate-y-1/2 w-9 h-9 bg-orange-500 rounded-full flex items-center justify-center hover:bg-orange-600 transition-colors"
          >
            <Search class="w-5 h-5 text-white" />
          </button>
        </div>
        <p v-if="keyword" class="text-sm text-teal-200 mt-3">
          "<strong class="text-white">{{ keyword }}</strong>" 검색 결과 {{ bakeries.length }}개
        </p>
      </div>
    </div>

    <!-- 검색 결과 -->
    <div class="max-w-4xl mx-auto px-6 py-8">
      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-4 border-teal-800 border-t-transparent mx-auto"></div>
        <p class="mt-4 text-teal-800 font-bold">검색 중...</p>
      </div>

      <!-- 결과 있음 -->
      <div v-else-if="bakeries.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="bakery in bakeries"
          :key="bakery.id"
          @click="goToBakery(bakery.id)"
          class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 cursor-pointer group"
        >
          <!-- 이미지 -->
          <div class="relative h-48 overflow-hidden bg-gray-100">
            <img
              :src="bakery.image || 'https://source.unsplash.com/random/400x300/?bakery'"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              @error="handleImageError"
            />
            <div class="absolute top-3 right-3 bg-white/95 px-3 py-1.5 rounded-full flex items-center gap-1 shadow-md">
              <Star class="w-4 h-4 fill-orange-400 text-orange-400" />
              <span class="text-sm font-bold text-gray-800">{{ bakery.avg_rating || '0.0' }}</span>
            </div>
          </div>

          <!-- 내용 -->
          <div class="p-5">
            <h3 class="text-xl font-bold text-[#1D4E45] mb-2 group-hover:text-orange-600 transition-colors">
              {{ bakery.name }}
            </h3>
            <p class="text-sm text-gray-600 mb-3 flex items-center gap-2">
              <MapPin class="w-4 h-4 text-teal-600" />
              {{ bakery.address }}
            </p>
            <div v-if="bakery.representative_tags" class="flex flex-wrap gap-2">
              <span
                v-for="tag in bakery.representative_tags.split(',')"
                :key="tag"
                class="text-xs px-3 py-1 bg-orange-50 text-orange-700 rounded-full border border-orange-200"
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
        <h2 class="text-2xl font-bold text-gray-800 mb-2">검색 결과가 없습니다</h2>
        <p class="text-gray-600 mb-6">다른 키워드로 검색해보세요!</p>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Star, MapPin } from 'lucide-vue-next'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const keyword = ref('')
const bakeries = ref([])
const isLoading = ref(false)

const handleImageError = (e) => {
  e.target.src = 'https://source.unsplash.com/random/400x300/?bread'
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
  } catch (error) {
    console.error('검색 실패:', error)
  } finally {
    isLoading.value = false
  }
}

const goToBakery = (id) => {
  router.push({ name: 'map', query: { store_id: id } })
}

onMounted(() => {
  if (route.query.search) {
    searchQuery.value = route.query.search
    handleSearch()
  }
})
</script>
