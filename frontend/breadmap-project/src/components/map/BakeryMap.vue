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

// 1. 지도 초기화
const initMap = () => {
  // KakaoMapLoader 덕분에 window.kakao.maps가 무조건 존재하는 상태임
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

  // 기존 마커 제거
  markers.forEach(m => m.setMap(null));
  markers = [];

  props.bakeries.forEach((bakery) => {
    const position = new window.kakao.maps.LatLng(bakery.lat, bakery.lng);

    // 심플한 빵 아이콘 마커
    const imageSrc = 'https://cdn-icons-png.flaticon.com/512/3081/3081903.png';
    const imageSize = new window.kakao.maps.Size(40, 40); // 적당한 크기
    const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize);

    const marker = new window.kakao.maps.Marker({
      map: mapInstance,
      position: position,
      title: bakery.name,
      image: markerImage,
      clickable: true
    });

    // 마커 클릭 시 이벤트 발생
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

watch(() => props.bakeries, () => {
  updateMarkers();
}, { deep: true });

// 선택된 빵집이 바뀌면 지도 이동
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

<style scoped>
/* 지도 컨테이너 스타일 */
</style>