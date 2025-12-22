<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import KakaoMapLoader from '@/components/map/KakaoMapLoader.vue';
import BakeryMap from '@/components/map/BakeryMap.vue';
import { Search, MapPin, Star, Heart, Navigation, ThumbsUp, Home, Map as MapIcon, BookOpen, User, ChevronLeft, ChevronRight } from 'lucide-vue-next';

const router = useRouter();

// 데이터를 빈 배열로 초기화
const bakeries = ref([]);
const isLoading = ref(false);

const selectedBakery = ref(null);
const currentHotBakery = ref(null);
const isListOpen = ref(true); // 사이드바 토글 상태
const currentTab = ref('map'); // 현재 탭 상태

// 지도 컴포넌트 제어용 ref
const mapRef = ref(null);

// 기분/상황별 필터
const moods = [
  { label: "☁️ 우울할 땐", keyword: "달달함" },
  { label: "🤯 스트레스", keyword: "매콤" },
  { label: "☕ 브런치", keyword: "담백함" },
  { label: "❤️ 데이트", keyword: "데이트" },
];

watch(isListOpen, async () => {
  await nextTick();
  setTimeout(() => {
    mapRef.value?.relayout?.();
  }, 350);
});

// ✅ [추가] 좌표가 없는 데이터들의 주소를 이용해 좌표를 채워주는 함수
const fillMissingCoordinates = async () => {
  // 1. 카카오맵 서비스 라이브러리 로드 대기 (최대 5초)
  let attempts = 0;
  while ((!window.kakao || !window.kakao.maps || !window.kakao.maps.services) && attempts < 10) {
    await new Promise(resolve => setTimeout(resolve, 500));
    attempts++;
  }

  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) {
    console.warn("⚠️ 카카오맵 Geocoder를 사용할 수 없습니다.");
    return;
  }

  const geocoder = new window.kakao.maps.services.Geocoder();
  let updatedCount = 0;

  console.log("🛠️ 좌표 보정 작업 시작 (주소 -> 좌표 변환)");

  // 2. 좌표가 없는 빵집들만 주소 검색 수행
  bakeries.value.forEach((bakery) => {
    // 좌표가 유효하지 않고(0 또는 null), 주소가 있는 경우
    if ((!bakery.lat || !bakery.lng) && bakery.address) {
      geocoder.addressSearch(bakery.address, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          // 좌표 업데이트 (Vue 반응성 덕분에 지도에도 자동 반영됨)
          bakery.lat = parseFloat(result[0].y);
          bakery.lng = parseFloat(result[0].x);
          updatedCount++;
          // console.log(`📍 좌표 변환 성공: ${bakery.name}`); 
        }
      });
    }
  });
};

// ✅ [수정됨] Django API 데이터 매핑 및 좌표 보정 호출
const fetchBakeries = async () => {
  if (isLoading.value) return;
  isLoading.value = true;

  try {
    const response = await axios.get('http://127.0.0.1:8000/stores/');
    
    // 데이터 구조 확인
    const rawData = Array.isArray(response.data) ? response.data : (response.data.results || []);
    const limitedData = rawData.slice(0, 50);

    bakeries.value = limitedData.map((store, index) => {
      // 1. 데이터 위치 파악 (Django DRF vs 기본 Serializer)
      const fields = store.fields || store;
      const pk = store.pk || store.id; 

      // 2. 좌표 추출 (없으면 null로 설정하여 보정 함수가 작동하게 함)
      const rawLat = fields.latitude || fields.lat;
      const rawLng = fields.longitude || fields.lng;

      return {
        id: pk, 
        name: fields.name,
        // 좌표가 없으면 0이나 null 할당
        lat: rawLat ? parseFloat(String(rawLat).trim()) : null,  
        lng: rawLng ? parseFloat(String(rawLng).trim()) : null, 
        address: fields.address || '',
        rating: parseFloat(fields.avg_rating) || 0.0, 
        image: `https://source.unsplash.com/random/400x300/?bakery&sig=${pk}`,
        tags: (fields.representative_tags && String(fields.representative_tags).trim() !== "") 
              ? String(fields.representative_tags).split(',') 
              : ['맛있는빵집', '추천'] 
      };
    });

    // 3. ⭐️ 좌표가 비어있는 데이터들을 위해 주소 기반 좌표 검색 실행
    fillMissingCoordinates();

    // 초기 추천 설정
    if (bakeries.value.length > 0) {
      pickRandomHotBakery();
    }
    
  } catch (error) {
    console.error('빵집 데이터를 불러오는데 실패했습니다:', error);
  } finally {
    isLoading.value = false;
  }
};

