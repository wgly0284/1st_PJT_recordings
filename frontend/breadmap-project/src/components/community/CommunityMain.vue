<template>
  <div class="min-h-screen bg-gray-50/50 pt-32 pb-32">
    <div class="max-w-7xl mx-auto px-6 space-y-8">
      <!-- 공통 헤더 -->
      <div class="text-center lg:text-left">
        <h1
          class="text-4xl md:text-5xl font-playfair font-bold bg-gradient-to-r from-teal-900 to-teal-700 bg-clip-text text-transparent mb-2"
        >
          COMMUNITY
        </h1>
        <p class="text-xl text-gray-600">
          빵을 사랑하는 사람들이 모이는 공간
        </p>
      </div>

      <!-- 모바일: 상세 보기 모드일 때 상단 뒤로가기 바 -->
      <div
        v-if="selectedPost && isMobile"
        class="flex items-center gap-3 py-2 border-b border-gray-200 lg:hidden"
      >
        <button
          type="button"
          class="flex items-center gap-1 text-sm text-teal-900 font-semibold"
          @click="backToList"
        >
          <span class="text-lg">←</span>
          <span>목록으로</span>
        </button>
        <span class="text-xs text-gray-400">/ {{ currentCategoryLabel }}</span>
      </div>

      <!-- 데스크톱 레이아웃 -->
      <div class="hidden lg:grid lg:grid-cols-3 lg:gap-8">
        <!-- 리스트 영역 -->
        <section
          :class="[
            'space-y-6',
            selectedPost ? 'lg:col-span-1' : 'lg:col-span-3',
          ]"
        >
          <!-- 카테고리 탭 -->
          <div class="flex flex-wrap justify-center lg:justify-start gap-3">
            <button
              v-for="cat in categories"
              :key="cat.value"
              @click="handleCategoryChange(cat.value)"
              :class="[
                'px-5 py-2 text-sm font-bold rounded-full border-2 transition-all duration-200 flex items-center gap-2',
                selectedCategory === cat.value
                  ? 'bg-teal-900 text-white border-teal-900'
                  : 'bg-white text-teal-900 border-teal-900/50 hover:border-teal-900 hover:bg-teal-50',
              ]"
            >
              <span class="w-2 h-2 rounded-full bg-current"></span>
              {{ cat.label }}
            </button>
          </div>

          <!-- 카테고리별 리스트 컴포넌트 -->
          <ChatterList
            v-if="selectedCategory === 'chatter'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <RecommendList
            v-else-if="selectedCategory === 'recommend'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <TipList
            v-else-if="selectedCategory === 'tip'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <HotList
            v-else
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
        </section>

        <!-- 상세 영역 (데스크톱) -->
        <Transition name="slide-detail">
          <section v-if="selectedPost" class="lg:col-span-2">
            <DetailCard
              :post="selectedPost"
              :is-comments-open="isCommentsOpen"
              :new-comment="newComment"
              @update:isCommentsOpen="isCommentsOpen = $event"
              @update:newComment="newComment = $event"
            />
          </section>
        </Transition>
      </div>

      <!-- 모바일/태블릿 레이아웃 -->
      <div class="lg:hidden">
        <!-- 상세 보기 모드 -->
        <section v-if="selectedPost">
          <Transition name="slide-detail">
            <DetailCard
              :post="selectedPost"
              :is-comments-open="isCommentsOpen"
              :new-comment="newComment"
              @update:isCommentsOpen="isCommentsOpen = $event"
              @update:newComment="newComment = $event"
            />
          </Transition>
        </section>

        <!-- 리스트 모드 -->
        <section v-else class="space-y-6">
          <!-- 카테고리 탭 -->
          <div class="flex flex-wrap justify-center gap-3">
            <button
              v-for="cat in categories"
              :key="cat.value"
              @click="handleCategoryChange(cat.value)"
              :class="[
                'px-4 py-2 text-xs font-bold rounded-full border-2 transition-all duration-200 flex items-center gap-2',
                selectedCategory === cat.value
                  ? 'bg-teal-900 text-white border-teal-900'
                  : 'bg-white text-teal-900 border-teal-900/50 hover:border-teal-900 hover:bg-teal-50',
              ]"
            >
              <span class="w-2 h-2 rounded-full bg-current"></span>
              {{ cat.label }}
            </button>
          </div>

          <!-- 카테고리별 리스트 컴포넌트 -->
          <ChatterList
            v-if="selectedCategory === 'chatter'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <RecommendList
            v-else-if="selectedCategory === 'recommend'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <TipList
            v-else-if="selectedCategory === 'tip'"
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
          <HotList
            v-else
            :selected-post-id="selectedPost?.id"
            @select-post="handleSelectPost"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import DetailCard from '@/components/community/DetailCard.vue'
import ChatterList from '@/components/community/ChatterList.vue'
import RecommendList from '@/components/community/RecommendList.vue'
import TipList from '@/components/community/TipList.vue'
import HotList from '@/components/community/HotList.vue'

const categories = [
  { value: 'hot', label: 'HOT' },
  { value: 'chatter', label: '빵 주저리' },
  { value: 'recommend', label: '빵집 추천' },
  { value: 'tip', label: '빵 꿀팁' },
]

const selectedCategory = ref('hot')
const selectedPost = ref(null)
const isCommentsOpen = ref(false)
const newComment = ref('')

// 반응형: 모바일 여부
const width = ref(window.innerWidth)
const onResize = () => {
  width.value = window.innerWidth
}
onMounted(() => {
  window.addEventListener('resize', onResize)
})
onUnmounted(() => window.removeEventListener('resize', onResize))
const isMobile = computed(() => width.value < 1024)

const currentCategoryLabel = computed(() => {
  const cat = categories.find((c) => c.value === selectedCategory.value)
  return cat ? cat.label : ''
})

const handleCategoryChange = (categoryValue) => {
  selectedCategory.value = categoryValue
  selectedPost.value = null
  isCommentsOpen.value = false
}

const handleSelectPost = async (post) => {
  selectedPost.value = post
  isCommentsOpen.value = false

  if (isMobile.value) {
    await nextTick()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const backToList = () => {
  selectedPost.value = null
  isCommentsOpen.value = false
}
</script>

<style scoped>
.slide-detail-enter-active,
.slide-detail-leave-active {
  transition: all 0.3s ease;
}
.slide-detail-enter-from,
.slide-detail-leave-to {
  opacity: 0;
  transform: translateX(16px);
}
</style>
