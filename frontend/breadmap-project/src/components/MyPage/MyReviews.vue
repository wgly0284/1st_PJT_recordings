<template>
  <div class="min-h-screen bg-gray-50/50 pt-32 pb-32">
    <div class="max-w-7xl mx-auto px-6 space-y-8">
      <!-- 헤더 -->
      <div class="text-center lg:text-left">
        <h1
          class="text-4xl md:text-5xl font-playfair font-bold bg-gradient-to-r from-teal-900 to-teal-700 bg-clip-text text-transparent mb-2"
        >
          MY REVIEWS
        </h1>
        <p class="text-xl text-gray-600">
          내가 남긴 빵집 리뷰들을 한눈에 모아보는 공간
        </p>
      </div>

      <!-- 데스크톱 레이아웃 -->
      <div class="hidden lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- 리스트 영역 -->
        <section class="space-y-6 lg:col-span-2">
          <h2 class="text-sm font-bold text-gray-500 tracking-widest">
            REVIEW LIST
          </h2>

          <div class="space-y-4">
            <article
              v-for="review in myReviews"
              :key="review.id"
              @click="selectReview(review)"
              :class="[
                'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
                selectedReview && selectedReview.id === review.id ? 'ring-2 ring-teal-500 bg-teal-50' : '',
              ]"
            >
              <div class="flex items-center justify-between mb-2 text-xs text-gray-400">
                <span class="font-medium">
                  {{ review.store?.name || review.bakeryName || '알 수 없는 가게' }}
                </span>
                <span v-if="review.created_at">
                  {{ formatDate(review.created_at) }}
                </span>
              </div>
              <h3
                class="text-lg font-bold text-gray-900 mb-1 line-clamp-1 group-hover:text-teal-900 transition-colors"
              >
                {{ review.title || '제목 없는 리뷰' }}
              </h3>
              <p class="text-sm text-gray-600 line-clamp-2">
                {{ review.content }}
              </p>
              <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
                <span class="text-yellow-500 font-semibold">
                  ★ {{ review.rating ?? '-' }}/5
                </span>
                <button
                  type="button"
                  class="inline-flex items-center gap-1 text-teal-700"
                >
                  자세히 보기
                </button>
              </div>
            </article>

            <p
              v-if="!myReviews.length"
              class="text-center text-sm text-gray-500 py-10"
            >
              아직 작성한 리뷰가 없습니다. 첫 번째 빵집 후기를 남겨보세요!
            </p>
          </div>
        </section>

        <!-- 상세 영역 + 작성 버튼 -->
        <section class="lg:col-span-1 space-y-4">
          <!-- 상세 카드 -->
          <div
            v-if="selectedReview"
            class="bg-white rounded-3xl border border-gray-100 p-6 shadow-sm space-y-3"
          >
            <h3 class="text-sm font-bold text-gray-500 tracking-widest mb-1">
              REVIEW DETAIL
            </h3>
            <p class="text-xs text-gray-400">
              {{ selectedReview.store?.name || selectedReview.bakeryName || '알 수 없는 가게' }}
            </p>
            <h2 class="text-xl font-bold text-gray-900 mb-1">
              {{ selectedReview.title || '제목 없는 리뷰' }}
            </h2>
            <div class="flex items-center gap-2 text-sm text-gray-500 mb-3">
              <span class="text-yellow-500 font-semibold">
                ★ {{ selectedReview.rating ?? '-' }}/5
              </span>
              <span v-if="selectedReview.created_at">
                · {{ formatDate(selectedReview.created_at) }}
              </span>
            </div>
            <p class="text-sm text-gray-700 whitespace-pre-line leading-relaxed">
              {{ selectedReview.content }}
            </p>
          </div>

          <!-- 새 리뷰 작성 카드 -->
          <div class="bg-white rounded-3xl border border-gray-100 p-6 shadow-sm">
            <h3 class="text-lg font-bold text-teal-900 mb-2">새 리뷰 작성</h3>
            <p class="text-sm text-gray-600 mb-4">
              최근 방문한 빵집의 맛과 분위기를 기록해두면,
              나중에 빵지순례 루트 짤 때 큰 도움이 돼요.
            </p>
            <router-link
              :to="{ name: 'newReview' }"
              class="inline-flex items-center justify-center w-full px-6 py-3 bg-teal-900 text-white text-sm font-bold
                     rounded-full hover:bg-teal-800 transition-all duration-300"
            >
              리뷰 작성하기
            </router-link>
          </div>

          <div class="bg-teal-900 text-white rounded-3xl p-6 shadow-sm space-y-2">
            <h4 class="text-sm font-semibold tracking-widest text-teal-100">
              TIP
            </h4>
            <p class="text-sm">
              한 줄 평 + 상세 설명 + 별점까지 남겨두면,
              다른 빵덕후들에게도 큰 도움이 됩니다.
            </p>
          </div>
        </section>
      </div>

      <!-- 모바일 / 태블릿 레이아웃 -->
      <div class="lg:hidden space-y-6">
        <section class="space-y-4">
          <h2 class="text-sm font-bold text-gray-500 tracking-widest text-center">
            MY REVIEWS
          </h2>

          <article
            v-for="review in myReviews"
            :key="review.id"
            @click="selectReview(review)"
            :class="[
              'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
              selectedReview && selectedReview.id === review.id ? 'ring-2 ring-teal-500 bg-teal-50' : '',
            ]"
          >
            <div class="flex items-center justify-between mb-2 text-xs text-gray-400">
              <span class="font-medium">
                {{ review.store?.name || review.bakeryName || '알 수 없는 가게' }}
              </span>
              <span v-if="review.created_at">
                {{ formatDate(review.created_at) }}
              </span>
            </div>
            <h3
              class="text-base font-bold text-gray-900 mb-1 line-clamp-1 group-hover:text-teal-900 transition-colors"
            >
              {{ review.title || '제목 없는 리뷰' }}
            </h3>
            <p class="text-sm text-gray-600 line-clamp-2">
              {{ review.content }}
            </p>
            <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
              <span class="text-yellow-500 font-semibold">
                ★ {{ review.rating ?? '-' }}/5
              </span>
              <button
                type="button"
                class="inline-flex items-center gap-1 text-teal-700"
              >
                자세히 보기
              </button>
            </div>

            <!-- 모바일 상세: 선택된 카드 아래에 전체 내용 표시 -->
            <div
              v-if="selectedReview && selectedReview.id === review.id"
              class="mt-4 border-t border-gray-100 pt-3 text-sm text-gray-700 whitespace-pre-line"
            >
              {{ review.content }}
            </div>
          </article>

          <p
            v-if="!myReviews.length"
            class="text-center text-sm text-gray-500 py-10"
          >
            아직 작성한 리뷰가 없습니다. 첫 번째 빵집 후기를 남겨보세요!
          </p>
        </section>

        <section class="pt-2">
          <router-link
            :to="{ name: 'newReview' }"
            class="inline-flex items-center justify-center w-full px-6 py-3 bg-teal-900 text-white text-sm font-bold
                   rounded-full hover:bg-teal-800 transition-all duration-300"
          >
            리뷰 작성하기
          </router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/axios'

