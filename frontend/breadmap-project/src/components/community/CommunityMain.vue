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
          <div
            class="flex flex-wrap lg:flex-nowrap justify-center lg:justify-start gap-3"
          >
            <button
              v-for="cat in categories"
              :key="cat.value"
              @click="
                () => {
                  selectedCategory = cat.value
                  selectedPost = null
                  isCommentsOpen = false
                }
              "
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

          <!-- 글 목록 -->
          <div class="space-y-4">
            <article
              v-for="post in filteredPosts"
              :key="post.id"
              @click="handleSelectPost(post)"
              :class="[
                'group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all',
                selectedPost && selectedPost.id === post.id
                  ? 'ring-2 ring-teal-500 bg-teal-50'
                  : '',
              ]"
            >
              <div class="flex items-center gap-2 mb-3">
                <span
                  class="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full"
                >
                  {{ post.category }}
                </span>
                <span class="text-xs text-gray-400 font-medium">
                  {{ post.type.toUpperCase() }}
                </span>
              </div>
              <h3
                class="text-lg font-bold text-gray-900 mb-2 line-clamp-1 group-hover:text-teal-900 transition-colors"
              >
                {{ post.title }}
              </h3>
              <p class="text-sm text-gray-600 line-clamp-2">
                {{ post.content }}
              </p>
              <div
                class="flex items-center justify-between mt-3 text-xs text-gray-500"
              >
                <div class="flex gap-3">
                  <span>❤️ {{ post.likes }}</span>
                  <span>💬 {{ post.comments }}</span>
                  <span>👀 {{ post.views }}k</span>
                </div>
                <span
                  class="hidden sm:inline-flex items-center gap-1 text-teal-700 group-hover:underline"
                >
                  자세히 보기
                </span>
              </div>
            </article>

            <p
              v-if="!filteredPosts.length"
              class="text-center text-sm text-gray-500 py-10"
            >
              아직 등록된 글이 없습니다. 첫 번째 빵 이야기를 남겨보세요!
            </p>
          </div>
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
              @click="
                () => {
                  selectedCategory = cat.value
                  isCommentsOpen = false
                }
              "
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

          <!-- 글 목록 -->
          <div class="space-y-4">
            <article
              v-for="post in filteredPosts"
              :key="post.id"
              @click="handleSelectPost(post)"
              class="group bg-white p-5 rounded-3xl border border-gray-100 cursor-pointer hover:shadow-md hover:-translate-y-1 transition-all"
            >
              <div class="flex items-center gap-2 mb-3">
                <span
                  class="px-3 py-1 bg-teal-100 text-teal-800 text-xs font-bold rounded-full"
                >
                  {{ post.category }}
                </span>
                <span class="text-xs text-gray-400 font-medium">
                  {{ post.type.toUpperCase() }}
                </span>
              </div>
              <h3
                class="text-lg font-bold text-gray-900 mb-2 line-clamp-1 group-hover:text-teal-900 transition-colors"
              >
                {{ post.title }}
              </h3>
              <p class="text-sm text-gray-600 line-clamp-2">
                {{ post.content }}
              </p>
              <div
                class="flex items-center justify-between mt-3 text-xs text-gray-500"
              >
                <div class="flex gap-3">
                  <span>❤️ {{ post.likes }}</span>
                  <span>💬 {{ post.comments }}</span>
                  <span>👀 {{ post.views }}k</span>
                </div>
                <span class="inline-flex items-center gap-1 text-teal-700">
                  자세히 보기
                </span>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
  onUnmounted,
  nextTick,
} from 'vue'
import DetailCard from '@/components/community/DetailCard.vue'

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
onMounted(() => window.addEventListener('resize', onResize))
onUnmounted(() => window.removeEventListener('resize', onResize))
const isMobile = computed(() => width.value < 1024)

// 목데이터
const posts = ref([
  {
    id: 1,
    category: '빵 주저리',
    type: 'chatter',
    title: '소금빵만 5군데 털어본 후기',
    content:
      '성수, 연남, 망원까지 돌면서 먹어본 소금빵 비교. 가격, 크기, 소금 함량까지 꼼꼼하게 비교해봤어요.',
    likes: 42,
    comments: 12,
    views: 1.2,
    date: '2025.12.20',
  },
  {
    id: 2,
    category: '빵집 추천',
    type: 'recommend',
    title: '서울 밤에 가기 좋은 베이글 맛집',
    content:
      '야근 끝나고도 열려있는 베이글 빵집 모음. 늦은 밤 크리미하고 쫀득한 베이글이 땡길 때 딱 좋은 곳들입니다.',
    likes: 28,
    comments: 8,
    views: 0.8,
    date: '2025.12.19',
  },
  {
    id: 3,
    category: '빵 꿀팁',
    type: 'tip',
    title: '크루아상 바삭하게 보관하는 법',
    content:
      '에어프라이어로 3분만에 갓 구운 느낌 살리기. 냉동 보관부터 해동까지 완벽한 크루아상 관리법 공유합니다.',
    likes: 67,
    comments: 23,
    views: 2.3,
    date: '2025.12.18',
  },
  {
    id: 4,
    category: '빵집 추천',
    type: 'recommend',
    title: '제주도 사워도우 투어 루트',
    content:
      '차 없이도 돌아다닐 수 있는 빵지 순례 코스. 제주공항 근처부터 성산까지 버스 타고 즐기는 사워도우 여행.',
    likes: 35,
    comments: 15,
    views: 1.8,
    date: '2025.12.17',
  },
])

const filteredPosts = computed(() => {
  if (selectedCategory.value === 'hot') return posts.value
  return posts.value.filter((p) => p.type === selectedCategory.value)
})

const currentCategoryLabel = computed(() => {
  const cat = categories.find((c) => c.value === selectedCategory.value)
  return cat ? cat.label : ''
})

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
