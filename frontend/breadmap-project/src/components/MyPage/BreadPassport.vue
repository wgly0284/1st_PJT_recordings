<script setup>
import { BookOpen } from 'lucide-vue-next';

defineProps({
  visitedStores: {
    type: Array,
    required: true,
    default: () => []
  },
  dateJoined: {
    type: String,
    required: true
  }
});

const getRotation = () => {
  return Math.random() * 10 - 5;
};

// 날짜 포맷팅 함수 (ISO 문자열에서 T 앞부분만 추출)
const formatDate = (dateString) => {
  if (!dateString) return '';
  return dateString.split('T')[0];
};
</script>

<template>
  <div class="bg-[#FFFDF9] rounded-3xl shadow-xl border border-[#F0EBE0] overflow-hidden flex flex-col h-full relative group">
    <!-- 여권 질감 효과 -->
    <div class="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/paper.png')] pointer-events-none"></div>
    
    <!-- 헤더 -->
    <div class="bg-[#2C3E50] p-5 flex items-center justify-between relative overflow-hidden shrink-0">
       <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/leather.png')] opacity-30"></div>
       <h3 class="text-white font-serif font-bold flex items-center gap-3 relative z-10 text-2xl tracking-wide">
         <BookOpen class="w-6 h-6 text-yellow-500" /> REPUBLIC OF BREAD
       </h3>
       <div class="text-xs font-bold text-yellow-500/90 border border-yellow-500/50 px-3 py-1 rounded uppercase tracking-widest relative z-10">
         Passport
       </div>
    </div>

    <!-- 여권 내부 (스탬프 영역) -->
    <div class="p-6 flex-1 bg-[#FFFDF9] overflow-y-auto custom-scroll">
       <div class="flex items-center justify-between mb-6 text-sm font-bold text-[#8B7E74] border-b-2 border-dashed border-[#D7CCC8] pb-3">
          <span>VISAS</span>
          <span>방문한 빵집 {{ visitedStores.length }}곳</span>
       </div>

       <!-- 스탬프 그리드 -->
       <div class="grid grid-cols-3 gap-4">
          <!-- 가입 기념 스탬프 -->
          <div class="aspect-square border-4 border-double border-teal-800/30 rounded-full flex flex-col items-center justify-center p-2 transform -rotate-6 opacity-90 hover:scale-110 transition-transform cursor-help bg-teal-50/30" title="입국 도장">
              <span class="text-[10px] text-teal-900 font-bold uppercase tracking-tighter mb-1">Entry</span>
              <div class="text-3xl text-teal-800 mb-1">✈️</div>
              <!-- 수정됨: formatDate 함수 적용 -->
              <span class="text-[10px] font-bold text-teal-900">{{ formatDate(dateJoined) }}</span>
          </div>

          <!-- 방문 스탬프 -->
          <div v-for="store in visitedStores" :key="store.id" 
               class="aspect-square border-2 border-orange-700/40 rounded-xl flex flex-col items-center justify-center p-1 transform hover:scale-110 transition-transform relative group/stamp bg-orange-50/20 shadow-sm"
               :style="{ transform: `rotate(${getRotation()}deg)` }">
              <div class="absolute inset-0 border border-orange-800/20 rounded-xl m-1"></div>
              
              <!-- 지역 (폰트 키움) -->
              <span class="text-[11px] text-orange-900/80 font-serif w-full text-center truncate px-1 mt-1">
                {{ store.location }}
              </span>
              
              <!-- 아이콘 -->
              <div class="text-3xl my-1 opacity-90 drop-shadow-sm">🥨</div>
              
              <!-- 가게 이름 (폰트 키움 & 강조) -->
              <span class="text-xs text-orange-900 font-extrabold w-full text-center truncate px-1 leading-tight">
                {{ store.name }}
              </span>
              
              <!-- 날짜 (폰트 키움) -->
              <!-- 수정됨: formatDate 함수 적용 -->
              <span class="text-[9px] font-bold text-orange-800/60 absolute bottom-1 right-2">
                {{ formatDate(store.date) }}
              </span>
          </div>

          <!-- 빈 공간 -->
          <div v-for="i in Math.max(0, 5 - visitedStores.length)" :key="`empty-${i}`"
               class="aspect-square border-2 border-dashed border-gray-300 rounded-xl flex items-center justify-center opacity-30">
               <span class="text-2xl text-gray-300 font-bold">?</span>
          </div>
       </div>
    </div>
    
    <!-- 페이지 넘김 효과 장식 -->
    <div class="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-black/5 to-transparent pointer-events-none"></div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

.font-serif {
  font-family: 'Gaegu', cursive;
}

/* 스크롤바 커스텀 */
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background-color: #D7CCC8;
  border-radius: 20px;
}
</style>