<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()

const category = ref('')
const title = ref('')
const content = ref('')
const imageFile = ref(null)
const isSubmitting = ref(false)

const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  imageFile.value = file
}

const handleSubmit = async () => {
  if (!category.value || !title.value || !content.value) {
    alert('카테고리, 제목, 내용을 모두 입력해주세요.')
    return
  }
  
  const formData = new FormData()
  formData.append('category', category.value)
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  try {
    isSubmitting.value = true
    const res = await apiClient.post('/community/create/', formData)
    alert('게시글이 등록되었습니다!')
    router.push({ name: 'community' }) 
  } catch (e) {
    console.error('게시글 등록 실패:', e)
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
          WRITE POST
        </h1>
        <p class="text-xl text-gray-600">
          빵에 대한 당신의 이야기를 자유롭게 공유해주세요.
        </p>
      </div>

      <!-- 작성 카드 -->
      <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 md:p-8">
        <h2 class="text-sm font-bold text-gray-500 tracking-widest mb-4">
          NEW POST FORM
        </h2>

        <div class="space-y-5">
          <!-- 카테고리 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">카테고리</span>
            <select
              v-model="category"
              class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-teal-800 focus:border-teal-800"
            >
              <option disabled value="">카테고리를 선택해주세요</option>
              <option value="빵 주저리">빵 주저리</option>
              <option value="빵집 추천">빵집 추천</option>
              <option value="빵 꿀팁">빵 꿀팁</option>
            </select>
          </label>

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
              placeholder="자유롭게 당신의 이야기를 적어주세요."
            ></textarea>
          </label>

          <!-- 이미지 첨부 -->
          <label class="block text-left">
            <span class="text-sm font-semibold text-gray-700">이미지 첨부</span>
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
