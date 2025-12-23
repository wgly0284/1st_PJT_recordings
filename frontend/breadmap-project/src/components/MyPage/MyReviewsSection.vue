<template>
  <div class="p-6">
    <div v-if="reviews.length">
      <ul class="space-y-4">
        <li
          v-for="review in reviews"
          :key="review.id"
          class="p-5 border rounded-xl bg-white hover:bg-[#F9F7F2] transition-colors cursor-pointer shadow-sm hover:shadow-md"
        >
          <div class="flex justify-between items-start mb-2">
            <p class="font-bold text-[#1D4E45]">{{ review.store__name || '빵집' }}</p>
            <div class="flex items-center gap-1">
              <span class="text-orange-500">★</span>
              <span class="text-sm font-bold text-orange-500">{{ review.rating }}</span>
            </div>
          </div>
          <p class="text-sm text-gray-700 line-clamp-3 mb-2">{{ review.content }}</p>
          <p class="text-xs text-gray-400">
            {{ new Date(review.created_at).toLocaleDateString('ko-KR') }}
          </p>
        </li>
      </ul>
    </div>
    <div v-else class="text-center text-gray-500 py-20">
      <span class="text-5xl mb-4 block">📝</span>
      <p class="font-medium">아직 작성한 리뷰가 없습니다.</p>
      <p class="text-sm text-gray-400 mt-2">방문한 빵집에 리뷰를 남겨보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  reviews: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<style scoped>
/* Add any specific styles here if needed */
</style>
