<template>
  <div class="p-6">
    <div v-if="posts.length">
      <ul class="space-y-4">
        <li
          v-for="post in posts"
          :key="post.id"
          @click="goToPost(post.id)"
          class="p-5 border rounded-xl bg-white hover:bg-[#F9F7F2] transition-colors cursor-pointer shadow-sm hover:shadow-md"
        >
          <div class="flex items-start gap-3">
            <span
              class="px-3 py-1 rounded-full text-xs font-bold shrink-0"
              :class="getCategoryStyle(post.category)"
            >
              {{ getCategoryLabel(post.category) }}
            </span>
            <div class="flex-1 min-w-0">
              <p class="font-bold text-[#1D4E45] mb-1 line-clamp-2">{{ post.title }}</p>
              <p class="text-xs text-gray-400">
                {{ new Date(post.created_at).toLocaleDateString('ko-KR') }}
              </p>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div v-else class="text-center text-gray-500 py-20">
      <span class="text-5xl mb-4 block">✍️</span>
      <p class="font-medium">아직 작성한 게시글이 없습니다.</p>
      <p class="text-sm text-gray-400 mt-2">커뮤니티에서 이야기를 나눠보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  posts: {
    type: Array,
    default: () => []
  }
});

const router = useRouter();

const goToPost = (id) => {
  router.push({ name: 'community-detail', params: { id } });
};

const getCategoryLabel = (category) => {
  const labels = {
    'tip': '꿀팁',
    'recommend': '추천',
    'chatter': '잡담'
  };
  return labels[category] || category;
};

const getCategoryStyle = (category) => {
  const styles = {
    'tip': 'bg-blue-100 text-blue-700',
    'recommend': 'bg-green-100 text-green-700',
    'chatter': 'bg-purple-100 text-purple-700'
  };
  return styles[category] || 'bg-gray-100 text-gray-700';
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

<style scoped>
/* Add any specific styles here if needed */
</style>
