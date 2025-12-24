<template>
  <div class="grid grid-cols-1 font-jua md:grid-cols-2 lg:grid-cols-4 gap-8">
    <div v-for="(bakery, idx) in bakeries" :key="bakery.id"
         @click="$emit('open-detail', bakery)"
         :class="{'lg:translate-y-16': idx % 2 !== 0}"
         class="group cursor-pointer">
      <div class="img-zoom-container rounded-[2rem] mb-6 shadow-soft relative aspect-[3/4] bg-gradient-to-br from-amber-50 to-orange-50 overflow-hidden">
        <!-- 이미지가 있을 때 -->
        <img
          v-if="bakery.image && !imageErrors[bakery.id]"
          :src="bakery.image"
          class="w-full h-full object-cover"
          @error="handleImageError(bakery.id)"
        >

        <!-- 이미지가 없거나 로드 실패했을 때 -->
        <div v-if="!bakery.image || imageErrors[bakery.id]" class="w-full h-full flex flex-col items-center justify-center p-6 text-center">
          <img
            src="@/assets/images/logo.png"
            alt="기본 로고"
            class="w-16 h-16 object-contain opacity-30 mb-3"
          />
          <p class="text-xs font-bold text-gray-400 mb-1">이미지가 등록되지 않았어요</p>
          <p class="text-[10px] text-gray-400">제보하기를 통해 이미지를 등록해주세요 📸</p>
        </div>

        <div class="absolute top-4 right-4 bg-white/90 backdrop-blur w-10 h-10 rounded-full flex items-center justify-center shadow-sm opacity-0 group-hover:opacity-100 transition-opacity duration-500 translate-y-2 group-hover:translate-y-0">
          <i data-lucide="arrow-up-right" class="w-5 h-5 text-teal-900"></i>
        </div>
        <div class="absolute bottom-4 left-4 flex gap-2">
          <span class="px-3 py-1 bg-white/90 backdrop-blur rounded-full text-xs font-bold text-teal-900">#{{ bakery.tags[0] }}</span>
        </div>
      </div>
      <div class="px-2">
        <div class="flex justify-between items-center mb-2">
          <h3 class="text-2xl font-bold text-teal-900">{{ bakery.bakeryName }}</h3>

          <div class="flex items-center gap-1 text-orange-600 font-bold text-sm">
            <i data-lucide="star" class="w-3 h-3 fill-current"></i> {{ Number(bakery.rating).toFixed(1) }}
          </div>
        </div>
        <p class="text-sm text-gray-500">{{ bakery.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps(['bakeries'])
defineEmits(['open-detail'])

// 이미지 로드 실패 추적
const imageErrors = ref({})

// 이미지 에러 처리
const handleImageError = (bakeryId) => {
  imageErrors.value[bakeryId] = true
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}
</style>