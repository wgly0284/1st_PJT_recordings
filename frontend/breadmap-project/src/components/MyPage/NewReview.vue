<template>
  <div class="max-w-xl mx-auto space-y-4">
    <h1 class="text-2xl font-bold mb-4">리뷰 작성하기</h1>

    <!-- 카테고리 -->
    <label class="block">
      <span class="text-sm font-semibold">카테고리</span>
      <select
        v-model="category"
        class="mt-1 w-full border rounded-lg px-3 py-2 text-sm bg-white"
      >
        <option disabled value="">카테고리를 선택해주세요</option>
        <option value="빵 주저리">빵 주저리</option>
        <option value="빵집 추천">빵집 추천</option>
        <option value="빵 꿀팁">빵 꿀팁</option>
      </select>
    </label>

    <!-- 제목 -->
    <label class="block">
      <span class="text-sm font-semibold">제목</span>
      <input
        v-model="title"
        type="text"
        class="mt-1 w-full border rounded-lg px-3 py-2 text-sm"
        placeholder="제목을 입력해주세요"
      />
    </label>

    <!-- 내용 -->
    <label class="block">
      <span class="text-sm font-semibold">내용</span>
      <textarea
        v-model="content"
        class="mt-1 w-full border rounded-lg px-3 py-2 text-sm min-h-[120px]"
        placeholder="리뷰 내용을 입력해주세요"
      ></textarea>
    </label>

    <!-- 이미지 첨부 -->
    <label class="block">
      <span class="text-sm font-semibold">이미지 첨부</span>
      <input
        type="file"
        accept="image/*"
        @change="handleImageChange"
        class="mt-1 block w-full text-sm"
      />
    </label>

    <button
      @click="handleSubmit"
      class="inline-block px-6 py-3 bg-teal-900 text-white text-xs font-bold
             rounded-full hover:bg-teal-800 transition-all duration-300 text-center"
    >
      등록하기
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const category = ref('')       // ✅ 카테고리
const title = ref('')
const content = ref('')
const imageFile = ref(null)

const handleImageChange = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  imageFile.value = file
}

const handleSubmit = () => {
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

  // TODO: apiClient.post('/reviews/', formData)
  console.log('전송 데이터:', {
    category: category.value,
    title: title.value,
    content: content.value,
    image: imageFile.value,
  })
}
</script>
