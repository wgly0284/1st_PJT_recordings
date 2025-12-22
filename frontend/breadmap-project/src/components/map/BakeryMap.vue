<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  bakeries: { type: Array, required: true, default: () => [] },
  selectedBakery: { type: Object, default: null }
});

const emit = defineEmits(['select-marker']);
const mapContainer = ref(null);
let mapInstance = null;
let markers = [];
let currentLocationOverlay = null;

// 1. 지도 초기화
const initMap = () => {
  if (!mapContainer.value || !window.kakao || !window.kakao.maps) {
    setTimeout(initMap, 100);
    return;
  }

  const options = {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780), // 기본값: 서울
    level: 5
  };

  mapInstance = new window.kakao.maps.Map(mapContainer.value, options);
  console.log("✅ 카카오맵 인스턴스 생성 완료");

  // 초기 데이터가 있다면 마커 표시 시도
  if (props.bakeries && props.bakeries.length > 0) {
    updateMarkers();
  }
};

// 2. 마커 업데이트
const updateMarkers = () => {
  if (!mapInstance || !window.kakao) return;

  console.log(`📍 마커 업데이트 시작. 데이터 개수: ${props.bakeries.length}개`);

  // 1) 기존 마커 싹 지우기
  markers.forEach(marker => marker.setMap(null));
  markers = [];

  const bounds = new window.kakao.maps.LatLngBounds();
  let hasValidMarker = false;

  // ⭐️ [변경] 마커 이미지를 '빵'으로 변경! 🍞
  // 귀여운 식빵 아이콘 사용 (원하시는 다른 이미지 URL이 있다면 여기를 교체하시면 됩니다)
  const imageSrc = 'https://cdn-icons-png.flaticon.com/512/992/992747.png'; 
  
  // 이미지 크기 설정 (너무 크지 않게 40x40 정도로 조정)
  const imageSize = new window.kakao.maps.Size(40, 40); 
  
  // 이미지 옵션: 마커의 좌표와 일치시킬 이미지 안에서의 좌표 (이미지의 중앙 하단이 지도 좌표에 오도록 설정)
  const imageOption = { offset: new window.kakao.maps.Point(20, 35) }; 
  
  const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

  props.bakeries.forEach((bakery, index) => {
    // lat/lng 변수 처리
    const rawLat = bakery.lat || bakery.latitude; 
    const rawLng = bakery.lng || bakery.longitude;

    const lat = parseFloat(rawLat);
    const lng = parseFloat(rawLng);

    if (isNaN(lat) || isNaN(lng) || lat === 0 || lng === 0) {
      // console.warn(`⚠️ [${index}번 데이터] 좌표값 없음 (NaN).`, bakery);
      return; 
    }

    const markerPosition = new window.kakao.maps.LatLng(lat, lng);

    // 마커 생성
    const marker = new window.kakao.maps.Marker({
      position: markerPosition,
      image: markerImage // 빵 마커 이미지 적용
    });

    // 지도에 올리기
    marker.setMap(mapInstance);

    // 클릭 이벤트
    window.kakao.maps.event.addListener(marker, 'click', () => {
      console.log(`🖱️ 빵 마커 클릭됨: ${bakery.name}`);
      emit('select-marker', bakery);
    });

    markers.push(marker);
    bounds.extend(markerPosition);
    hasValidMarker = true;
  });

  // 3) 마커가 하나라도 찍혔으면 지도 범위를 거기로 이동
  if (hasValidMarker) {
    console.log("🔭 지도를 마커 위치로 이동시킵니다.");
    mapInstance.setBounds(bounds);
  } else {
    console.warn("❌ 표시할 수 있는 마커가 하나도 없습니다.");
  }
};

// 좌표 이동 함수
const panTo = (lat, lng) => {
  if (mapInstance && window.kakao) {
    const nLat = parseFloat(lat);
    const nLng = parseFloat(lng);
    
    if (isNaN(nLat) || isNaN(nLng)) return;

    mapInstance.relayout();
    const moveLatLon = new window.kakao.maps.LatLng(nLat, nLng);
    mapInstance.panTo(moveLatLon);
  }
};

// 현재 위치
const moveToCurrentLocation = () => {
  if (!navigator.geolocation) {
    alert('위치 정보를 사용할 수 없습니다.');
    return;
  }
  navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const locPosition = new window.kakao.maps.LatLng(lat, lng);

      if (mapInstance) {
        mapInstance.relayout();
        mapInstance.panTo(locPosition);
        mapInstance.setLevel(4);
      }
      
      if (currentLocationOverlay) {
        currentLocationOverlay.setMap(null);
      }

      const content = `
        <div style="position: relative; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
          <div style="position: absolute; width: 100%; height: 100%; background-color: rgba(59, 130, 246, 0.4); border-radius: 50%; animation: pulse 1.5s infinite;"></div>
          <div style="width: 12px; height: 12px; background-color: #3b82f6; border: 2px solid white; border-radius: 50%; z-index: 10;"></div>
        </div>
      `;

      currentLocationOverlay = new window.kakao.maps.CustomOverlay({
        map: mapInstance,
        position: locPosition,
        content: content,
        zIndex: 5
      });
  });
};

const relayout = () => {
  if (mapInstance) mapInstance.relayout();
};

// 데이터 변경 감지
watch(() => props.bakeries, (newVal) => {
  if (mapInstance && newVal && newVal.length > 0) {
    updateMarkers();
  }
}, { deep: true, immediate: true });

watch(() => props.selectedBakery, (newVal) => {
  if (newVal && mapInstance) {
    const lat = newVal.lat || newVal.latitude;
    const lng = newVal.lng || newVal.longitude;
    setTimeout(() => panTo(lat, lng), 150);
  }
});

onMounted(() => {
  setTimeout(initMap, 200);
});

defineExpose({ moveToCurrentLocation, relayout });
</script>

<template>
  <div ref="mapContainer" class="w-full h-full min-h-[400px] bg-gray-100 relative z-0"></div>
</template>

<style>
@keyframes pulse {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2.5); opacity: 0; }
}
</style>