<script setup>
import { BookOpen } from 'lucide-vue-next';

// 부모(MyPage)로부터 데이터를 받아옵니다.
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

// 스탬프 랜덤 회전 각도 생성 함수 (템플릿 내에서 호출)
const getRotation = () => {
  return Math.random() * 10 - 5; // -5도 ~ +5도 사이 랜덤
};
</script>

<template>
  <div class="bg-[#FFFDF9] rounded-3xl shadow-xl border border-[#F0EBE0] overflow-hidden flex flex-col h-full relative group">
    <!-- 여권 질감 효과 -->
    <div class="absolute inset-0 opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/paper.png')] pointer-events-none"></div>
    
    <!-- 헤더 -->
    <div class="bg-[#2C3E50] p-4 flex items-center justify-between relative overflow-hidden shrink-0">
       <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/leather.png')] opacity-30"></div>
       <h3 class="text-white font-serif font-bold flex items-center gap-2 relative z-10 text-lg">
         <BookOpen class="w-5 h-5 text-yellow-500" /> REPUBLIC OF BREAD
       </h3>
       <div class="text-[10px] text-yellow-500/80 border border-yellow-500/50 px-2 py-0.5 rounded uppercase tracking-widest relative z-10">
         Passport
       </div>
    </div>

    <!-- 여권 내부 (스탬프 영역) -->
    <div class="p-6 flex-1 bg-[#FFFDF9] overflow-y-auto custom-scroll">
        <div class="flex items-center justify-between mb-4 text-xs text-[#8B7E74] border-b border-dashed border-[#D7CCC8] pb-2">
            <span>VISAS</span>
            <span>방문한 빵집 {{ visitedStores.length }}곳</span>
        </div>

        <!-- 스탬프 그리드 -->
        <div class="grid grid-cols-3 gap-3">
            <!-- 가입 기념 스탬프 -->
            <div class="aspect-square border-2 border-double border-teal-800/30 rounded-full flex flex-col items-center justify-center p-2 transform -rotate-6 opacity-80 hover:scale-110 transition-transform cursor-help" title="입국 도장">
                <span class="text-[8px] text-teal-900 font-bold uppercase tracking-tighter">Entry</span>
                <div class="text-2xl text-teal-800">✈️</div>
                <span class="text-[8px] text-teal-900">{{ dateJoined }}</span>
            </div>

            <!-- 방문 스탬프 -->
            <div v-for="store in visitedStores" :key="store.id" 
                 class="aspect-square border-2 border-orange-700/40 rounded-xl flex flex-col items-center justify-center p-1 transform hover:scale-110 transition-transform relative group/stamp"
                 :style="{ transform: `rotate(${getRotation()}deg)` }">
                <div class="absolute inset-0 border border-orange-800/20 rounded-xl m-1"></div>
                <span class="text-[9px] text-orange-900/70 font-serif w-full text-center truncate px-1">{{ store.location }}</span>
                <div class="text-2xl my-1 opacity-90">🥨</div>
                <span class="text-[9px] text-orange-900 font-bold w-full text-center truncate px-1">{{ store.name }}</span>
                <span class="text-[7px] text-orange-800/50 absolute bottom-1 right-1">{{ store.date }}</span>
            </div>

            <!-- 빈 공간 (투명 도장 느낌) -->
            <div v-for="i in Math.max(0, 5 - visitedStores.length)" :key="`empty-${i}`"
                 class="aspect-square border border-dashed border-gray-300 rounded-xl flex items-center justify-center opacity-20">
            </div>
        </div>
    </div>
    
    <!-- 페이지 넘김 효과 장식 -->
    <div class="absolute right-0 top-0 bottom-0 w-6 bg-gradient-to-l from-black/5 to-transparent pointer-events-none"></div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&display=swap');

.font-serif {
  font-family: 'Gaegu', cursive;
}

/* 스크롤바 커스텀 (여권 내부 스크롤) */
.custom-scroll::-webkit-scrollbar {
  width: 4px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background-color: #D7CCC8;
  border-radius: 20px;
}
</style>