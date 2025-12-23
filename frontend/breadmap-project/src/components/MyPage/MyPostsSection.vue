<template>
  <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0]">
    <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2 mb-6">
      <span class="text-2xl">✍️</span> My Community Posts ({{ posts.length }}개)
    </h3>
    <div v-if="posts.length">
      <ul class="space-y-4">
        <li v-for="post in posts" :key="post.id" class="p-4 border rounded-lg bg-gray-50">
          <p class="font-semibold">[{{ post.category }}] {{ post.title }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ new Date(post.created_at).toLocaleDateString() }}</p>
        </li>
      </ul>
    </div>
    <div v-else class="text-center text-gray-500 py-4">
      아직 작성한 게시글이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  posts: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
/* Add any specific styles here if needed */
</style>
