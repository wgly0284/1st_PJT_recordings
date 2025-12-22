<script setup>
import { ref } from 'vue'; // ref 추가
import { X, Star, MapPin, ChevronRight, Phone, Clock, Utensils, Sparkles } from 'lucide-vue-next'; // Sparkles 아이콘 추가
import axios from 'axios'; // axios 추가 (AI 요약 호출용)

// 부모로부터 선택된 빵집 정보와 닫기 이벤트를 받습니다.
const props = defineProps({
  bakery: { type: Object, required: true }
});

const emit = defineEmits(['close', 'view-detail']);

const aiSummary = ref(null); // AI 요약 데이터 저장
const isAiLoading = ref(false); // AI 로딩 상태

// 이미지 에러 처리
const handleImageError = (e) => {
  e.target.src = 'https://source.unsplash.com/random/400x300/?bread'; 
};

// [추가] AI 요약 생성 함수 (카드용 간략 버전)
const generateAISummary = async () => {
  if (isAiLoading.value) return;
  isAiLoading.value = true;
  
  try {
    // ⚠️ 실제 백엔드 주소 확인 (예: http://127.0.0.1:8000/stores/1/ai-summary/)
    const response = await axios.get(`http://127.0.0.1:8000/stores/${props.bakery.id}/ai-summary/`);
    
    aiSummary.value = {
      text: response.data.summary,
      keywords: response.data.keywords
    };
  } catch (error) {
    console.error("AI 요약 실패:", error);
    aiSummary.value = {
      text: "아직 분석할 리뷰가 충분하지 않아요 🥲",
      keywords: ["데이터부족"]
    };
  } finally {
    isAiLoading.value = false;
  }
};
</script>

