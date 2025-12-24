<script setup>
import { ref, watch, computed } from 'vue'
import apiClient from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  post: { type: Object, required: true },
  isCommentsOpen: { type: Boolean, default: false },
  newComment: { type: String, default: '' },
})

const emit = defineEmits(['update:isCommentsOpen', 'update:newComment', 'likeUpdated', 'close'])

const authStore = useAuthStore()

// 화면에 표시할 게시글 데이터 (Props + API Fetch 병합용)
const postData = ref({ ...props.post })

const localLikes = ref(props.post.likes)
const isLiked = ref(false)
const isLiking = ref(false)
const isFollowed = ref(false)
const isFollowing = ref(false)
const comments = ref([])
const commentsCount = ref(props.post.comments || 0)
const isCommentsOpen = ref(props.isCommentsOpen)
const newComment = ref('')
const isSubmittingComment = ref(false)
const replyingTo = ref(null)
const replyContent = ref('')
const isSubmittingReply = ref(false)
const isDeletingPost = ref(false)
const isDeletingComment = ref(null)

// 작성자 프로필 이미지 처리
const authorProfileImage = computed(() => {
  const img = postData.value.author_profile_image
  if (!img) return null
  if (img.startsWith('http')) return img
  return `http://127.0.0.1:8000${img}`
})

// ✅ 이미지 URL 처리 (상대 경로일 경우 백엔드 도메인 추가)
const imageUrl = computed(() => {
  const img = postData.value.image // postData에서 이미지 확인
  if (!img) return null
  if (img.startsWith('http')) return img
  // 백엔드 주소 (설정에 맞게 변경 가능)
  return `http://127.0.0.1:8000${img}`
})

// ✅ 게시글 상세 정보 가져오기 (이미지 누락 방지)
const fetchPostDetail = async () => {
  if (!props.post.id) return
  try {
    const res = await apiClient.get(`/community/${props.post.id}/`)
    const data = res.data

    console.log('post detail data:', data) // 🔍 확인용

    postData.value = {
      ...postData.value,
      ...data,
      image: data.image,
      // 🔥 여기 중요: 백엔드에서 author는 pk(int)로 오니까 그대로 사용
      author_id: data.author, 
      user_nickname: data.author_nickname,
      date: data.created_at?.slice(0, 10) || postData.value.date,
    }

    console.log('author_id set to:', postData.value.author_id) // 🔍 확인용

    if (data.like_count !== undefined) {
      localLikes.value = data.like_count
    }

    if (authStore.isAuthenticated && data.like_users) {
      isLiked.value = data.like_users.includes(authStore.user?.pk)
    }
  } catch (error) {
    console.error('게시글 상세 로드 실패:', error)
  }
}


