<template>
  <div class="space-y-6">
    <!-- 헤더 -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-orange-500"></span>
        <h2 class="text-2xl font-bold text-orange-500">HOT</h2>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="fetchPosts"
          title="새로고침"
          class="p-2 rounded-full text-gray-500 hover:bg-gray-100 hover:text-gray-800 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.899 2.186l-1.414 1.414A5.002 5.002 0 005.999 7.99V11a1 1 0 11-2 0V3a1 1 0 011-1zm12 3.899A7.003 7.003 0 018.101 16.89l1.414-1.414A5.002 5.002 0 0014.001 12.01V9a1 1 0 112 0v6a1 1 0 01-1 1h-5a1 1 0 110-2h2.01a5.002 5.002 0 00-3.9-3.9l1.414-1.414A7.003 7.003 0 0116 5.899z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 글 목록 -->
    <div class="space-y-4">
      <article
        v-for="post in posts"
        :key="post.id"
        @click="$emit('selectPost', post)"
        :class="[
          'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
          selectedPostId === post.id ? 'ring-2 ring-teal-500 bg-teal-50' : '',
        ]"
      >
        <div class="flex items-center gap-2 mb-3">
          <span class="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full">
            {{ post.category }}
          </span>
        </div>
        <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-1 group-hover:text-teal-900 transition-colors">
          {{ post.title }}
        </h3>
        <p class="text-sm text-gray-600 line-clamp-2">
          {{ post.content }}
        </p>
        <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
          <div class="flex gap-3">
            <span>❤️ {{ post.likes }}</span>
            <span>💬 {{ post.comments }}</span>
            <span>👀 {{ post.views }}k</span>
          </div>
          <span class="inline-flex items-center gap-1 text-teal-700 group-hover:underline">
            자세히 보기
          </span>
        </div>
      </article>

      <p v-if="!posts.length" class="text-center text-sm text-gray-500 py-10">
        좋아요 10개 이상인 인기 글이 없습니다.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const props = defineProps({
  selectedPostId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['selectPost'])

const posts = ref([])

const fetchPosts = async () => {
  try {
    const res = await apiClient.get('/reviews/')
    // 좋아요 10개 이상인 게시글만 가져와서 좋아요 수로 정렬 (인기순)
    posts.value = res.data
      .map((r) => ({
        id: r.id,
        category: r.tags || '빵 주저리',
        type: 'hot',
        title: r.content.split('\n')[0].replace(/\*\*/g, ''),
        content: r.content,
        likes: r.like_users.length,
        like_user_ids: r.like_users,
        comments: r.comments_count || 0,
        views: 0,
        date: r.created_at.slice(0, 10),
        author_id: r.user,
        user_nickname: r.user_nickname,
      }))
      .filter((p) => p.likes >= 10) // 좋아요 10개 이상만 필터링
      .sort((a, b) => b.likes - a.likes) // 좋아요 수 내림차순 정렬
    console.log('HOT 글 로드 (좋아요 10개 이상):', posts.value)
  } catch (e) {
    console.error('HOT 글 불러오기 실패:', e)
  }
}

onMounted(() => {
  fetchPosts()
})
</script>
