<template>
  <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0]">
    <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2 mb-6">
      <span class="text-2xl">📝</span> My Reviews ({{ reviews.length }}개)
    </h3>
    <div v-if="reviews.length">
      <ul class="space-y-4">
        <li v-for="review in reviews" :key="review.id" class="p-4 border rounded-lg bg-gray-50">
          <p class="font-semibold">{{ review.store__name }} - {{ review.rating }}점</p>
          <p class="text-sm text-gray-600 line-clamp-2">{{ review.content }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ new Date(review.created_at).toLocaleDateString() }}</p>
        </li>
      </ul>
    </div>
    <div v-else class="text-center text-gray-500 py-4">
      아직 작성한 리뷰가 없습니다.
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
/* Add any specific styles here if needed */
</style>