<template>
  <div class="h-full flex flex-col bg-white animate-slide-in shadow-lg border-l border-gray-100">
    <!-- 1. 헤더 (이미지 및 닫기 버튼) -->
    <div class="relative w-full h-56 bg-gray-100 shrink-0 overflow-hidden">
      <img 
        :src="bakery.image" 
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
      
      <!-- 평점 배지 (이미지 위 오버레이) -->
      <div class="absolute bottom-4 left-4 flex gap-2">
         <div class="bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs font-bold text-orange-600 shadow-sm flex items-center gap-1">
           <Star class="w-3.5 h-3.5 fill-current" /> {{ bakery.rating ? Number(bakery.rating).toFixed(1) : '0.0' }}
         </div>
         <div v-if="bakery.tags && bakery.tags.length > 0" class="bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-xl text-xs font-bold text-[#1D4E45] shadow-sm">
           #{{ bakery.tags[0] }}
         </div>
      </div>
    </div>

    <!-- 2. 본문 정보 -->
    <div class="p-6 flex-1 flex flex-col overflow-y-auto hide-scrollbar">
      <div class="mb-5">
        <h2 class="text-2xl font-bold text-[#1D4E45] mb-2 font-serif leading-tight">{{ bakery.name }}</h2>
        <div class="flex flex-wrap gap-1.5">
           <span v-for="tag in bakery.tags" :key="tag" class="text-[10px] px-2 py-0.5 bg-gray-100 text-gray-500 rounded-md">#{{ tag }}</span>
        </div>
      </div>

      <div class="space-y-3 mb-6 bg-gray-50 p-4 rounded-2xl border border-gray-100">
        <div class="flex items-start gap-3 text-sm text-gray-600">
          <MapPin class="w-4 h-4 mt-0.5 text-[#1D4E45]" />
          <span class="leading-snug">{{ bakery.address }}</span>
        </div>
        
        <!-- 영업시간 (데이터가 있다면 표시) -->
        <div class="flex items-center gap-3 text-sm text-gray-600">
          <Clock class="w-4 h-4 text-[#1D4E45]" />
          <span>{{ bakery.business_hours || '10:00 ~ 20:00' }}</span>
        </div>

        <!-- 전화번호 (데이터가 있다면 표시) -->
        <div v-if="bakery.contact" class="flex items-center gap-3 text-sm text-gray-600">
          <Phone class="w-4 h-4 text-[#1D4E45]" />
          <span>{{ bakery.contact }}</span>
        </div>
      </div>

      <!-- ✅ [추가] AI 요약 섹션 -->
      <div class="mb-6">
        <h3 class="text-sm font-bold text-teal-800 mb-3 flex items-center gap-1.5">
            <Sparkles class="w-4 h-4 text-purple-500" /> AI 리뷰 요약
        </h3>
        
        <div v-if="!aiSummary" class="text-center">
            <button 
                @click="generateAISummary" 
                class="w-full py-2 bg-purple-50 border border-purple-100 rounded-xl text-xs font-bold text-purple-600 hover:bg-purple-100 transition-colors flex items-center justify-center gap-2"
                :disabled="isAiLoading"
            >
                <span v-if="isAiLoading" class="animate-spin w-3 h-3 border-2 border-purple-600 border-t-transparent rounded-full"></span>
                <span v-else>✨ AI 분석 보기</span>
            </button>
        </div>
        
        <div v-else class="bg-purple-50 p-4 rounded-xl border border-purple-100 animate-slide-in">
            <p class="text-xs text-gray-700 leading-relaxed mb-2 line-clamp-3">"{{ aiSummary.text }}"</p>
            <div class="flex flex-wrap gap-1">
                <span v-for="k in aiSummary.keywords" :key="k" class="text-[10px] bg-white text-purple-600 px-2 py-0.5 rounded border border-purple-200">#{{ k }}</span>
            </div>
        </div>
      </div>

      <!-- 대표 메뉴 미리보기 -->
      <!-- bakery.menu 데이터가 있는지 확인 -->
      <div class="mb-4">
        <h3 class="text-sm font-bold text-gray-800 mb-3 flex items-center gap-1.5">
            <Utensils class="w-4 h-4 text-orange-500" /> 대표 메뉴
        </h3>
        
        <div v-if="bakery.menu && bakery.menu.length > 0" class="space-y-2">
          <!-- TODO: 실제 메뉴 데이터 필드명(name, price 등) 확인 필요 -->
          <div v-for="item in bakery.menu.slice(0, 3)" :key="item.id || item.name" class="flex items-center justify-between p-3 bg-white border border-gray-100 rounded-xl hover:border-orange-100 transition-colors">
            <div class="flex items-center gap-3 overflow-hidden">
                <div class="w-8 h-8 rounded-lg bg-gray-100 shrink-0 overflow-hidden">
                    <img v-if="item.image_url" :src="item.image_url" class="w-full h-full object-cover">
                    <div v-else class="w-full h-full flex items-center justify-center text-xs">🍞</div>
                </div>
                <span class="text-sm text-gray-700 truncate font-medium">{{ item.name }}</span>
            </div>
            <span class="text-xs font-bold text-orange-600 shrink-0">{{ Number(item.price).toLocaleString() }}원</span>
          </div>
          <div v-if="bakery.menu.length > 3" class="text-center text-xs text-gray-400 mt-1">
            + {{ bakery.menu.length - 3 }}개의 메뉴 더보기
          </div>
        </div>
        
        <div v-else class="text-center py-6 bg-gray-50 rounded-xl border border-dashed border-gray-200">
            <p class="text-xs text-gray-400">등록된 대표 메뉴가 없어요 🥐</p>
        </div>
      </div>
    </div>
    
    <!-- 3. 하단 고정 버튼 -->
    <div class="p-5 border-t border-gray-100 bg-white shrink-0">
        <button 
            @click="$emit('view-detail', bakery.id)"
            class="w-full py-4 bg-[#1D4E45] text-white rounded-xl font-bold hover:bg-[#153e35] transition-all flex items-center justify-center gap-2 shadow-lg shadow-teal-900/10 active:scale-[0.98] group"
        >
            상세보기 <ChevronRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </button>
    </div>
  </div>
</template>

<style scoped>
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
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