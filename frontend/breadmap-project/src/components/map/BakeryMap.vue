<script setup>
import { ref, onMounted, watch } from 'vue';

const props = defineProps({
  bakeries: { type: Array, required: true, default: () => [] },
  selectedBakery: { type: Object, default: null }
});

const emit = defineEmits(['select-marker', 'map-moved']);
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
    center: new window.kakao.maps.LatLng(37.5665, 126.9780),
    level: 5,
    draggable: true, // ✅ 마우스 드래그 이동 허용
    scrollwheel: true // ✅ 마우스 휠 확대/축소 허용
  };

  mapInstance = new window.kakao.maps.Map(mapContainer.value, options);
  
  // 지도 이동 이벤트
  window.kakao.maps.event.addListener(mapInstance, 'dragend', () => {
    emit('map-moved');
  });
  window.kakao.maps.event.addListener(mapInstance, 'zoom_changed', () => {
    emit('map-moved');
  });

  if (props.bakeries && props.bakeries.length > 0) {
    updateMarkers();
  }
};

// 2. 마커 업데이트
const updateMarkers = () => {
  if (!mapInstance || !window.kakao) return;

  markers.forEach(marker => marker.setMap(null));
  markers = [];

  // 빵 마커 이미지
  const imageSrc = 'https://cdn-icons-png.flaticon.com/512/992/992747.png'; 
  const imageSize = new window.kakao.maps.Size(40, 40); 
  const imageOption = { offset: new window.kakao.maps.Point(20, 35) }; 
  const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

  props.bakeries.forEach((bakery) => {
    const lat = parseFloat(bakery.lat);
    const lng = parseFloat(bakery.lng);

    if (isNaN(lat) || isNaN(lng) || lat === 0 || lng === 0) return;

    const markerPosition = new window.kakao.maps.LatLng(lat, lng);

    const marker = new window.kakao.maps.Marker({
      position: markerPosition,
      image: markerImage
    });

    marker.setMap(mapInstance);

    window.kakao.maps.event.addListener(marker, 'click', () => {
      emit('select-marker', bakery);
    });

    markers.push(marker);
  });

  // ✅ [수정] 지도를 전체 마커 범위(bounds)로 넓히지 않고, 가장 가까운(첫번째) 빵집으로 중심만 이동
  if (props.bakeries.length > 0) {
    const nearest = props.bakeries[0];
    const nLat = parseFloat(nearest.lat);
    const nLng = parseFloat(nearest.lng);
    
    if (!isNaN(nLat) && !isNaN(nLng) && nLat !== 0 && nLng !== 0) {
      const moveLatLon = new window.kakao.maps.LatLng(nLat, nLng);
      // 줌 레벨을 유지하며 부드럽게 이동
      mapInstance.panTo(moveLatLon);
    }
  }
};

// ✅ [수정] 지도 레이아웃 재계산 후 이동 (화면 깨짐/이동 불가 방지)
const panTo = (lat, lng) => {
  if (mapInstance && window.kakao) {
    const nLat = parseFloat(lat);
    const nLng = parseFloat(lng);
    if (isNaN(nLat) || isNaN(nLng)) return;
    
    // 지도가 표시되는 div 크기가 변경되었을 수 있으므로 레이아웃 갱신
    mapInstance.relayout();
    
    const moveLatLon = new window.kakao.maps.LatLng(nLat, nLng);
    mapInstance.panTo(moveLatLon);
  }
};

const moveToCurrentLocation = () => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      alert('위치 정보를 사용할 수 없습니다.');
      reject();
      return;
    }
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;
      const locPosition = new window.kakao.maps.LatLng(lat, lng);

      if (mapInstance) {
        mapInstance.relayout(); // 이동 전 레이아웃 갱신
        mapInstance.panTo(locPosition);
      }
      
      if (currentLocationOverlay) currentLocationOverlay.setMap(null);
      
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
      
      resolve({ lat, lng });
    }, (err) => {
      reject(err);
    });
  });
};

const relayout = () => {
  if (mapInstance) mapInstance.relayout();
};

const getMapCenter = () => {
  if (mapInstance) {
    const center = mapInstance.getCenter();
    return { lat: center.getLat(), lng: center.getLng() };
  }
  return null;
};

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

defineExpose({ moveToCurrentLocation, relayout, getMapCenter, panTo });
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