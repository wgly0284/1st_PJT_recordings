<template>
  <div class="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
    <!-- 헤더 -->
    <header class="bg-gradient-to-r from-teal-900 to-teal-700 text-white p-6 lg:p-8">
      <div class="flex items-center justify-between mb-4 gap-3 flex-wrap">
        <span class="px-4 py-1 bg-white/20 rounded-full text-xs font-bold">
          {{ post.category }}
        </span>
        <div class="flex gap-4 text-xs lg:text-sm opacity-90 flex-wrap">
          <span>❤️ {{ localLikes }}</span>
          <span>💬 {{ commentsCount }}</span>
          <span>👀 {{ post.views }}k</span>
        </div>
      </div>
      <h2 class="text-2xl lg:text-3xl font-bold mb-3 leading-tight">
        {{ post.title }}
      </h2>
      <p class="text-xs lg:text-sm opacity-80">
        {{ post.date }} · {{ post.user_nickname || '빵순이🥐' }}
      </p>
    </header>

    <!-- 본문 -->
    <main class="p-6 lg:p-8 space-y-6">
      <p class="text-sm lg:text-base text-gray-800 leading-relaxed whitespace-pre-line">
        {{ post.content }}
      </p>

      <!-- 좋아요 버튼 -->
      <div class="flex items-center gap-4 pt-4 border-t border-gray-100">
        <button
          @click="handleLike"
          :disabled="isLiking"
          :class="[
            'flex items-center gap-2 px-5 py-2.5 rounded-full font-semibold text-sm transition-all',
            isLiked
              ? 'bg-red-50 text-red-600 hover:bg-red-100'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
            isLiking ? 'opacity-50 cursor-not-allowed' : ''
          ]"
        >
          <span class="text-lg">{{ isLiked ? '❤️' : '🤍' }}</span>
          <span>좋아요 {{ localLikes }}</span>
        </button>
      </div>

      <section v-if="post.storeName" class="p-5 bg-teal-50 rounded-2xl text-sm lg:text-base text-gray-700">
        <h3 class="font-bold text-teal-900 mb-2">🥯 빵집 정보</h3>
        <p>{{ post.storeName }}</p>
      </section>
    </main>

    <!-- 댓글 아코디언 -->
    <section class="border-t border-gray-100">
      <!-- 토글 헤더 -->
      <button
        type="button"
        class="w-full flex items-center justify-between px-6 lg:px-8 py-4 text-sm lg:text-base font-semibold text-left hover:bg-gray-50 transition-colors"
        @click="toggleComments"
      >
        <span class="flex items-center gap-2">
          💬 댓글 {{ commentsCount }}
        </span>
        <span class="flex items-center gap-1 text-xs text-gray-500 select-none">
          <span v-if="isCommentsOpen">닫기</span>
          <span v-else>펼치기</span>
          <svg
            :class="['w-4 h-4 transition-transform', isCommentsOpen ? 'rotate-180' : 'rotate-0']"
            viewBox="0 0 20 20"
            fill="none"
          >
            <path
              d="M5 8l5 5 5-5"
              stroke="currentColor"
              stroke-width="1.6"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </span>
      </button>

      <!-- 아코디언 본문 -->
      <Transition name="comments">
        <div
          v-if="isCommentsOpen"
          class="px-6 lg:px-8 pb-6 lg:pb-8 space-y-4 bg-gray-50"
        >
          <!-- 댓글 리스트 -->
          <div class="space-y-3 max-h-96 overflow-y-auto">
            <div v-for="comment in comments" :key="comment.id" class="space-y-2">
              <!-- 댓글 -->
              <div class="flex gap-3 p-3 bg-white rounded-xl shadow-sm shadow-black/5">
                <div class="w-9 h-9 rounded-full bg-teal-100 flex items-center justify-center flex-shrink-0">
                  <span class="text-xs font-bold">🍞</span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-semibold mb-1">{{ comment.user_nickname }}</p>
                  <p class="text-xs text-gray-700 whitespace-pre-line">{{ comment.content }}</p>
                  <div class="flex items-center gap-3 mt-1">
                    <p class="text-[11px] text-gray-400">
                      {{ formatDate(comment.created_at) }}
                    </p>
                    <button
                      @click="startReply(comment)"
                      class="text-[11px] text-teal-700 hover:underline"
                    >
                      답글
                    </button>
                  </div>
                </div>
              </div>

              <!-- 답글들 -->
              <div v-if="comment.replies && comment.replies.length" class="ml-8 space-y-2">
                <div
                  v-for="reply in comment.replies"
                  :key="reply.id"
                  class="flex gap-3 p-3 bg-white rounded-xl shadow-sm shadow-black/5"
                >
                  <div class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                    <span class="text-xs font-bold">🥐</span>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs font-semibold mb-1">{{ reply.user_nickname }}</p>
                    <p class="text-xs text-gray-700 whitespace-pre-line">{{ reply.content }}</p>
                    <p class="text-[11px] text-gray-400 mt-1">
                      {{ formatDate(reply.created_at) }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- 답글 작성 폼 -->
              <div v-if="replyingTo?.id === comment.id" class="ml-8">
                <textarea
                  v-model="replyContent"
                  rows="2"
                  class="w-full text-xs lg:text-sm p-3 border border-gray-200 rounded-2xl resize-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
                  placeholder="답글을 입력하세요"
                ></textarea>
                <div class="flex justify-end gap-2 mt-2">
                  <button
                    type="button"
                    class="px-3 py-1 text-[11px] text-gray-500 hover:text-gray-700"
                    @click="cancelReply"
                  >
                    취소
                  </button>
                  <button
                    type="button"
                    @click="submitReply"
                    :disabled="!replyContent.trim() || isSubmittingReply"
                    class="px-4 py-1.5 text-[11px] lg:text-xs font-bold rounded-xl bg-teal-900 text-white hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {{ isSubmittingReply ? '등록 중...' : '답글 달기' }}
                  </button>
                </div>
              </div>
            </div>

            <p v-if="!comments.length" class="text-center text-sm text-gray-400 py-6">
              아직 댓글이 없습니다. 첫 번째 댓글을 남겨보세요!
            </p>
          </div>

          <!-- 댓글 입력 -->
          <div class="mt-4">
            <textarea
              v-model="newComment"
              rows="2"
              class="w-full text-xs lg:text-sm p-3 border border-gray-200 rounded-2xl resize-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
              placeholder="빵 이야기 남겨보세요 :)"
            ></textarea>
            <div class="flex justify-end gap-2 mt-2">
              <button
                type="button"
                class="px-3 py-1 text-[11px] text-gray-500 hover:text-gray-700"
                @click="isCommentsOpen = false"
              >
                취소
              </button>
              <button
                type="button"
                @click="submitComment"
                :disabled="!newComment.trim() || isSubmittingComment"
                class="px-4 py-1.5 text-[11px] lg:text-xs font-bold rounded-xl bg-teal-900 text-white hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {{ isSubmittingComment ? '등록 중...' : '댓글 달기' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  post: { type: Object, required: true },
  isCommentsOpen: { type: Boolean, default: false },
  newComment: { type: String, default: '' },
})

