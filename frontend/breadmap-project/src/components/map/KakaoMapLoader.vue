<script setup>
import { ref, onMounted } from 'vue';

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;
const isLoaded = ref(false);

const initMap = () => {
  // 1. 이미 kakao 객체가 있고, maps까지 로드된 상태인지 체크
  if (window.kakao && window.kakao.maps) {
    // 안전하게 한번 더 load 함수 호출 후 상태 변경
    window.kakao.maps.load(() => {
      isLoaded.value = true;
    });
    return;
  }

  // 2. 스크립트가 헤더에 이미 있는지 확인 (중복 삽입 방지)
  const scriptId = 'kakao-map-script';
  const existingScript = document.getElementById(scriptId);

  if (!existingScript) {
    const script = document.createElement('script');
    script.id = scriptId;
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_API_KEY}&libraries=services,clusterer`;
    
    script.onload = () => {
      window.kakao.maps.load(() => {
        isLoaded.value = true;
      });
    };
    
    script.onerror = () => {
      console.error('카카오맵 스크립트 로드 실패');
    };
    
    document.head.appendChild(script);
  } else {
    // 스크립트 태그는 있는데 아직 로딩이 안 끝난 경우 (아주 드문 케이스)
    // 약간의 딜레이 후 다시 init 시도
    if (window.kakao && window.kakao.maps) {
       window.kakao.maps.load(() => { isLoaded.value = true; });
    } else {
       existingScript.onload = () => {
         window.kakao.maps.load(() => { isLoaded.value = true; });
       };
    }
  }
};

onMounted(() => {
  if (!KAKAO_API_KEY) {
    console.error('API Key가 없습니다. .env 파일을 확인해주세요.');
    return;
  }
  initMap();
});
</script>

<template>
  <div class="w-full h-full relative">
    <!-- 지도가 로드되면 내부 컴포넌트(BakeryMap) 표시 -->
    <slot v-if="isLoaded"></slot>
    
    <!-- 로딩 중일 때 표시할 화면 -->
    <div v-else class="w-full h-full flex flex-col items-center justify-center bg-gray-50 absolute top-0 left-0 z-10">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#1D4E45]"></div>
      <span class="text-gray-500 text-sm mt-2 font-medium">지도 준비 중...</span>
    </div>
  </div>
</template>