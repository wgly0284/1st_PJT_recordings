<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- 카테고리 탭 -->
    <header class="flex gap-3">
      <button
        v-for="cat in categories"
        :key="cat.value"
        @click="selectedCategory = cat.value"
        :class="[
          'px-4 py-2 text-xs font-bold rounded-full border transition-all duration-200',
          selectedCategory === cat.value
            ? 'bg-teal-900 text-white border-teal-900'
            : 'bg-white text-teal-900 border-teal-900 hover:bg-teal-50'
        ]"
      >
        {{ cat.label }}
      </button>
    </header>

    <div>
      <h1 class="text-2xl font-bold mb-4">커뮤니티 메인</h1>

      <!-- 선택된 카테고리의 상위 3개 글 -->
      <div v-if="topPosts.length" class="space-y-3">
        <div
          v-for="post in topPosts"
          :key="post.id"
          class="p-4 border rounded-2xl hover:shadow-sm cursor-pointer"
        >
          <p class="text-xs text-gray-400 mb-1">{{ post.category }}</p>
          <p class="font-semibold text-teal-900 mb-1 truncate">{{ post.title }}</p>
          <p class="text-sm text-gray-600 line-clamp-2">{{ post.content }}</p>
        </div>
      </div>
      <p v-else class="text-gray-500 text-sm">아직 등록된 글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const categories = [
  { value: 'hot', label: 'HOT' },
  { value: 'chatter', label: '빵 주저리' },
  { value: 'recommend', label: '빵집 추천' },
  { value: 'tip', label: '빵 꿀팁' },
]

const selectedCategory = ref('hot')

// 개발용 목데이터 (나중에 API로 교체)
const posts = ref([
  { id: 1, category: '빵 주저리', type: 'chatter', title: '소금빵만 5군데 털어본 후기', content: '성수, 연남, 망원까지 돌면서 먹어본 소금빵 비교...' },
  { id: 2, category: '빵집 추천', type: 'recommend', title: '서울 밤에 가기 좋은 베이글 맛집', content: '야근 끝나고도 열려있는 베이글 빵집 모음.' },
  { id: 3, category: '빵 꿀팁', type: 'tip', title: '크루아상 바삭하게 보관하는 법', content: '에어프라이어로 3분만에 갓 구운 느낌 살리기.' },
  { id: 4, category: '빵집 추천', type: 'recommend', title: '제주도 사워도우 투어 루트', content: '차 없이도 돌아다닐 수 있는 빵지 순례 코스.' },
  { id: 5, category: '빵 주저리', type: 'chatter', title: '다이어트 중인데 빵 끊기 너무 힘들다', content: 'PT쌤 몰래 먹는 빵 이야기...' },
])

// HOT = 전체에서 상위 3개, 나머지 = 해당 카테고리에서 상위 3개
const topPosts = computed(() => {
  if (selectedCategory.value === 'hot') {
    return posts.value.slice(0, 3)
  }
  return posts.value
    .filter(p => p.type === selectedCategory.value)
    .slice(0, 3)
})
</script>
