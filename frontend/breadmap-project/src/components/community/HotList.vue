<template>
  <div class="space-y-6 p-4">
    <!-- 헤더 -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <span class="w-3 h-3 rounded-full bg-[#FF7043] animate-pulse"></span>
        <h2 class="text-2xl font-bold text-[#BF360C] font-serif">HOT Issues</h2>
      </div>
      <div class="flex items-center gap-2">
        <button @click="fetchPosts" title="새로고침" class="p-2 rounded-full text-[#8D6E63] hover:bg-[#EFEBE9] hover:text-[#5D4037] transition-colors">
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
          'group bg-white p-5 rounded-3xl border border-[#E0E0E0] cursor-pointer hover:shadow-lg hover:-translate-y-1 transition-all',
          selectedPostId === post.id ? 'ring-2 ring-[#FFAB91] bg-[#FBE9E7]' : 'hover:border-[#FFCCBC]',
        ]"
      >
        <div class="flex items-center gap-2 mb-3">
          <span class="px-3 py-1 bg-[#FFCCBC] text-[#BF360C] text-xs font-bold rounded-full">
            {{ post.category }}
          </span>
        </div>
        <h3 class="text-lg font-bold text-[#4E342E] mb-2 line-clamp-1 group-hover:text-[#BF360C] transition-colors">
          {{ post.title }}
        </h3>
        <p class="text-sm text-[#795548] line-clamp-2">
          {{ post.content }}
        </p>
        <div class="flex items-center justify-between mt-3 text-xs text-[#A1887F]">
          <div class="flex gap-3 font-medium">
            <span>❤️ {{ post.likes }}</span>
            <span>💬 {{ post.comments }}</span>
            <span>👀 {{ post.views }}k</span>
          </div>
          <span class="inline-flex items-center gap-1 text-[#8D6E63] font-bold group-hover:underline">
            자세히 보기
          </span>
        </div>
      </article>

      <p v-if="!posts.length" class="text-center text-sm text-[#A1887F] py-10 bg-white/50 rounded-2xl border border-dashed border-[#D7CCC8]">
        아직 갓 구운 인기 글이 없어요. 🥐
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const props = defineProps({
  selectedPostId: { type: Number, default: null },
})
const emit = defineEmits(['selectPost'])
const posts = ref([])

const fetchPosts = async () => {
  try {
    const res = await apiClient.get('/community/')
    posts.value = res.data
      .map((p) => ({
        id: p.id,
        category: p.category || '빵 주저리',
        type: 'hot',
        title: p.title,
        content: p.content,
        likes: p.like_count || 0,
        like_user_ids: p.like_users || [],
        comments: p.comments_count || 0,
        views: 0,
        date: p.created_at.slice(0, 10),
        author_id: p.author,
        user_nickname: p.author_nickname,
        image: p.image,
      }))
      .filter((p) => p.likes >= 10)
      .sort((a, b) => b.likes - a.likes)
  } catch (e) {
    console.error('HOT 글 불러오기 실패:', e)
  }
}

onMounted(() => { fetchPosts() })
</script>

<style scoped>
.font-serif { font-family: 'Gaegu', cursive; }
</style>