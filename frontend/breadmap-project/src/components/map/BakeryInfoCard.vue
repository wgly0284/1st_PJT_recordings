<script setup>
import { ref, onMounted } from 'vue'
import {
  X,
  Star,
  MapPin,
  ChevronRight,
  Phone,
  Clock,
  Utensils,
  Sparkles,
  Heart,
  MessageCircle,
  ThumbsUp,
} from 'lucide-vue-next'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// 부모로부터 선택된 빵집 정보와 닫기 이벤트를 받습니다.
const props = defineProps({
  bakery: { type: Object, required: true },
})

const emit = defineEmits(['close', 'view-detail', 'write-review'])

const authStore = useAuthStore()
const aiSummary = ref(null)
const isAiLoading = ref(false)
const isBookmarked = ref(false)
const storeReviews = ref([])
const isReviewsLoading = ref(false)
const showReviews = ref(false)
const activeTab = ref('menu') // 'menu' 또는 'review'

// 이미지 에러 처리
const handleImageError = (e) => {
  e.target.src =
    'https://via.placeholder.com/600x400/f5f5f5/8B4513?text=Bakery'
}

// AI 요약 생성 함수
const generateAISummary = async () => {
  if (isAiLoading.value) return
  isAiLoading.value = true

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/stores/${props.bakery.id}/ai-summary/`,
    )
    aiSummary.value = {
      text: response.data.summary,
      keywords: response.data.keywords,
    }
  } catch (error) {
    console.error('AI 요약 실패:', error)
    aiSummary.value = {
      text: '아직 분석할 리뷰가 충분하지 않아요 🥲',
      keywords: ['데이터부족'],
    }
  } finally {
    isAiLoading.value = false
  }
}

// 북마크 토글 함수
const toggleBookmark = async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }

  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/stores/${props.bakery.id}/bookmark/`,
      {},
      { headers: { Authorization: `Token ${authStore.token}` } },
    )

    if (response.data.status === 'bookmark added') {
      isBookmarked.value = true
    } else {
      isBookmarked.value = false
    }
  } catch (error) {
    console.error('북마크 실패:', error)
  }
}

