<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  bakeries: { type: Array, required: true },
  selectedBakery: { type: Object, default: null }
});

const emit = defineEmits(['select-marker']);
const mapContainer = ref(null);
let mapInstance = null;
let markers = [];
let currentLocationOverlay = null; // 현재 위치 표시용 오버레이

// 1. 지도 초기화
const initMap = () => {
  const options = {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780),
    level: 7
  };
  mapInstance = new window.kakao.maps.Map(mapContainer.value, options);
  
  if (props.bakeries.length > 0) {
    updateMarkers();
  }
};

const updateMarkers = () => {
  if (!mapInstance) return;

  markers.forEach(m => m.setMap(null));
  markers = [];

  props.bakeries.forEach((bakery) => {
    const position = new window.kakao.maps.LatLng(bakery.lat, bakery.lng);
    const imageSrc = 'https://cdn-icons-png.flaticon.com/512/3081/3081903.png';
    const imageSize = new window.kakao.maps.Size(40, 40);
    const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize);

    const marker = new window.kakao.maps.Marker({
      map: mapInstance,
      position: position,
      title: bakery.name,
      image: markerImage,
      clickable: true
    });

    window.kakao.maps.event.addListener(marker, 'click', () => {
      emit('select-marker', bakery);
      panTo(position);
    });

    markers.push(marker);
  });
};

const panTo = (latLng) => {
  mapInstance.panTo(latLng);
};

// ✅ [추가] 현재 위치로 이동하는 함수
const moveToCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert('이 브라우저에서는 위치 정보를 사용할 수 없습니다.');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const locPosition = new window.kakao.maps.LatLng(lat, lng);

      // 1. 지도 이동
      panTo(locPosition);

      // 2. 기존 내 위치 마커 제거
      if (currentLocationOverlay) {
        currentLocationOverlay.setMap(null);
      }

      // 3. 내 위치 표시 (파동치는 파란 점)
      const content = `
        <div class="my-location-marker">
          <div class="pulse"></div>
          <div class="dot"></div>
        </div>
      `;

      currentLocationOverlay = new window.kakao.maps.CustomOverlay({
        map: mapInstance,
        position: locPosition,
        content: content,
        zIndex: 5
      });
      
      // (선택) 레벨을 조금 확대해서 보여줌
      mapInstance.setLevel(4);
    },
    (error) => {
      console.error(error);
      alert('위치 정보를 가져올 수 없습니다. 위치 권한을 확인해주세요.');
    }
  );
};

// 부모 컴포넌트에서 이 함수를 쓸 수 있게 공개
defineExpose({ moveToCurrentLocation });

watch(() => props.bakeries, () => updateMarkers(), { deep: true });
watch(() => props.selectedBakery, (newVal) => {
  if (newVal && mapInstance) {
    const moveLatLon = new window.kakao.maps.LatLng(newVal.lat, newVal.lng);
    panTo(moveLatLon);
  }
});

onMounted(() => {
  initMap();
});
</script>

<template>
  <div ref="mapContainer" class="w-full h-full bg-gray-100"></div>
</template>

<style>
/* 현재 위치 마커 스타일 (전역 적용) */
.my-location-marker {
  position: relative;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.my-location-marker .dot {
  width: 12px;
  height: 12px;
  background-color: #3b82f6; /* Blue-500 */
  border: 2px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  z-index: 2;
}

.my-location-marker .pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(59, 130, 246, 0.4);
  border-radius: 50%;
  animation: pulse-ring 1.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
  z-index: 1;
}

@keyframes pulse-ring {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}
</style>