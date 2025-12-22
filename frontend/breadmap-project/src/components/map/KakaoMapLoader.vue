<script setup>
import { ref, onMounted } from 'vue';

const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;
const isLoaded = ref(false); // 지도가 준비되었는지 확인하는 상태 변수

const loadKakaoMap = () => {
  if (!KAKAO_API_KEY) {
    console.error('API Key is missing! Check .env.local file.');
    return Promise.reject('API Key is missing');
  }

  return new Promise((resolve, reject) => {
    // 이미 로드되어 있다면 바로 resolve (단, load함수 호출로 안전하게)
    if (window.kakao && window.kakao.maps) {
      window.kakao.maps.load(resolve);
      return;
    }

    const script = document.createElement('script');
    // 스크립트 로드 후 maps.load를 호출해야 LatLng 같은 생성자를 쓸 수 있음
    script.onload = () => window.kakao.maps.load(resolve);
    script.onerror = reject;
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_API_KEY}&libraries=services,clusterer`;
    document.head.appendChild(script);
  });
};

onMounted(async () => {
  try {
    await loadKakaoMap();
    isLoaded.value = true; // 로딩이 끝나면 true로 변경 -> 하위 컴포넌트 렌더링 시작
  } catch (error) {
    console.error('Failed to load Kakao Map:', error);
  }
});
</script>

<template>
  <!-- 지도가 로드된 후에만 내부 컴포넌트(슬롯)를 렌더링 -->
  <template v-if="isLoaded">
    <slot></slot>
  </template>
  <div v-else class="w-full h-full flex items-center justify-center bg-gray-50">
    <span class="text-gray-400 text-sm">지도를 불러오는 중...</span>
  </div>
</template>