const handleMarkerClick = (bakery) => {
  selectedBakery.value = bakery;
  if (!isListOpen.value) isListOpen.value = true;
};

const handleListClick = (bakery) => {
  selectedBakery.value = bakery;
};

const filterByMood = (keyword) => {
  console.log("Filtering by:", keyword);
};

const pickRandomHotBakery = () => {
  if (bakeries.value.length === 0) return;
  const randomIndex = Math.floor(Math.random() * bakeries.value.length);
  currentHotBakery.value = bakeries.value[randomIndex];
};

const handleMyLocationClick = () => {
  if (mapRef.value) {
    mapRef.value.moveToCurrentLocation();
  }
};

const refreshMap = () => {
  location.reload();
};

onMounted(() => {
  fetchBakeries();
});
</script>

<template>
  <KakaoMapLoader>
    <!-- fixed inset-0 z-50: 화면 전체를 덮도록 설정 -->
    <div class="fixed inset-0 z-50 flex w-full h-full bg-[#F9F7F2] overflow-hidden">
      
      <!-- 0. 세로형 네비게이션 바 -->
      <nav class="w-[72px] h-full bg-[#1D4E45] flex flex-col items-center py-6 z-50 shrink-0 shadow-lg text-white/70">
        <router-link :to="{ name: 'home' }" class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center text-xl mb-10 cursor-pointer hover:bg-white/20 transition-colors text-white no-underline">
          🥐
        </router-link>

        <div class="flex flex-col gap-8 w-full">
          <router-link :to="{ name: 'home' }" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group no-underline text-white/70">
            <Home class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">홈</span>
          </router-link>
          
          <button @click="refreshMap" class="flex flex-col items-center gap-1 text-orange-400 scale-110 transition-all group relative">
            <MapIcon class="w-6 h-6 stroke-[2.5px]" />
            <span class="text-[10px] font-medium">지도</span>
            <div class="absolute -right-[18px] top-1/2 -translate-y-1/2 w-1 h-8 bg-orange-400 rounded-l-full"></div>
          </button>

          <router-link :to="{ name: 'community' }" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group no-underline text-white/70">
            <BookOpen class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">커뮤니티</span>
          </router-link>

           <router-link :to="{ name: 'mypage' }" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group no-underline text-white/70">
            <User class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">마이</span>
          </router-link>
        </div>

        <div class="mt-auto">
           <button class="w-10 h-10 rounded-full overflow-hidden border-2 border-white/20 hover:border-white transition-colors">
             <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="w-full h-full bg-white/10" />
           </button>
        </div>
      </nav>

      <!-- 1. 사이드바 -->
      <div 
        class="absolute md:relative z-20 h-full bg-white shadow-xl transition-all duration-300 flex flex-col border-r border-[#1D4E45]/10 left-[72px] md:left-0"
        :class="isListOpen ? 'w-[320px] md:w-[380px] translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-0 overflow-hidden'"
      >
        <!-- 사이드바 헤더 -->
        <div class="p-5 border-b border-gray-100 bg-white shrink-0 z-10">
          <div class="relative mb-4">
            <input 
              type="text" 
              placeholder="장소, 주소, 빵 검색" 
              class="w-full pl-11 pr-4 py-3 bg-[#F9F7F2] rounded-lg border-none outline-none text-[#4A4036] placeholder-gray-400 focus:ring-2 focus:ring-[#1D4E45]/20 transition-all font-medium"
            />
            <Search class="absolute left-3.5 top-3.5 w-5 h-5 text-[#1D4E45]" />
          </div>

          <div class="flex gap-2 overflow-x-auto hide-scrollbar pb-1">
            <button 
              v-for="mood in moods" 
              :key="mood.label"
              @click="filterByMood(mood.keyword)"
              class="flex-shrink-0 px-3 py-1.5 rounded-full border border-gray-200 text-xs font-bold text-gray-600 hover:bg-[#1D4E45] hover:text-white hover:border-[#1D4E45] transition-all whitespace-nowrap"
            >
              {{ mood.label }}
            </button>
          </div>
        </div>

        <!-- 리스트 목록 -->
        <div class="flex-1 overflow-y-auto p-5 space-y-6 hide-scrollbar bg-white">
          
          <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 gap-4">
            <div class="animate-spin rounded-full h-10 w-10 border-4 border-[#1D4E45] border-t-transparent"></div>
            <span class="text-sm text-gray-500">맛있는 빵집을 찾고 있어요...</span>
          </div>

          <div v-else>
            <!-- 추천 카드 -->
            <div v-if="currentHotBakery" class="bg-gradient-to-br from-[#1D4E45] to-[#12352E] rounded-2xl p-5 text-white shadow-lg relative overflow-hidden group cursor-pointer mb-6" @click="handleListClick(currentHotBakery)">
               <div class="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>
               
               <div class="flex justify-between items-start mb-3 relative z-10">
                 <span class="px-2 py-1 bg-white/20 backdrop-blur rounded text-[10px] font-bold tracking-wider flex items-center gap-1">
                   <ThumbsUp class="w-3 h-3" /> 오늘의 추천
                 </span>
                 <button class="text-white/70 hover:text-white"><Heart class="w-4 h-4" /></button>
               </div>
               
               <div class="flex gap-4 items-center relative z-10">
                 <div class="w-16 h-16 rounded-full bg-white/10 border-2 border-white/20 overflow-hidden shrink-0">
                   <img :src="currentHotBakery.image" class="w-full h-full object-cover" />
                 </div>
                 <div>
                   <h3 class="font-bold text-lg leading-tight mb-1">{{ currentHotBakery.name }}</h3>
                   <p class="text-xs text-white/70 truncate w-40">{{ currentHotBakery.address }}</p>
                   <div class="flex gap-2 mt-2 text-xs">
                     <span class="text-orange-300 font-bold">★ {{ currentHotBakery.rating }}</span>
                     <span class="text-white/50">#{{ currentHotBakery.tags[0] }}</span>
                   </div>
                 </div>
               </div>
            </div>

            <!-- 빵집 리스트 -->
            <div>
              <h3 class="font-bold text-[#4A4036] mb-3 text-sm px-1">
                내 주변 빵집 리스트 ({{ bakeries.length }}개)
              </h3>
              <div class="space-y-3">
                <div 
                  v-for="bakery in bakeries" 
                  :key="bakery.id"
                  @click="handleListClick(bakery)"
                  :class="[
                    'p-4 rounded-xl border transition-all cursor-pointer flex gap-3 hover:shadow-md',
                    selectedBakery?.id === bakery.id 
                      ? 'border-[#1D4E45] bg-[#F9F7F2] ring-1 ring-[#1D4E45]/20' 
                      : 'border-gray-100 bg-white hover:border-[#1D4E45]/30'
                  ]"
                >
                  <div class="w-20 h-20 rounded-lg bg-gray-100 overflow-hidden shrink-0">
                    <img :src="bakery.image" class="w-full h-full object-cover" />
                  </div>
                  
                  <div class="flex-1 min-w-0 flex flex-col justify-between">
                    <div class="flex justify-between items-start">
                      <h4 class="font-bold text-[#1D4E45] truncate">{{ bakery.name }}</h4>
                      <span class="text-xs font-bold text-orange-500 flex items-center gap-0.5">
                        <Star class="w-3 h-3 fill-current" /> {{ bakery.rating }}
                      </span>
                    </div>
                    <p class="text-xs text-gray-500 line-clamp-1">{{ bakery.address }}</p>
                    <div class="flex gap-1 mt-1">
                      <span v-for="tag in bakery.tags" :key="tag" class="px-1.5 py-0.5 bg-gray-100 rounded text-[10px] text-gray-500 font-medium">#{{ tag }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 접기/펼치기 버튼 -->
      <button 
        @click="isListOpen = !isListOpen"
        class="absolute top-1/2 -translate-y-1/2 z-30 w-6 h-12 bg-white border border-l-0 border-gray-200 rounded-r-lg flex items-center justify-center text-gray-400 shadow-md hover:text-[#1D4E45] transition-all duration-300"
        :class="isListOpen ? 'left-[392px] md:left-[452px]' : 'left-[72px]'"
      >
        <ChevronLeft v-if="isListOpen" class="w-4 h-4" />
        <ChevronRight v-else class="w-4 h-4" />
      </button>

      <!-- 2. 지도 영역 -->
      <div class="flex-1 h-full relative z-0">
        <BakeryMap 
          ref="mapRef"
          :bakeries="bakeries" 
          :selected-bakery="selectedBakery"
          @select-marker="handleMarkerClick"
        />
        
        <div class="absolute top-4 right-4 flex flex-col gap-2 z-10">
          <button 
            @click="handleMyLocationClick" 
            class="bg-white p-2.5 rounded shadow-md text-gray-600 hover:text-[#1D4E45] hover:bg-gray-50 transition-colors" 
            title="내 위치"
          >
            <Navigation class="w-5 h-5" />
          </button>
          
          <button class="bg-white p-2.5 rounded shadow-md text-gray-600 hover:text-[#1D4E45] hover:bg-gray-50 transition-colors" title="지도 뷰 변경">
             <MapIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

    </div>
  </KakaoMapLoader>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>