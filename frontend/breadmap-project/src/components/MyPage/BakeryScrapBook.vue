<script setup>
import { defineProps, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { MapPin, X } from 'lucide-vue-next';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  bookmarkedStores: {
    type: Array,
    required: true,
    default: () => []
  }
});

const router = useRouter();
const authStore = useAuthStore();

// Props로 받은 데이터를 내부에서 수정(삭제)할 수 있도록 로컬 상태로 복사
const localStores = ref([...props.bookmarkedStores]);

// Props가 변경되면 로컬 상태도 업데이트 (데이터 동기화)
watch(() => props.bookmarkedStores, (newVal) => {
  localStores.value = [...newVal];
});

// 폴라로이드 랜덤 회전 각도 (-3도 ~ +3도)
const getRandomRotate = () => {
  return Math.random() * 6 - 3;
};

// 마스킹 테이프 색상 랜덤
const tapeColors = ['bg-pink-200/80', 'bg-yellow-200/80', 'bg-blue-200/80', 'bg-green-200/80'];
const getRandomTape = () => {
  return tapeColors[Math.floor(Math.random() * tapeColors.length)];
};

// 1️⃣ 상세 페이지 이동
const goToDetail = (id) => {
  router.push({ name: 'detail', params: { id } });
};

// 2️⃣ 북마크 삭제 로직
const removeBookmark = async (storeId) => {
  if (!confirm('이 빵집을 스크랩북에서 떼어낼까요? 🗑️')) return;

  try {
    const token = authStore.token;
    await axios.post(
      `http://127.0.0.1:8000/stores/${storeId}/bookmark/`,
      {},
      { headers: { Authorization: `Token ${token}` } }
    );

    // 화면 목록에서 즉시 제거 (API 호출 성공 시)
    localStores.value = localStores.value.filter(store => store.id !== storeId);
  } catch (error) {
    console.error('북마크 제거 실패:', error);
    alert('삭제 중 오류가 발생했습니다.');
  }
};
</script>

<template>
  <div class="relative w-full h-full min-h-[400px] bg-[#E8DCC4] rounded-3xl shadow-xl overflow-hidden flex flex-col border-[8px] border-[#D4C5A9]">
    
    <!-- 1. 코르크 보드 질감 배경 -->
    <div class="absolute inset-0 opacity-60 pointer-events-none" 
         style="background-image: url('https://www.transparenttextures.com/patterns/cork-board.png'); background-size: 300px;">
    </div>
    <div class="absolute inset-0 shadow-[inset_0_0_80px_rgba(0,0,0,0.2)] pointer-events-none z-10"></div>

    <!-- 2. 헤더: 포스트잇 스타일 -->
    <div class="relative z-20 pt-8 px-8 pb-4">
      <div class="inline-block bg-[#FFF9C4] px-6 py-3 shadow-md transform -rotate-1 relative">
        <div class="absolute -top-3 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-red-500 shadow-sm border border-red-600 z-30"></div> <!-- 압정 -->
        <h3 class="font-serif text-2xl font-bold text-[#5D4037] tracking-widest">
           MY BAKERY BUCKET LIST 📌
        </h3>
        <p class="font-hand text-sm text-gray-600 mt-1">언젠가 꼭 정복하고 말 거야!</p>
      </div>
    </div>

    <!-- 3. 폴라로이드 그리드 -->
    <div class="relative z-20 p-6 overflow-y-auto custom-scroll flex-1">
      
      <!-- 데이터가 있을 때 -->
      <div v-if="localStores && localStores.length > 0" class="grid grid-cols-2 md:grid-cols-3 gap-6 pb-8">
        <div v-for="(store, index) in localStores" :key="store.id"
             class="group relative bg-white p-3 pb-8 shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 cursor-pointer ease-out"
             :style="{ transform: `rotate(${getRandomRotate()}deg)` }"
             @click="goToDetail(store.id)">
          
          <!-- 마스킹 테이프 (상단 중앙) -->
          <div :class="`absolute -top-3 left-1/2 -translate-x-1/2 w-16 h-6 ${getRandomTape()} shadow-sm rotate-1 opacity-90 z-30`"></div>

          <!-- 🗑️ 삭제 버튼 (호버 시 등장) -->
          <button 
            @click.stop="removeBookmark(store.id)"
            class="absolute -top-2 -right-2 bg-white rounded-full p-1 shadow-md opacity-0 group-hover:opacity-100 transition-opacity z-40 hover:bg-red-50 text-red-400"
            title="삭제하기"
          >
            <X class="w-4 h-4" />
          </button>

          <!-- 사진 영역 -->
          <div class="w-full aspect-square bg-gradient-to-br from-amber-50 to-orange-50 mb-3 overflow-hidden border border-gray-200 grayscale-[20%] group-hover:grayscale-0 transition-all">
            <img
              v-if="store.image || store.image_url"
              :src="store.image || store.image_url"
              class="w-full h-full object-cover"
              @error="e => e.target.src = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600'"
            >
            <div v-else class="w-full h-full flex flex-col items-center justify-center p-3 text-center">
              <img
                src="@/assets/images/logo.png"
                alt="기본 로고"
                class="w-12 h-12 object-contain opacity-30 mb-2"
              />
              <p class="text-[10px] text-gray-400 leading-tight">이미지 없음<br/>제보 요청📸</p>
            </div>
          </div>

          <!-- 텍스트 (손글씨 느낌) -->
          <div class="text-center">
             <h4 class="font-hand text-lg font-bold text-[#3E2723] truncate px-1 group-hover:text-orange-600 transition-colors">{{ store.name }}</h4>
             <div class="flex items-center justify-center gap-1 text-[#8D6E63] text-xs font-hand mt-1">
                <MapPin class="w-3 h-3" /> {{ store.address || store.location || '위치 정보 없음' }}
             </div>
          </div>

          <!-- 호버 시 나타나는 스티커 -->
          <div class="absolute -bottom-2 -right-2 text-3xl opacity-0 group-hover:opacity-100 group-hover:scale-110 transition-all duration-300 rotate-12">
            🤤
          </div>
        </div>
      </div>

      <!-- 데이터가 없을 때 (빈 메모지) -->
      <div v-else class="flex justify-center items-center h-48">
         <div class="bg-white p-6 shadow-md rotate-2 max-w-xs text-center relative">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 w-24 h-6 bg-blue-200/70 shadow-sm -rotate-2"></div>
            <p class="font-hand text-gray-500 text-lg">아직 찜해둔 빵집이 없어요.<br>맛있는 곳을 찾아볼까요? 🥐</p>
         </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Nanum+Pen+Script&display=swap');

.font-serif {
  font-family: 'Gaegu', cursive;
}

.font-hand {
  font-family: 'Nanum Pen Script', cursive; /* 더 손글씨 같은 폰트 */
  font-size: 1.2rem;
}

/* 스크롤바 커스텀 */
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.05);
}
.custom-scroll::-webkit-scrollbar-thumb {
  background-color: #8D6E63;
  border-radius: 10px;
}
</style>