const myReviews = ref([])
const selectedReview = ref(null)

// 개발용 목데이터
const mockReviews = [
  {
    id: 1,
    title: '성수 어니언 베이글 존맛',
    bakeryName: 'Onion Bagle',
    content: '바삭+쫄깃 조합 최고였어요. 크림치즈도 넉넉하게 들어있어서 만족!',
    rating: 5,
    created_at: '2025-12-20',
  },
  {
    id: 2,
    title: '제주 사워도우 빵지순례',
    bakeryName: 'Wheat & Grain',
    content: '산미가 은은하고 속은 촉촉해서 계속 손이 갔던 사워도우입니다.',
    rating: 4,
    created_at: '2025-12-18',
  },
]

const fetchMyReviews = async () => {
  try {
    const res = await apiClient.get('/reviews/my/')
    myReviews.value = res.data

    if (import.meta.env.DEV && myReviews.value.length === 0) {
      myReviews.value = mockReviews
    }

    if (myReviews.value.length > 0) {
      selectedReview.value = myReviews.value[0]
    }
  } catch (error) {
    console.error('Failed to fetch my reviews:', error)
    if (import.meta.env.DEV) {
      myReviews.value = mockReviews
      selectedReview.value = mockReviews[0]
    }
  }
}

const selectReview = (review) => {
  selectedReview.value = review
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


import { useRoute } from 'vue-router'

const route = useRoute()

onMounted(() => {
  fetchMyReviews().then(() => {
    const selectedId = Number(route.query.selectedId)
    if (selectedId && myReviews.value.length) {
      const found = myReviews.value.find(r => r.id === selectedId)
      if (found) selectedReview.value = found
    }
  })
})


</script>
