<template>
  <div class="min-h-screen bg-gray-50/50 pt-32 pb-32">
    <div class="max-w-7xl mx-auto px-6 space-y-8">
      <!-- 헤더 -->
      <div class="text-center lg:text-left">
        <h1
          class="text-4xl md:text-5xl font-playfair font-bold bg-gradient-to-r from-teal-900 to-teal-700 bg-clip-text text-transparent mb-2"
        >
          MY POSTS
        </h1>
        <p class="text-xl text-gray-600">
          내가 작성한 커뮤니티 게시글을 한눈에 모아보는 공간
        </p>
      </div>

      <!-- 데스크톱 레이아웃 -->
      <div class="hidden lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- 리스트 영역 -->
        <section class="space-y-6 lg:col-span-2">
          <h2 class="text-sm font-bold text-gray-500 tracking-widest">
            POST LIST
          </h2>

          <div class="space-y-4">
            <article
              v-for="post in myPosts"
              :key="post.id"
              @click="selectPost(post)"
              :class="[
                'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
                selectedPost && selectedPost.id === post.id ? 'ring-2 ring-teal-500 bg-teal-50' : '',
              ]"
            >
              <div class="flex items-center justify-between mb-2 text-xs text-gray-400">
                <span class="px-3 py-1 bg-teal-50 text-teal-700 font-semibold rounded-full">
                  {{ post.category }}
                </span>
                <span v-if="post.created_at">
                  {{ formatDate(post.created_at) }}
                </span>
              </div>
              <h3
                class="text-lg font-bold text-gray-900 mb-1 line-clamp-1 group-hover:text-teal-900 transition-colors"
              >
                {{ post.title || '제목 없는 게시글' }}
              </h3>
              <p class="text-sm text-gray-600 line-clamp-2">
                {{ post.content }}
              </p>
              <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
                <div class="flex gap-3">
                  <span>❤️ {{ post.likes || 0 }}</span>
                  <span>💬 {{ post.comments || 0 }}</span>
                </div>
                <button
                  type="button"
                  class="inline-flex items-center gap-1 text-teal-700"
                >
                  자세히 보기
                </button>
              </div>
            </article>

            <p
              v-if="!myPosts.length"
              class="text-center text-sm text-gray-500 py-10"
            >
              아직 작성한 게시글이 없습니다. 커뮤니티에 첫 번째 글을 남겨보세요!
            </p>
          </div>
        </section>

        <!-- 상세 영역 + 작성 버튼 -->
        <section class="lg:col-span-1 space-y-4">
          <!-- 상세 카드 -->
          <div
            v-if="selectedPost"
            class="bg-white rounded-3xl border border-gray-100 p-6 shadow-sm space-y-3"
          >
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-bold text-gray-500 tracking-widest mb-1">
                POST DETAIL
              </h3>
              <button
                @click="deletePost(selectedPost.id)"
                :disabled="isDeletingPost"
                class="px-3 py-1.5 text-xs font-semibold text-red-600 hover:text-white hover:bg-red-600 border border-red-600 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isDeletingPost ? '삭제 중...' : '삭제' }}
              </button>
            </div>
            <div class="flex items-center gap-2 mb-2">
              <span class="px-3 py-1 bg-teal-50 text-teal-700 text-xs font-semibold rounded-full">
                {{ selectedPost.category }}
              </span>
            </div>
            <h2 class="text-xl font-bold text-gray-900 mb-1">
              {{ selectedPost.title || '제목 없는 게시글' }}
            </h2>
            <div class="flex items-center gap-2 text-sm text-gray-500 mb-3">
              <span>❤️ {{ selectedPost.likes || 0 }}</span>
              <span>💬 {{ selectedPost.comments || 0 }}</span>
              <span v-if="selectedPost.created_at">
                · {{ formatDate(selectedPost.created_at) }}
              </span>
            </div>
            <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">
              {{ selectedPost.content }}
            </p>
          </div>

          <!-- 새 글 작성 카드 -->
          <div class="bg-white rounded-3xl border border-gray-100 p-6 shadow-sm">
            <h3 class="text-lg font-bold text-teal-900 mb-2">새 글 작성</h3>
            <p class="text-sm text-gray-600 mb-4">
              빵 이야기를 나누고 싶으신가요?
              커뮤니티에 새로운 글을 작성해보세요.
            </p>
            <router-link
              :to="{ name: 'community' }"
              class="inline-flex items-center justify-center w-full px-6 py-3 bg-teal-900 text-white text-sm font-bold
                     rounded-full hover:bg-teal-800 transition-all duration-300"
            >
              커뮤니티로 이동
            </router-link>
          </div>

          <div class="bg-teal-900 text-white rounded-3xl p-6 shadow-sm space-y-2">
            <h4 class="text-sm font-semibold tracking-widest text-teal-100">
              TIP
            </h4>
            <p class="text-sm">
              다른 빵덕후들과 소통하며 더 많은 빵집 정보를 얻어보세요!
            </p>
          </div>
        </section>
      </div>

      <!-- 모바일 / 태블릿 레이아웃 -->
      <div class="lg:hidden space-y-6">
        <section class="space-y-4">
          <h2 class="text-sm font-bold text-gray-500 tracking-widest text-center">
            MY POSTS
          </h2>

          <article
            v-for="post in myPosts"
            :key="post.id"
            @click="selectPost(post)"
            :class="[
              'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
              selectedPost && selectedPost.id === post.id ? 'ring-2 ring-teal-500 bg-teal-50' : '',
            ]"
          >
            <div class="flex items-center justify-between mb-2 text-xs text-gray-400">
              <span class="px-3 py-1 bg-teal-50 text-teal-700 font-semibold rounded-full">
                {{ post.category }}
              </span>
              <span v-if="post.created_at">
                {{ formatDate(post.created_at) }}
              </span>
            </div>
            <h3
              class="text-base font-bold text-gray-900 mb-1 line-clamp-1 group-hover:text-teal-900 transition-colors"
            >
              {{ post.title || '제목 없는 게시글' }}
            </h3>
            <p class="text-sm text-gray-600 line-clamp-2">
              {{ post.content }}
            </p>
            <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
              <div class="flex gap-3">
                <span>❤️ {{ post.likes || 0 }}</span>
                <span>💬 {{ post.comments || 0 }}</span>
              </div>
              <button
                type="button"
                class="inline-flex items-center gap-1 text-teal-700"
              >
                자세히 보기
              </button>
            </div>

            <!-- 모바일 상세: 선택된 카드 아래에 전체 내용 표시 -->
            <div
              v-if="selectedPost && selectedPost.id === post.id"
              class="mt-4 border-t border-gray-100 pt-3 text-sm text-gray-700 whitespace-pre-line"
            >
              {{ post.content }}
            </div>
          </article>

          <p
            v-if="!myPosts.length"
            class="text-center text-sm text-gray-500 py-10"
          >
            아직 작성한 게시글이 없습니다. 커뮤니티에 첫 번째 글을 남겨보세요!
          </p>
        </section>

        <section class="pt-2">
          <router-link
            :to="{ name: 'community' }"
            class="inline-flex items-center justify-center w-full px-6 py-3 bg-teal-900 text-white text-sm font-bold
                   rounded-full hover:bg-teal-800 transition-all duration-300"
          >
            커뮤니티로 이동
          </router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const myPosts = ref([])
