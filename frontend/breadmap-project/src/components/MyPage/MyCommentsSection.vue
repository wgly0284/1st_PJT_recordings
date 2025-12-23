<template>
  <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0]">
    <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2 mb-6">
      <span class="text-2xl">💬</span> My Comments ({{ comments.length }}개)
    </h3>
    <div v-if="comments.length">
      <ul class="space-y-4">
        <li v-for="comment in comments" :key="comment.id" class="p-4 border rounded-lg bg-gray-50">
          <p class="font-semibold">리뷰 ID: {{ comment.review__id }}</p>
          <p class="text-sm text-gray-600 line-clamp-2">{{ comment.content }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ new Date(comment.created_at).toLocaleDateString() }}</p>
        </li>
      </ul>
    </div>
    <div v-else class="text-center text-gray-500 py-4">
      아직 작성한 댓글이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any specific styles here if needed */
</style>
