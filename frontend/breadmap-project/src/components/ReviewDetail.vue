<template>
  <div v-if="review" class="space-y-4">
    <h2 class="text-2xl font-bold">{{ review.title }}</h2>
    <p class="text-sm text-gray-500">{{ review.bakeryName }}</p>
    <p class="text-gray-700 whitespace-pre-line">{{ review.content }}</p>

    <!-- 댓글 목록 -->
    <div class="mt-6">
      <h3 class="font-bold mb-2">Comments ({{ comments.length }})</h3>
      <ul class="space-y-2">
        <li
          v-for="c in comments"
          :key="c.id"
          class="p-3 bg-cream-100 rounded"
        >
          <p class="text-sm font-semibold">{{ c.author }}</p>
          <p class="text-sm text-gray-700">{{ c.text }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  reviewId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['deleted', 'updated'])

const review = ref(null)
const comments = ref([])

const fetchReview = async () => {
  // TODO: 실제 API 사용
  review.value = {
    id: props.reviewId,
    title: '샘플 리뷰 제목',
    bakeryName: '샘플 빵집',
    content: '리뷰 내용입니다.\n빵이 정말 맛있어요!'
  }
  comments.value = [
    { id: 1, author: 'UserA', text: '헉 여기도 가보고 싶어요!' },
    { id: 2, author: 'UserB', text: '소금빵 추천 감사합니다.' }
  ]
}

watch(() => props.reviewId, fetchReview, { immediate: true })
onMounted(fetchReview)
</script>
