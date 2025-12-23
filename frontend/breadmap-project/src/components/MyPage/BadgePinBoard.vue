<script setup>
import { defineProps } from 'vue';
import { Award, Lock } from 'lucide-vue-next';

defineProps({
  badges: {
    type: Array,
    required: true,
    default: () => []
  }
});
</script>

<template>
  <div class="relative w-full bg-[#263238] rounded-xl border-[10px] border-[#5D4037] shadow-[0_10px_30px_rgba(0,0,0,0.5)] overflow-hidden">
    
    <!-- 1. 벨벳 텍스처 배경 -->
    <div class="absolute inset-0 opacity-40 pointer-events-none" 
         style="background-image: url('https://www.transparenttextures.com/patterns/black-felt.png');">
    </div>

    <!-- 2. 상단 유리 반사 효과 (Glass Reflection) -->
    <div class="absolute inset-0 bg-gradient-to-tr from-white/10 via-transparent to-transparent pointer-events-none z-20 rounded-lg"></div>
    <div class="absolute top-0 right-0 w-2/3 h-full bg-gradient-to-bl from-white/5 to-transparent pointer-events-none z-20"></div>

    <!-- 3. 헤더: 금속 명판 느낌 -->
    <div class="relative z-10 flex justify-center pt-6 pb-2">
      <div class="bg-gradient-to-r from-[#FFD700] via-[#FDB931] to-[#FFD700] px-6 py-1 rounded shadow-md border border-[#C5A028] transform hover:scale-105 transition-transform duration-300">
        <h3 class="text-[#5D4037] font-serif font-bold text-sm tracking-widest uppercase flex items-center gap-2">
          <Award class="w-4 h-4" /> Master Collection
        </h3>
      </div>
    </div>

    <!-- 4. 뱃지 그리드 -->
    <div class="relative z-10 p-6 min-h-[250px]">
      <div v-if="badges.length > 0" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-6">
        
        <!-- 획득한 뱃지 (핀 뱃지 느낌) -->
        <div v-for="(badge, idx) in badges" :key="idx" 
             class="group flex flex-col items-center justify-center relative">
          
          <!-- 뱃지 본체 (금속 광택 효과 및 그림자) -->
          <div class="relative w-16 h-16 flex items-center justify-center transition-all duration-300 transform group-hover:-translate-y-1 group-hover:scale-110 cursor-pointer">
            <!-- 핀 그림자 (입체감) -->
            <div class="absolute bottom-[-5px] w-10 h-2 bg-black/50 blur-sm rounded-[50%]"></div>
            
            <div class="text-5xl filter drop-shadow-md z-10 relative">
              {{ badge.icon }}
              <!-- 하이라이트 (광택) -->
              <div class="absolute top-1 right-2 w-2 h-2 bg-white rounded-full opacity-40 blur-[1px]"></div>
            </div>
          </div>

          <!-- 이름표 -->
          <span class="mt-2 text-[10px] text-[#E0E0E0] font-medium bg-black/30 px-2 py-0.5 rounded-full backdrop-blur-sm border border-white/10">
            {{ badge.name }}
          </span>

          <!-- 툴팁 -->
          <div class="absolute -top-10 left-1/2 -translate-x-1/2 bg-black/90 text-[#FFD700] text-xs px-3 py-1.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-30 pointer-events-none border border-[#FFD700]/30">
            {{ badge.description }}
            <div class="absolute bottom-[-4px] left-1/2 -translate-x-1/2 w-2 h-2 bg-black/90 rotate-45 border-b border-r border-[#FFD700]/30"></div>
          </div>
        </div>

        <!-- 빈 슬롯 (음각 효과) -->
        <div v-for="i in Math.max(0, 5 - badges.length)" :key="`slot-${i}`" 
             class="flex flex-col items-center justify-center opacity-30">
          <div class="w-14 h-14 rounded-full border-2 border-dashed border-gray-500 bg-black/20 flex items-center justify-center shadow-[inset_0_2px_4px_rgba(0,0,0,0.5)]">
             <Lock class="w-5 h-5 text-gray-500" />
          </div>
        </div>

      </div>

      <!-- 뱃지가 하나도 없을 때 -->
      <div v-else class="flex flex-col items-center justify-center h-40 text-gray-500/50">
        <Award class="w-16 h-16 mb-2 opacity-20" />
        <p class="text-xs uppercase tracking-widest">Collection Empty</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');

.font-serif {
  font-family: 'Cinzel', serif; /* 명판용 고급스러운 폰트 */
}
</style>