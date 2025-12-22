<template>
  <div class="bg-white rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
    <!-- 헤더 -->
    <header class="bg-gradient-to-r from-teal-900 to-teal-700 text-white p-6 lg:p-8">
      <div class="flex items-center justify-between mb-4 gap-3 flex-wrap">
        <span class="px-4 py-1 bg-white/20 rounded-full text-xs font-bold">
          {{ post.category }}
        </span>
        <div class="flex gap-4 text-xs lg:text-sm opacity-90 flex-wrap">
          <span>❤️ {{ post.likes }}</span>
          <span>💬 {{ post.comments }}</span>
          <span>👀 {{ post.views }}k</span>
        </div>
      </div>
      <h2 class="text-2xl lg:text-3xl font-bold mb-3 leading-tight">
        {{ post.title }}
      </h2>
      <p class="text-xs lg:text-sm opacity-80">
        {{ post.date }} · 빵순이🥐
      </p>
    </header>

    <!-- 본문 -->
    <main class="p-6 lg:p-8 space-y-6">
      <p class="text-sm lg:text-base text-gray-800 leading-relaxed">
        {{ post.content }}
      </p>

      <section class="p-5 bg-teal-50 rounded-2xl text-sm lg:text-base text-gray-700">
        <h3 class="font-bold text-teal-900 mb-2">🥯 빵집 정보</h3>
        <p>성수동 빵순이 맛집 · 영업시간 08:00–22:00 · 평점 ★4.9</p>
      </section>
    </main>

    <!-- 댓글 아코디언 -->
    <section class="border-t border-gray-100">
      <!-- 토글 헤더 -->
      <button
        type="button"
        class="w-full flex items-center justify-between px-6 lg:px-8 py-4 text-sm lg:text-base font-semibold text-left hover:bg-gray-50 transition-colors"
        @click="$emit('update:isCommentsOpen', !isCommentsOpen)"
      >
        <span class="flex items-center gap-2">
          💬 댓글 {{ post.comments }}
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
          <!-- 댓글 리스트 (목업) -->
          <div class="space-y-3 max-h-64 overflow-y-auto">
            <div class="flex gap-3 p-3 bg-white rounded-xl shadow-sm shadow-black/5">
              <div
                class="w-9 h-9 rounded-full bg-teal-100 flex items-center justify-center flex-shrink-0"
              >
                <span class="text-xs font-bold">🍞</span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-xs font-semibold mb-1">크루아상러버</p>
                <p class="text-xs text-gray-700">
                  소금빵 진짜 맛있게 드셨군요! 다음엔 함께 가요~
                </p>
                <p class="text-[11px] text-gray-400 mt-1">
                  2시간 전 · 좋아요 5
                </p>
              </div>
            </div>
          </div>

          <!-- 댓글 입력 -->
          <div class="mt-4">
            <textarea
              :value="newComment"
              @input="$emit('update:newComment', $event.target.value)"
              rows="2"
              class="w-full text-xs lg:text-sm p-3 border border-gray-200 rounded-2xl resize-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500 outline-none bg-white"
              placeholder="빵 이야기 남겨보세요 :)"
            ></textarea>
            <div class="flex justify-end gap-2 mt-2">
              <button
                type="button"
                class="px-3 py-1 text-[11px] text-gray-500 hover:text-gray-700"
                @click="$emit('update:isCommentsOpen', false)"
              >
                취소
              </button>
              <button
                type="button"
                class="px-4 py-1.5 text-[11px] lg:text-xs font-bold rounded-xl bg-teal-900 text-white hover:bg-teal-800"
              >
                댓글 달기
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </section>
  </div>
</template>

<script setup>
const props = defineProps({
  post: { type: Object, required: true },
  isCommentsOpen: { type: Boolean, default: false },
  newComment: { type: String, default: '' },
})

defineEmits(['update:isCommentsOpen', 'update:newComment'])
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
  max-height: 500px;
  opacity: 1;
}
</style>