// 가게 리뷰 조회 함수
const fetchStoreReviews = async () => {
  if (storeReviews.value.length > 0) return
  if (isReviewsLoading.value) return
  isReviewsLoading.value = true

  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/stores/${props.bakery.id}/reviews/`,
    )
    storeReviews.value = response.data
  } catch (error) {
    console.error('리뷰 조회 실패:', error)
  } finally {
    isReviewsLoading.value = false
  }
}

// 탭 변경 함수
const changeTab = (tab) => {
  activeTab.value = tab
  if (tab === 'review' && storeReviews.value.length === 0) {
    fetchStoreReviews()
  }
}

// 북마크 상태 확인
const checkBookmarkStatus = async () => {
  if (!authStore.isAuthenticated) return

  try {
    const response = await axios.get(
      'http://127.0.0.1:8000/stores/my_bookmarks/',
      {
        headers: { Authorization: `Token ${authStore.token}` },
      },
    )
    const bookmarkedIds = response.data.map((store) => store.id)
    isBookmarked.value = bookmarkedIds.includes(props.bakery.id)
  } catch (error) {
    console.error('북마크 상태 확인 실패:', error)
  }
}

// 리뷰 작성 페이지로 이동
const goToWriteReview = () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }
  emit('write-review', props.bakery.id)
}

onMounted(() => {
  checkBookmarkStatus()
})
</script>

<template>
  <div
    class="h-full flex flex-col bg-white animate-slide-in shadow-lg border-l border-gray-100"
  >
    <!-- 1. 헤더 (이미지 및 닫기 버튼) -->
    <div
      class="relative w-full h-56 bg-gray-100 shrink-0 overflow-hidden"
    >
      <!-- ✅ 백엔드 preview_image 사용 -->
      <img
        :src="bakery.preview_image"
        @error="handleImageError"
        class="w-full h-full object-cover transition-transform hover:scale-105 duration-700"
        alt="bakery image"
      />

      <!-- 닫기 버튼 -->
      <button
        @click="$emit('close')"
        class="absolute top-4 right-4 w-8 h-8 bg-black/40 hover:bg-black/60 rounded-full flex items-center justify-center text-white transition-colors backdrop-blur-sm"
      >
        <X class="w-5 h-5" />
      </button>

      <!-- 북마크 버튼 -->
      <button
        @click="toggleBookmark"
        class="absolute top-4 right-14 w-8 h-8 bg-black/40 hover:bg-black/60 rounded-full flex items-center justify-center text-white transition-all backdrop-blur-sm group"
        :class="{
          'bg-red-500/80 hover:bg-red-600/80': isBookmarked,
        }"
      >
        <Heart
          class="w-5 h-5 transition-all"
          :class="isBookmarked ? 'fill-white' : 'fill-transparent'"
        />
      </button>

      <!-- 평점 배지 (이미지 위 오버레이) -->
      <div class="absolute bottom-4 left-4 flex gap-2">
        <div
          class="bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs font-bold text-orange-600 shadow-sm flex items-center gap-1"
        >
          <Star class="w-3.5 h-3.5 fill-current" />
          {{ bakery.rating ? Number(bakery.rating).toFixed(1) : '0.0' }}
        </div>
        <div
          v-if="bakery.tags && bakery.tags.length > 0"
          class="bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs font-bold text-[#1D4E45] shadow-sm"
        >
          #{{ bakery.tags[0] }}
        </div>
      </div>
    </div>

    <!-- 2. 본문 정보 -->
    <div class="p-6 flex-1 flex flex-col overflow-y-auto hide-scrollbar">
      <div class="mb-5">
        <h2
          class="text-2xl font-bold text-[#1D4E45] mb-2 font-serif leading-tight"
        >
          {{ bakery.name }}
        </h2>
        <div class="flex flex-wrap gap-1.5">
          <span
            v-for="tag in bakery.tags"
            :key="tag"
            class="text-[10px] px-2 py-0.5 bg-gray-100 text-gray-500 rounded-md"
            >#{{ tag }}</span
          >
        </div>
      </div>

      <div
        class="space-y-3 mb-6 bg-gray-50 p-4 rounded-2xl border border-gray-100"
      >
        <div class="flex items-start gap-3 text-sm text-gray-600">
          <MapPin class="w-4 h-4 mt-0.5 text-[#1D4E45]" />
          <span class="leading-snug">{{ bakery.address }}</span>
        </div>

        <!-- 영업시간 -->
        <div class="flex items-center gap-3 text-sm text-gray-600">
          <Clock class="w-4 h-4 text-[#1D4E45]" />
          <span>{{ bakery.business_hours || '10:00 ~ 20:00' }}</span>
        </div>

        <!-- 전화번호 -->
        <div
          v-if="bakery.contact"
          class="flex items-center gap-3 text-sm text-gray-600"
        >
          <Phone class="w-4 h-4 text-[#1D4E45]" />
          <span>{{ bakery.contact }}</span>
        </div>
      </div>

      <!-- AI 요약 섹션 -->
      <div class="mb-6">
        <h3
          class="text-sm font-bold text-teal-800 mb-3 flex items-center gap-1.5"
        >
          <Sparkles class="w-4 h-4 text-purple-500" /> AI 리뷰 요약
        </h3>

        <div v-if="!aiSummary" class="text-center">
          <button
            @click="generateAISummary"
            class="w-full py-2 bg-purple-50 border border-purple-100 rounded-xl text-xs font-bold text-purple-600 hover:bg-purple-100 transition-colors flex items-center justify-center gap-2"
            :disabled="isAiLoading"
          >
            <span
              v-if="isAiLoading"
              class="animate-spin w-3 h-3 border-2 border-purple-600 border-t-transparent rounded-full"
            ></span>
            <span v-else>✨ AI 분석 보기</span>
          </button>
        </div>

        <div
          v-else
          class="bg-purple-50 p-4 rounded-xl border border-purple-100 animate-slide-in"
        >
          <p
            class="text-xs text-gray-700 leading-relaxed mb-2 line-clamp-3"
          >
            "{{ aiSummary.text }}"
          </p>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="k in aiSummary.keywords"
              :key="k"
              class="text-[10px] bg-white text-purple-600 px-2 py-0.5 rounded border border-purple-200"
              >#{{ k }}</span
            >
          </div>
        </div>
      </div>

      <!-- 탭 메뉴 (대표 메뉴 / 리뷰) -->
      <div class="mb-4">
        <!-- 탭 버튼 -->
        <div class="flex gap-2 mb-4 border-b border-gray-200">
          <button
            @click="changeTab('menu')"
            class="flex-1 pb-3 text-sm font-bold transition-all relative"
            :class="
              activeTab === 'menu'
                ? 'text-orange-600'
                : 'text-gray-400 hover:text-gray-600'
            "
          >
            <Utensils class="w-4 h-4 inline mr-1" />
            대표 메뉴
            <div
              v-if="activeTab === 'menu'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-orange-600 rounded-t-full"
            ></div>
          </button>
          <button
            @click="changeTab('review')"
            class="flex-1 pb-3 text-sm font-bold transition-all relative"
            :class="
              activeTab === 'review'
                ? 'text-teal-600'
                : 'text-gray-400 hover:text-gray-600'
            "
          >
            <MessageCircle class="w-4 h-4 inline mr-1" />
            리뷰
            <div
              v-if="activeTab === 'review'"
              class="absolute bottom-0 left-0 right-0 h-0.5 bg-teal-600 rounded-t-full"
            ></div>
          </button>
        </div>

        <!-- 대표 메뉴 탭 -->
        <div v-if="activeTab === 'menu'">
          <div
            v-if="bakery.menu && bakery.menu.length > 0"
            class="space-y-2"
          >
            <div
              v-for="item in bakery.menu.slice(0, 5)"
              :key="item.id || item.name"
              class="flex items-center justify-between p-3 bg-white border border-gray-100 rounded-xl hover:border-orange-100 transition-colors"
            >
              <div class="flex items-center gap-3 overflow-hidden">
                <div
                  class="w-10 h-10 rounded-lg bg-gray-100 shrink-0 overflow-hidden"
                >
                  <img
                    v-if="item.image_url"
                    :src="item.image_url"
                    class="w-full h-full object-cover"
                  />
                  <div
                    v-else
                    class="w-full h-full flex items-center justify-center text-base"
                  >
                    🍞
                  </div>
                </div>
                <span
                  class="text-sm text-gray-700 truncate font-medium"
                  >{{ item.name }}</span
                >
              </div>
              <span
                class="text-xs font-bold text-orange-600 shrink-0"
                >{{ Number(item.price).toLocaleString() }}원</span
              >
            </div>
            <div
              v-if="bakery.menu.length > 5"
              class="text-center text-xs text-gray-400 mt-2"
            >
              + {{ bakery.menu.length - 5 }}개의 메뉴 더보기
            </div>
          </div>

          <div
            v-else
            class="text-center py-8 bg-gray-50 rounded-xl border border-dashed border-gray-200"
          >
            <p class="text-xs text-gray-400">등록된 대표 메뉴가 없어요 🥐</p>
          </div>
        </div>

        <!-- 리뷰 탭 -->
        <div v-if="activeTab === 'review'">
          <!-- 리뷰 로딩 -->
          <div v-if="isReviewsLoading" class="text-center py-8">
            <div
              class="animate-spin w-6 h-6 border-2 border-teal-600 border-t-transparent rounded-full mx-auto"
            ></div>
          </div>

          <!-- 리뷰 목록 -->
          <div
            v-else-if="storeReviews.length > 0"
            class="space-y-3 max-h-96 overflow-y-auto hide-scrollbar"
          >
            <div
              v-for="review in storeReviews"
              :key="review.id"
              class="bg-white border border-gray-200 rounded-xl p-4 hover:border-teal-200 transition-colors"
            >
              <!-- 리뷰 헤더 -->
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div
                    class="w-8 h-8 bg-teal-100 rounded-full flex items-center justify-center"
                  >
                    <span
                      class="text-xs font-bold text-teal-700"
                      >{{ review.user_nickname?.charAt(0) || 'U' }}</span
                    >
                  </div>
                  <div>
                    <p class="text-sm font-bold text-gray-800">
                      {{ review.user_nickname || '익명' }}
                    </p>
                    <p class="text-[10px] text-gray-400">
                      {{
                        new Date(
                          review.created_at,
                        ).toLocaleDateString()
                      }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center gap-1">
                  <Star
                    class="w-4 h-4 fill-orange-400 text-orange-400"
                  />
                  <span
                    class="text-sm font-bold text-orange-600"
                    >{{ review.rating }}</span
                  >
                </div>
              </div>

              <!-- 리뷰 내용 -->
              <p
                class="text-sm text-gray-700 leading-relaxed mb-2 line-clamp-3"
              >
                {{ review.content }}
              </p>

              <!-- 리뷰 이미지 -->
              <div v-if="review.photo_urls" class="mb-2">
                <img
                  :src="`http://127.0.0.1:8000${review.photo_urls}`"
                  class="w-full h-32 object-cover rounded-lg"
                />
              </div>

              <!-- 키워드 태그 -->
              <div
                v-if="review.taste_tags"
                class="flex flex-wrap gap-1 mb-2"
              >
                <span
                  v-for="tag in review.taste_tags.split(',')"
                  :key="tag"
                  class="text-[10px] px-2 py-0.5 bg-teal-50 text-teal-700 rounded-full border border-teal-200"
                  >{{ tag.trim() }}</span
                >
              </div>

              <!-- 좋아요 & 댓글 -->
              <div class="flex items-center gap-4 text-xs text-gray-500">
                <div class="flex items-center gap-1">
                  <ThumbsUp class="w-3 h-3" />
                  <span>{{ review.like_users?.length || 0 }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <MessageCircle class="w-3 h-3" />
                  <span>{{ review.comments_count || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- 리뷰 작성 버튼 -->
            <button
              @click="goToWriteReview"
              class="w-full mt-2 py-2.5 bg-teal-50 border border-teal-200 rounded-xl text-sm font-bold text-teal-700 hover:bg-teal-100 transition-colors"
            >
              + 이 가게 리뷰 남기기
            </button>
          </div>

          <!-- 리뷰 없음 -->
          <div
            v-else
            class="text-center py-8 bg-gray-50 rounded-xl border border-dashed border-gray-200"
          >
            <p class="text-xs text-gray-400 mb-3">
              아직 작성된 리뷰가 없어요 😢
            </p>
            <button
              @click="goToWriteReview"
              class="text-xs text-teal-600 font-bold hover:underline"
            >
              첫 리뷰 작성하기 →
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. 하단 고정 버튼 -->
    <div class="p-5 border-t border-gray-100 bg-white shrink-0">
      <button
        @click="$emit('view-detail', bakery.id)"
        class="w-full py-4 bg-[#1D4E45] text-white rounded-xl font-bold hover:bg-[#153e35] transition-all flex items-center justify-center gap-2 shadow-lg shadow-teal-900/10 active:scale-[0.98] group"
      >
        상세보기
        <ChevronRight
          class="w-4 h-4 group-hover:translate-x-1 transition-transform"
        />
      </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
.animate-slide-in {
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
