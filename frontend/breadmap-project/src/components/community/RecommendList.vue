<template>
  <div class="space-y-6">
    <!-- 헤더 -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <span class="w-2 h-2 rounded-full bg-teal-900"></span>
        <h2 class="text-2xl font-bold text-teal-900">빵집 추천</h2>
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
        <router-link
          :to="{ name: 'newRecommend' }"
          class="px-5 py-2 text-sm font-bold rounded-full bg-orange-500 text-white hover:bg-orange-600 transition-colors whitespace-nowrap"
        >
          글 작성
        </router-link>
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
            빵집 추천
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
        아직 등록된 글이 없습니다. 첫 번째 빵집을 추천해보세요!
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
    posts.value = res.data
      .filter((r) => r.tags === '빵집 추천')
      .map((r) => ({
        id: r.id,
        category: r.tags,
        type: 'recommend',
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
    console.log('빵집 추천 로드:', posts.value)
  } catch (e) {
    console.error('빵집 추천 불러오기 실패:', e)
  }
}

onMounted(() => {
  fetchPosts()
})
</script>
