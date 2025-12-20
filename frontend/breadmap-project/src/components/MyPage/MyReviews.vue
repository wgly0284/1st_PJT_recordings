<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">My Reviews</h1>
    <ul v-if="myReviews.length > 0" class="space-y-2">
      <li
        v-for="review in myReviews"
        :key="review.id"
        @click="selectReview(review.id)"
        class="p-3 border rounded cursor-pointer hover:bg-cream-100"
        :class="{ 'bg-cream-200': review.id === selectedReviewId }"
      >
        <p class="font-bold truncate">{{ review.title }}</p>
        <p class="text-sm text-gray-500 truncate">
          {{ review.bakeryName || review.store?.name }}
        </p>
      </li>
    </ul>
    <p v-else class="text-gray-500">아직 작성한 리뷰가 없습니다.</p>
  </div>
  <router-link
    :to="{ name: 'newReview' }"
    class="inline-block px-6 py-3 bg-teal-900 text-white text-xs font-bold
          rounded-full hover:bg-teal-800 transition-all duration-300 text-center"
  >
    리뷰 작성하기
  </router-link>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'
import NewReview from './NewReview.vue'

const myReviews = ref([])
const selectedReviewId = ref(null)

// 개발용 목데이터
const mockReviews = [
  { id: 1, title: '성수 어니언 베이글 존맛', bakeryName: 'Onion Bagle' },
  { id: 2, title: '제주 사워도우 빵지순례', bakeryName: 'Wheat & Grain' },
]

const fetchMyReviews = async () => {
  try {
    // 1) 실제 API 호출
    const res = await apiClient.get('/reviews/my/')
    myReviews.value = res.data

    // 2) 개발 환경이고, 아직 리뷰가 없다면 목데이터 사용
    if (import.meta.env.DEV && myReviews.value.length === 0) {
      myReviews.value = mockReviews
    }

    if (myReviews.value.length > 0) {
      selectedReviewId.value = myReviews.value[0].id
    }
  } catch (error) {
    console.error('Failed to fetch my reviews:', error)
    // 3) API 에러 나면 개발 환경에서만 목데이터로 대체
    if (import.meta.env.DEV) {
      myReviews.value = mockReviews
      selectedReviewId.value = mockReviews[0].id
    }
  }
}


onMounted(fetchMyReviews)
</script>