const selectedPost = ref(null)
const isDeletingPost = ref(false)

const fetchMyPosts = async () => {
  try {
    const res = await apiClient.get('/community/my/')
    myPosts.value = res.data

    if (myPosts.value.length > 0) {
      selectedPost.value = myPosts.value[0]
    }
  } catch (error) {
    console.error('Failed to fetch my posts:', error)
  }
}

const selectPost = (post) => {
  selectedPost.value = post
}

const formatDate = (value) => {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return value
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
}

const deletePost = async (postId) => {
  if (!confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    return
  }

  try {
    isDeletingPost.value = true
    await apiClient.delete(`/community/${postId}/`)

    // 게시글 목록에서 제거
    myPosts.value = myPosts.value.filter(p => p.id !== postId)

    // 선택된 게시글이 삭제된 게시글이라면 선택 해제
    if (selectedPost.value?.id === postId) {
      selectedPost.value = myPosts.value.length > 0 ? myPosts.value[0] : null
    }

    alert('게시글이 삭제되었습니다.')
  } catch (error) {
    console.error('게시글 삭제 실패:', error)
    alert('게시글 삭제 중 오류가 발생했습니다.')
  } finally {
    isDeletingPost.value = false
  }
}

import { useRoute } from 'vue-router'

const route = useRoute()

onMounted(() => {
  fetchMyPosts().then(() => {
    const selectedId = Number(route.query.selectedId)
    if (selectedId && myPosts.value.length) {
      const found = myPosts.value.find(p => p.id === selectedId)
      if (found) selectedPost.value = found
    }
  })
})
</script>
