<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()
const route = useRoute()

const stores = ref([])
const storeQuery = ref('')
// 라우터 파라미터로 storeId가 넘어오면 미리 선택
const storeId = ref(route.params.storeId || '')

const title = ref('')
const content = ref('')
const rating = ref(5)
const tasteTags = ref('')
const imageFile = ref(null)
const isSubmitting = ref(false)

// 가게 목록 불러오기
onMounted(async () => {
  try {
    const res = await apiClient.get('/stores/')
    stores.value = res.data
  } catch (e) {
    console.error('가게 목록 로드 실패:', e)
  }
})

// 가게 검색 필터링
const filteredStores = computed(() => {
  const q = storeQuery.value.trim().toLowerCase()
  if (!q) return stores.value.slice(0, 20)
  return stores.value.filter((s) =>
    `${s.name} ${s.address || ''}`.toLowerCase().includes(q)
  ).slice(0, 20)
})

const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  imageFile.value = file
}

const handleSubmit = async () => {
  if (!storeId.value) {
    alert('추천할 빵집을 선택해주세요.')
    return
  }
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  try {
    isSubmitting.value = true

    const formData = new FormData()
    formData.append('store', storeId.value) // 필수: 가게 ID
    formData.append('rating', rating.value) // 필수: 평점
    formData.append('title', title.value)
    formData.append('content', content.value)
    formData.append('tags', '빵집 추천') // 리뷰 모델의 태그로 구분
    formData.append('taste_tags', tasteTags.value || '')

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    // Review 앱 API 사용 (가게 정보 연결을 위해)
    await apiClient.post('/reviews/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    alert('빵집 추천글이 등록되었습니다!')
    router.push({ name: 'community' })
  } catch (e) {
    console.error('추천글 등록 실패:', e.response?.data || e)
    alert('등록 중 오류가 발생했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-6 space-y-8 py-10">
    <div class="text-center lg:text-left">
      <h1 class="text-3xl md:text-4xl font-playfair font-bold text-teal-900 mb-2">
        빵집 추천하기
      </h1>
      <p class="text-lg text-gray-600">
        맛있는 빵집을 다른 사람들에게 알려주세요.
      </p>
    </div>

    <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 md:p-8">
      <div class="flex items-center gap-2 mb-4">
        <span class="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full">
          빵집 추천
        </span>
      </div>

      <div class="space-y-5">
        <!-- 가게 검색 -->
        <div class="space-y-2">
          <span class="text-sm font-semibold text-gray-700">가게 선택 (필수)</span>
          <input
            v-model="storeQuery"
            type="text"
            class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800"
            placeholder="가게 이름 검색..."
          />
          
          <!-- 검색 결과 -->
          <div v-if="storeQuery && filteredStores.length" class="max-h-40 overflow-y-auto border rounded-lg divide-y mt-1">
            <button
              v-for="store in filteredStores"
              :key="store.id"
              @click="storeId = store.id; storeQuery = store.name"
              class="w-full text-left px-3 py-2 text-sm hover:bg-teal-50 flex flex-col"
              :class="{ 'bg-teal-50': storeId === store.id }"
            >
              <span class="font-bold">{{ store.name }}</span>
              <span class="text-xs text-gray-500">{{ store.address }}</span>
            </button>
          </div>
          <p v-if="storeId" class="text-xs text-teal-600 font-bold mt-1">
            ✓ 가게가 선택되었습니다.
          </p>
        </div>

        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">제목</span>
          <input
            v-model="title"
            type="text"
            class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800"
            placeholder="제목을 입력해주세요"
          />
        </label>

        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">내용</span>
          <textarea
            v-model="content"
            class="mt-1 w-full border rounded-lg px-3 py-2 text-sm min-h-[160px] bg-white focus:outline-none focus:ring-2 focus:ring-teal-800"
            placeholder="추천 이유를 자세히 적어주세요."
          ></textarea>
        </label>

        <!-- 평점 선택 -->
        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">평점</span>
          <div class="flex gap-2 mt-1">
            <button 
              v-for="star in 5" 
              :key="star" 
              @click="rating = star"
              type="button"
              class="text-2xl focus:outline-none transition-transform active:scale-110"
              :class="star <= rating ? 'text-yellow-400' : 'text-gray-300'"
            >
              ★
            </button>
            <span class="text-sm text-gray-500 self-center ml-2">{{ rating }}점</span>
          </div>
        </label>

        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">이미지 첨부</span>
          <input
            type="file"
            accept="image/*"
            @change="handleImageChange"
            class="mt-1 block w-full text-sm text-gray-700"
          />
        </label>
      </div>

      <div class="mt-8 flex flex-col sm:flex-row justify-between gap-3">
        <button
          @click="router.go(-1)"
          class="inline-flex items-center justify-center px-6 py-3 border border-gray-200 text-sm font-semibold rounded-full text-gray-600 hover:bg-gray-50"
        >
          취소
        </button>
        <button
          @click="handleSubmit"
          :disabled="isSubmitting"
          class="inline-flex items-center justify-center px-8 py-3 bg-teal-900 text-white text-sm font-bold rounded-full hover:bg-teal-800 disabled:bg-gray-400 transition-all"
        >
          {{ isSubmitting ? '등록 중...' : '등록하기' }}
        </button>
      </div>
    </div>
  </div>
</template>