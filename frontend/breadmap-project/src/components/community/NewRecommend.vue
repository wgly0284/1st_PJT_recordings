<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()
const route = useRoute()

const stores = ref([])
const storeQuery = ref('')
const storeId = ref(route.params.storeId || '')

const title = ref('')
const content = ref('')
const rating = ref(5)
const tasteTags = ref('')
const imageFile = ref(null)
const isSubmitting = ref(false)

onMounted(async () => {
  try {
    const res = await apiClient.get('/stores/')
    stores.value = res.data
  } catch (e) {
    console.error('가게 목록 불러오기 실패:', e)
  }
})

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
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  if (!storeId.value) {
    alert('추천할 빵집을 선택해주세요.')
    return
  }

  try {
    isSubmitting.value = true

    const formData = new FormData()
    formData.append('store', storeId.value)
    formData.append('rating', rating.value)
    formData.append('title', title.value)
    formData.append('content', content.value)
    formData.append('tags', '빵집 추천')
    formData.append('taste_tags', tasteTags.value || '')

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    await apiClient.post('/reviews/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    alert('빵집 추천글이 등록되었습니다!')
    router.push({ name: 'community' })
  } catch (e) {
    console.error('게시글 등록 실패:', e.response?.data || e)
    alert('게시글 등록 중 오류가 발생했습니다.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50/50 pt-32 pb-32">
    <div class="max-w-4xl mx-auto px-6 space-y-8">
      <!-- 헤더 -->
      <div class="text-center lg:text-left">
        <h1
          class="text-4xl md:text-5xl font-playfair font-bold bg-gradient-to-r from-teal-900 to-teal-700 bg-clip-text text-transparent mb-2"
        >
          빵집 추천 작성
        </h1>
        <p class="text-xl text-gray-600">
          맛있는 빵집을 다른 사람들에게 추천해주세요.
        </p>
      </div>

      <!-- 작성 카드 -->
      <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 md:p-8">
        <div class="flex items-center gap-2 mb-4">
          <span class="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full">
            빵집 추천
          </span>
        </div>

        <div class="space-y-5">
          <!-- 가게 검색/선택 -->
          <div class="space-y-2">
            <span class="text-sm font-semibold text-gray-700">가게 선택 (필수)</span>

            <!-- 검색 입력 -->
            <input
              v-model="storeQuery"
              type="text"
              class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800 focus:border-teal-800"
              placeholder="가게 이름 또는 주소를 입력해서 검색하세요"
            />

            <!-- 검색 결과 리스트 -->
            <div
              v-if="filteredStores.length"
              class="max-h-52 overflow-y-auto border border-gray-200 rounded-xl divide-y"
            >
              <button
                v-for="store in filteredStores"
                :key="store.id"
                type="button"
                @click="storeId = store.id"
                :class="[
                  'w-full px-3 py-2 text-left text-sm hover:bg-teal-50',
                  storeId === store.id ? 'bg-teal-100' : ''
                ]"
              >
                <div class="font-semibold text-gray-900">
                  {{ store.name }}
                </div>
                <div class="text-xs text-gray-500">
                  {{ store.address }}
                </div>
              </button>
            </div>

            <p v-else class="text-xs text-gray-400">
              검색 결과가 없습니다.
            </p>

            <!-- 선택된 가게 표시 -->
            <p v-if="storeId" class="text-xs text-teal-700 mt-1">
              선택된 가게 ID: {{ storeId }}
            </p>
          </div>

          <!-- 제목 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">제목</span>
            <input
              v-model="title"
              type="text"
              class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800 focus:border-teal-800"
              placeholder="제목을 입력해주세요"
            />
          </label>

          <!-- 내용 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">내용</span>
            <textarea
              v-model="content"
              class="mt-1 w-full border rounded-lg px-3 py-2 text-sm min-h-[160px] bg-white focus:outline-none focus:ring-2 focus:ring-teal-800 focus:border-teal-800"
              placeholder="이 빵집을 추천하는 이유를 적어주세요."
            ></textarea>
          </label>

          <!-- 평점 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">평점</span>
            <select
              v-model.number="rating"
              class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800 focus:border-teal-800"
            >
              <option :value="5">⭐⭐⭐⭐⭐ (5점)</option>
              <option :value="4">⭐⭐⭐⭐ (4점)</option>
              <option :value="3">⭐⭐⭐ (3점)</option>
              <option :value="2">⭐⭐ (2점)</option>
              <option :value="1">⭐ (1점)</option>
            </select>
          </label>

          <!-- 이미지 첨부 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">이미지 첨부 (선택)</span>
            <input
              type="file"
              accept="image/*"
              @change="handleImageChange"
              class="mt-1 block w-full text-sm text-gray-700"
            />
            <p v-if="imageFile" class="mt-1 text-xs text-gray-500">
              선택된 파일: {{ imageFile.name }}
            </p>
          </label>
        </div>

        <div class="mt-8 flex flex-col sm:flex-row justify-between gap-3">
          <router-link
            :to="{ name: 'community' }"
            class="inline-flex items-center justify-center px-6 py-3 border border-gray-200 text-sm font-semibold rounded-full text-gray-600 hover:bg-gray-50"
          >
            취소하고 돌아가기
          </router-link>

          <button
            @click="handleSubmit"
            :disabled="isSubmitting"
            class="inline-flex items-center justify-center px-8 py-3 bg-teal-900 text-white text-sm font-bold
                   rounded-full hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300"
          >
            {{ isSubmitting ? '등록 중...' : '등록하기' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