const checkFollowStatus = async () => {
  if (!authStore.isAuthenticated || !postData.value.author_id) return
  try {
    const response = await apiClient.get('/accounts/following/')
    const followingIds = response.data.following?.map(u => u.id) || []
    isFollowed.value = followingIds.includes(postData.value.author_id)
  } catch (error) {
    console.error('팔로우 상태 확인 실패:', error)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  if (diff < 60) return '방금 전'
  if (diff < 3600) return `${Math.floor(diff / 60)}분 전`
  if (diff < 86400) return `${Math.floor(diff / 3600)}시간 전`
  if (diff < 604800) return `${Math.floor(diff / 86400)}일 전`
  return date.toLocaleDateString('ko-KR')
}

const toggleComments = async () => {
  isCommentsOpen.value = !isCommentsOpen.value
  emit('update:isCommentsOpen', isCommentsOpen.value) 
  if (isCommentsOpen.value && comments.value.length === 0) {
    await fetchComments()
  }
}

const fetchComments = async () => {
  try {
    const res = await apiClient.get(`/community/${props.post.id}/comments/`)
    comments.value = res.data
    commentsCount.value = res.data.reduce((count, comment) => {
      return count + 1 + (comment.replies ? comment.replies.length : 0)
    }, 0)
  } catch (error) {
    console.error('댓글 불러오기 실패:', error)
  }
}

const submitComment = async () => {
  if (!authStore.isAuthenticated) { alert('로그인이 필요합니다.'); return }
  if (!newComment.value.trim()) return
  try {
    isSubmittingComment.value = true
    await apiClient.post(`/community/${props.post.id}/comments/create/`, { content: newComment.value })
    emit('update:newComment', '') 
    newComment.value = '' 
    await fetchComments()
  } catch (error) { console.error('댓글 작성 실패:', error); alert('오류 발생') } finally { isSubmittingComment.value = false }
}

const startReply = (comment) => {
  if (!authStore.isAuthenticated) { alert('로그인이 필요합니다.'); return }
  replyingTo.value = comment; replyContent.value = ''
}
const cancelReply = () => { replyingTo.value = null; replyContent.value = '' }

const submitReply = async () => {
  if (!replyContent.value.trim()) return
  try {
    isSubmittingReply.value = true
    await apiClient.post(`/community/comments/${replyingTo.value.id}/reply/`, { content: replyContent.value })
    replyContent.value = ''; replyingTo.value = null; await fetchComments()
  } catch (error) { console.error('답글 작성 실패:', error); alert('오류 발생') } finally { isSubmittingReply.value = false }
}

const handleLike = async () => {
  if (!authStore.isAuthenticated) { alert('로그인이 필요합니다.'); return }
  if (isLiking.value) return
  try {
    isLiking.value = true
    const response = await apiClient.post(`/community/${props.post.id}/like/`)
    if (response.data.status === 'like added') { isLiked.value = true; localLikes.value += 1 }
    else { isLiked.value = false; localLikes.value -= 1 }
    emit('likeUpdated', { id: props.post.id, likes: localLikes.value })
  } catch (error) { console.error('좋아요 실패:', error) } finally { isLiking.value = false }
}

const handleFollow = async () => {
  if (!authStore.isAuthenticated) { alert('로그인이 필요합니다.'); return }
  if (isFollowing.value || !postData.value.author_id) return
  try {
    isFollowing.value = true
    const response = await apiClient.post(`/accounts/follow/${postData.value.author_id}/`)
    isFollowed.value = response.data.status === 'followed'
  } catch (error) { console.error('팔로우 실패:', error); alert('팔로우 처리 중 오류가 발생했습니다.') } finally { isFollowing.value = false }
}

const deletePost = async () => {
  if (!confirm('삭제하시겠습니까?')) return
  try { isDeletingPost.value = true; await apiClient.delete(`/community/${props.post.id}/`); window.location.reload() }
  catch (error) { console.error('삭제 실패:', error) } finally { isDeletingPost.value = false }
}

const deleteComment = async (id) => {
  if (!confirm('삭제하시겠습니까?')) return
  try { isDeletingComment.value = id; await apiClient.delete(`/community/comments/${id}/`); await fetchComments() }
  catch (error) { console.error('삭제 실패:', error) } finally { isDeletingComment.value = null }
}
const deleteReply = async (id, parentId) => {
    deleteComment(id)
}

// 작성자 프로필 페이지로 이동
const goToAuthorProfile = () => {
  console.log('goToAuthorProfile author_id:', postData.value.author_id)
  if (!postData.value.author_id) return
  if (authStore.user?.pk === postData.value.author_id) {
    window.location.href = '/mypage'
  } else {
    window.location.href = `/user/${postData.value.author_id}`
  }
}

// ✅ Watcher 수정: post 변경 시 데이터 초기화 및 상세 정보(이미지) Fetch
watch(
  () => props.post,
  (newPost) => {
    if (newPost) {
      postData.value = {
        ...newPost,
        // 목록 API에서 author가 안 들어오는 경우 대비용
        author_id: newPost.author ?? postData.value.author_id,
      }
      localLikes.value = newPost.likes

      if (authStore.isAuthenticated && newPost.like_user_ids) {
        isLiked.value = newPost.like_user_ids.includes(authStore.user?.pk)
      }

      fetchPostDetail()
      checkFollowStatus()
    }
  },
  { immediate: true }
)

</script>

<template>
  <div class="bg-white rounded-[32px] shadow-xl border border-[#D7CCC8] overflow-hidden relative h-full flex flex-col">
    
    <!-- 배경 질감 효과 (몽글몽글) -->
    <div class="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/paper.png')] pointer-events-none z-0"></div>

    <!-- 헤더 -->
    <header class="bg-gradient-to-r from-[#5D4037] to-[#8D6E63] text-white p-6 lg:p-8 relative z-10 shrink-0">
      <!-- 몽글몽글 구름 장식 -->
      <div class="absolute -top-10 -right-10 w-40 h-40 bg-[#FFFFFF]/10 rounded-full blur-2xl"></div>
      <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-[#FFFFFF]/10 rounded-full blur-2xl"></div>

      <!-- 뒤로가기 버튼 -->
      <button @click="$emit('close')" class="absolute top-4 left-5 z-20 flex items-center gap-1.5 text-sm text-white/70 hover:text-white transition-colors group">
        <div class="w-7 h-7 rounded-full border border-white/20 flex items-center justify-center group-hover:bg-white/10 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
        </div>
        <span class="font-bold">목록으로</span>
      </button>

      <div class="flex items-center justify-between mb-4 gap-3 flex-wrap relative z-10 mt-10">
        <span class="px-4 py-1.5 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold border border-white/10 shadow-sm">
          {{ postData.category }}
        </span>
        <div class="flex gap-4 text-xs lg:text-sm opacity-90 flex-wrap items-center font-medium">
          <span>❤️ {{ localLikes }}</span>
          <span>💬 {{ commentsCount }}</span>
          <span>👀 {{ postData.views || 0 }}k</span>
          <button
            v-if="postData.author_id && authStore.user?.pk === postData.author_id"
            @click="deletePost"
            :disabled="isDeletingPost"
            class="px-3 py-1.5 text-xs font-semibold text-white hover:bg-[#FF7043] border border-white/30 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isDeletingPost ? '삭제 중...' : '삭제' }}
          </button>
        </div>
      </div>
      <h2 class="text-2xl lg:text-3xl font-bold mb-3 leading-tight font-serif tracking-wide">
        {{ postData.title }}
      </h2>
      <div class="flex items-center justify-between relative z-10 gap-3">
        <div class="flex items-center gap-3">
          <!-- 작성자 프로필 이미지 -->
          <div
            @click="goToAuthorProfile"
            class="cursor-pointer hover:opacity-80 transition-opacity"
          >
            <div v-if="authorProfileImage" class="w-10 h-10 rounded-full overflow-hidden border-2 border-white/30 shadow-md">
              <img :src="authorProfileImage" alt="프로필" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center text-xl border-2 border-white/30 shadow-md">
              🧑‍🍳
            </div>
          </div>

          <!-- 작성자 정보 -->
          <div class="flex flex-col gap-1">
            <span
              @click="goToAuthorProfile"
              class="text-sm lg:text-base font-bold cursor-pointer hover:underline"
            >
              {{ postData.user_nickname || '익명 빵순이' }}
            </span>
            <span class="text-xs opacity-70">📅 {{ postData.date }}</span>
          </div>
        </div>

        <button
          v-if="postData.author_id && authStore.user?.pk !== postData.author_id"
          @click="handleFollow"
          :disabled="isFollowing"
          :class="[
            'px-4 py-1.5 rounded-full text-xs font-semibold transition-all shadow-sm shrink-0',
            isFollowed
              ? 'bg-[#EFEBE9] text-[#5D4037] hover:bg-[#D7CCC8]'
              : 'bg-[#FFCC80] text-[#5D4037] hover:bg-[#FFA726] border border-[#FFB74D]',
            isFollowing ? 'opacity-50 cursor-not-allowed' : ''
          ]"
        >
          {{ isFollowed ? '팔로잉' : '팔로우 +' }}
        </button>
      </div>
    </header>

    <!-- 본문 (스크롤 가능 영역) -->
    <div class="flex-1 overflow-y-auto custom-scroll relative z-10 bg-white">
      <main class="p-6 lg:p-8 space-y-6">
        <!-- 📷 이미지 표시 영역 (최대 높이 제한) -->
        <div v-if="imageUrl" class="rounded-2xl overflow-hidden shadow-sm mb-4 bg-gray-50 border border-gray-100 flex justify-center">
           <img :src="imageUrl" alt="게시글 이미지" class="max-w-full max-h-[450px] object-contain" />
        </div>

        <p class="text-sm lg:text-base text-[#4E342E] leading-relaxed whitespace-pre-line font-medium min-h-[100px]">
          {{ postData.content }}
        </p>

        <!-- 좋아요 버튼 -->
        <div class="flex items-center justify-center pt-6 border-t border-[#EFEBE9] border-dashed">
          <button
            @click="handleLike"
            :disabled="isLiking"
            :class="[
              'flex items-center gap-2 px-6 py-3 rounded-full font-bold text-sm transition-all shadow-md transform hover:-translate-y-0.5 active:translate-y-0',
              isLiked
                ? 'bg-[#FFAB91] text-[#BF360C] hover:bg-[#FF8A65]'
                : 'bg-[#EFEBE9] text-[#8D6E63] hover:bg-[#D7CCC8]',
              isLiking ? 'opacity-50 cursor-not-allowed' : ''
            ]"
          >
            <span class="text-xl animate-bounce">{{ isLiked ? '❤️' : '🤍' }}</span>
            <span>좋아요 {{ localLikes }}</span>
          </button>
        </div>

        <section v-if="postData.storeName" class="p-5 bg-[#FFF8E1] rounded-2xl text-sm lg:text-base text-[#5D4037] border border-[#FFE0B2] shadow-sm">
          <h3 class="font-bold text-[#F57C00] mb-2 flex items-center gap-2 font-serif text-lg">
            🥯 추천 빵집 정보
          </h3>
          <p>{{ postData.storeName }}</p>
        </section>
      </main>

      <!-- 댓글 아코디언 -->
      <section class="border-t border-[#D7CCC8]/50 bg-[#FAFAFA]">
        <!-- 토글 헤더 -->
        <button
          type="button"
          class="w-full flex items-center justify-between px-6 lg:px-8 py-4 text-sm lg:text-base font-bold text-[#5D4037] text-left hover:bg-[#F5F5F5] transition-colors"
          @click="toggleComments"
        >
          <span class="flex items-center gap-2">
            💬 수다 떨기 ({{ commentsCount }})
          </span>
          <span class="flex items-center gap-1 text-xs text-[#8D6E63] select-none bg-[#EFEBE9] px-2 py-1 rounded-lg">
            <span v-if="isCommentsOpen">접기</span>
            <span v-else>펼치기</span>
            <svg
              :class="['w-3 h-3 transition-transform', isCommentsOpen ? 'rotate-180' : 'rotate-0']"
              viewBox="0 0 20 20"
              fill="none"
            >
              <path d="M5 8l5 5 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
        </button>

        <!-- 아코디언 본문 -->
        <Transition name="comments">
          <div
            v-if="isCommentsOpen"
            class="px-6 lg:px-8 pb-6 lg:pb-8 space-y-4"
          >
            <!-- 댓글 리스트 -->
            <div class="space-y-3">
              <div v-for="comment in comments" :key="comment.id" class="space-y-2">
                <!-- 댓글 -->
                <div class="flex gap-3 p-4 bg-white rounded-2xl shadow-sm border border-[#E0E0E0]">
                  <div class="w-10 h-10 rounded-full bg-[#EFEBE9] flex items-center justify-center flex-shrink-0 text-lg border border-[#D7CCC8]">
                    🥐
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                      <p class="text-xs font-bold text-[#5D4037]">{{ comment.user_nickname }}</p>
                      <button
                        v-if="comment.author_id && authStore.user?.pk === comment.author_id"
                        @click="deleteComment(comment.id)"
                        :disabled="isDeletingComment === comment.id"
                        class="text-[10px] text-[#FF7043] hover:underline disabled:opacity-50 font-medium"
                      >
                        {{ isDeletingComment === comment.id ? '삭제...' : '삭제' }}
                      </button>
                    </div>
                    <p class="text-xs text-[#6D4C41] whitespace-pre-line leading-relaxed">{{ comment.content }}</p>
                    <div class="flex items-center gap-3 mt-2">
                      <p class="text-[10px] text-[#A1887F]">
                        {{ formatDate(comment.created_at) }}
                      </p>
                      <button
                        @click="startReply(comment)"
                        class="text-[10px] text-[#8D6E63] font-bold hover:text-[#5D4037] bg-[#EFEBE9] px-2 py-0.5 rounded transition-colors"
                      >
                        답글 달기
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 답글들 -->
                <div v-if="comment.replies && comment.replies.length" class="ml-8 space-y-2 border-l-2 border-[#D7CCC8] pl-4">
                  <div
                    v-for="reply in comment.replies"
                    :key="reply.id"
                    class="flex gap-3 p-3 bg-[#F9F7F2] rounded-xl border border-[#E0E0E0]"
                  >
                    <div class="w-8 h-8 rounded-full bg-[#FFE0B2] flex items-center justify-center flex-shrink-0 text-sm border border-[#FFCC80]">
                      🥨
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center justify-between mb-1">
                        <p class="text-xs font-bold text-[#5D4037]">{{ reply.user_nickname }}</p>
                        <button
                          v-if="reply.author_id && authStore.user?.pk === reply.author_id"
                          @click="deleteReply(reply.id, comment.id)"
                          :disabled="isDeletingComment === reply.id"
                          class="text-[10px] text-[#FF7043] hover:underline disabled:opacity-50"
                        >
                          삭제
                        </button>
                      </div>
                      <p class="text-xs text-[#6D4C41] whitespace-pre-line">{{ reply.content }}</p>
                      <p class="text-[10px] text-[#A1887F] mt-1">
                        {{ formatDate(reply.created_at) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 답글 작성 폼 -->
                <div v-if="replyingTo?.id === comment.id" class="ml-8 mt-2 p-3 bg-[#EFEBE9] rounded-xl">
                  <p class="text-[10px] text-[#8D6E63] mb-1 font-bold">↳ 답글 작성 중...</p>
                  <textarea
                    v-model="replyContent"
                    rows="2"
                    class="w-full text-xs p-2 border border-[#D7CCC8] rounded-lg resize-none focus:ring-2 focus:ring-[#8D6E63] focus:border-[#8D6E63] outline-none bg-white"
                    placeholder="따뜻한 답글을 남겨주세요."
                  ></textarea>
                  <div class="flex justify-end gap-2 mt-2">
                    <button
                      type="button"
                      class="px-3 py-1 text-[10px] text-[#8D6E63] hover:text-[#5D4037]"
                      @click="cancelReply"
                    >
                      취소
                    </button>
                    <button
                      type="button"
                      @click="submitReply"
                      :disabled="!replyContent.trim() || isSubmittingReply"
                      class="px-3 py-1 text-[10px] font-bold rounded-lg bg-[#8D6E63] text-white hover:bg-[#6D4C41] disabled:bg-[#BCAAA4]"
                    >
                      등록
                    </button>
                  </div>
                </div>
              </div>

              <p v-if="!comments.length" class="text-center text-sm text-[#A1887F] py-8 bg-[#F5F5F5] rounded-xl border border-dashed border-[#D7CCC8]">
                아직 조용하네요. 첫 번째 댓글을 구워보세요! 🧁
              </p>
            </div>

            <!-- 댓글 입력 -->
            <div class="mt-4 pt-4 border-t border-[#E0E0E0]">
              <div class="relative">
                  <textarea
                  v-model="newComment"
                  rows="2"
                  class="w-full text-sm p-4 pr-20 border border-[#D7CCC8] rounded-2xl resize-none focus:ring-2 focus:ring-[#8D6E63] focus:border-[#8D6E63] outline-none bg-white shadow-sm"
                  placeholder="오늘의 빵 이야기는 무엇인가요? :)"
                  ></textarea>
                  <button
                  type="button"
                  @click="submitComment"
                  :disabled="!newComment.trim() || isSubmittingComment"
                  class="absolute bottom-3 right-3 px-4 py-1.5 text-xs font-bold rounded-xl bg-[#5D4037] text-white hover:bg-[#4E342E] disabled:bg-[#BCAAA4] transition-colors shadow-sm"
                  >
                  전송
                  </button>
              </div>
            </div>
          </div>
        </Transition>
      </section>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');
.font-serif { font-family: 'Gaegu', cursive; }
.custom-scroll::-webkit-scrollbar { width: 6px; }
.custom-scroll::-webkit-scrollbar-thumb { background-color: #D7CCC8; border-radius: 10px; }
.custom-scroll::-webkit-scrollbar-track { background: transparent; }
.comments-enter-active, .comments-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); overflow: hidden; }
.comments-enter-from, .comments-leave-to { max-height: 0; opacity: 0; }
.comments-enter-to, .comments-leave-from { max-height: 800px; opacity: 1; }
</style>