const emit = defineEmits(['update:isCommentsOpen', 'update:newComment', 'likeUpdated'])

const authStore = useAuthStore()
const localLikes = ref(props.post.likes)
const isLiked = ref(false)
const isLiking = ref(false)

// 댓글 관련
const comments = ref([])
const commentsCount = ref(props.post.comments || 0)
const isCommentsOpen = ref(props.isCommentsOpen)
const newComment = ref('')
const isSubmittingComment = ref(false)

// 답글 관련
const replyingTo = ref(null)
const replyContent = ref('')
const isSubmittingReply = ref(false)

// post의 like_user_ids를 확인하여 초기 좋아요 상태 설정
watch(() => props.post, (newPost) => {
  if (newPost) {
    localLikes.value = newPost.likes
    if (authStore.isAuthenticated && newPost.like_user_ids) {
      isLiked.value = newPost.like_user_ids.includes(authStore.user?.pk)
    }
  }
}, { immediate: true })

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000) // 초 단위

  if (diff < 60) return '방금 전'
  if (diff < 3600) return `${Math.floor(diff / 60)}분 전`
  if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`
  if (diff < 604800) return `${Math.floor(diff / 86400)}일 전`

  return date.toLocaleDateString('ko-KR')
}

const toggleComments = async () => {
  isCommentsOpen.value = !isCommentsOpen.value
  if (isCommentsOpen.value && comments.value.length === 0) {
    await fetchComments()
  }
}

const fetchComments = async () => {
  try {
    const res = await apiClient.get(`/reviews/${props.post.id}/comments/`)
    comments.value = res.data
    commentsCount.value = res.data.reduce((count, comment) => {
      return count + 1 + (comment.replies ? comment.replies.length : 0)
    }, 0)
  } catch (error) {
    console.error('댓글 불러오기 실패:', error)
  }
}

const submitComment = async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }

  if (!newComment.value.trim()) return

  try {
    isSubmittingComment.value = true
    await apiClient.post(`/reviews/${props.post.id}/comments/`, {
      content: newComment.value
    })
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    console.error('댓글 작성 실패:', error)
    alert('댓글 작성 중 오류가 발생했습니다.')
  } finally {
    isSubmittingComment.value = false
  }
}

const startReply = (comment) => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }
  replyingTo.value = comment
  replyContent.value = ''
}

const cancelReply = () => {
  replyingTo.value = null
  replyContent.value = ''
}

const submitReply = async () => {
  if (!replyContent.value.trim()) return

  try {
    isSubmittingReply.value = true
    await apiClient.post(`/reviews/comments/${replyingTo.value.id}/reply/`, {
      content: replyContent.value
    })
    replyContent.value = ''
    replyingTo.value = null
    await fetchComments()
  } catch (error) {
    console.error('답글 작성 실패:', error)
    alert('답글 작성 중 오류가 발생했습니다.')
  } finally {
    isSubmittingReply.value = false
  }
}

const handleLike = async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }

  if (isLiking.value) return

  try {
    isLiking.value = true
    const response = await apiClient.post(`/reviews/${props.post.id}/like/`)

    if (response.data.status === 'like added') {
      isLiked.value = true
      localLikes.value += 1
    } else if (response.data.status === 'like removed') {
      isLiked.value = false
      localLikes.value -= 1
    }

    emit('likeUpdated', { id: props.post.id, likes: localLikes.value })
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
    alert('좋아요 처리 중 오류가 발생했습니다.')
  } finally {
    isLiking.value = false
  }
}
</script>

<style scoped>
.comments-enter-active,
.comments-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.comments-enter-from,
.comments-leave-to {
  max-height: 0;
  opacity: 0;
}
.comments-enter-to,
.comments-leave-from {
  max-height: 800px;
  opacity: 1;
}
</style>
