<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios'

const router = useRouter()

const title = ref('')
const content = ref('')
// 카테고리 고정
const category = '빵 꿀팁'
const imageFile = ref(null)
const isSubmitting = ref(false)

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

  try {
    isSubmitting.value = true

    const formData = new FormData()
    formData.append('title', title.value)
    formData.append('content', content.value)
    formData.append('category', category) // 꿀팁 카테고리 전송

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    // Community 앱 API 호출 (기존 코드에서 review 호출하던 부분 수정됨)
    await apiClient.post('/api/community/create/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    alert('꿀팁이 등록되었습니다!')
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
  <div class="max-w-4xl mx-auto px-6 space-y-8 py-10">
    <div class="text-center lg:text-left">
      <h1 class="text-3xl md:text-4xl font-playfair font-bold text-teal-900 mb-2">
        빵 꿀팁 공유
      </h1>
      <p class="text-lg text-gray-600">
        나만 알기 아까운 빵 보관법, 맛있게 먹는 법을 공유해주세요.
      </p>
    </div>

    <div class="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 md:p-8">
      <div class="flex items-center gap-2 mb-4">
        <span class="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-bold rounded-full">
          {{ category }}
        </span>
      </div>

      <div class="space-y-5">
        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">제목</span>
          <input
            v-model="title"
            type="text"
            class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            placeholder="예: 바게트 눅눅하지 않게 보관하는 법"
          />
        </label>

        <label class="block text-left">
          <span class="text-sm font-semibold text-gray-700">내용</span>
          <textarea
            v-model="content"
            class="mt-1 w-full border rounded-lg px-3 py-2 text-sm min-h-[160px] bg-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            placeholder="자세한 팁을 적어주세요."
          ></textarea>
        </label>

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
        <button
          @click="router.go(-1)"
          class="inline-flex items-center justify-center px-6 py-3 border border-gray-200 text-sm font-semibold rounded-full text-gray-600 hover:bg-gray-50"
        >
          취소
        </button>
        <button
          @click="handleSubmit"
          :disabled="isSubmitting"
          class="inline-flex items-center justify-center px-8 py-3 bg-amber-600 text-white text-sm font-bold rounded-full hover:bg-amber-700 disabled:bg-gray-400 transition-all"
        >
          {{ isSubmitting ? '등록 중...' : '등록하기' }}
        </button>
      </div>
    </div>
  </div>
</template>