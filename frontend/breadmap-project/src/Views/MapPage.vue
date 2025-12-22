<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import KakaoMapLoader from '@/components/map/KakaoMapLoader.vue';
import BakeryMap from '@/components/map/BakeryMap.vue';
import { Search, MapPin, Star, Heart, Navigation, ThumbsUp, Home, Map as MapIcon, BookOpen, User, ChevronLeft, ChevronRight, RotateCw } from 'lucide-vue-next';

const router = useRouter();

// 데이터 상태
const bakeries = ref([]); 
const isLoading = ref(false);
const searchKeyword = ref('');

const selectedBakery = ref(null);
const currentHotBakery = ref(null); 
const isListOpen = ref(true); 
const currentTab = ref('map'); 
const mapRef = ref(null);

const showReSearchBtn = ref(false);
const isFallbackSearch = ref(false);

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

// 거리 계산 함수
const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
  const R = 6371; 
  const dLat = deg2rad(lat2 - lat1);  
  const dLon = deg2rad(lon2 - lon1); 
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2); 
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)); 
  const d = R * c; 
  return d;
}

const deg2rad = (deg) => {
  return deg * (Math.PI/180)
}

const fillMissingCoordinates = async () => {
  let attempts = 0;
  while ((!window.kakao || !window.kakao.maps || !window.kakao.maps.services) && attempts < 10) {
    await new Promise(resolve => setTimeout(resolve, 500));
    attempts++;
  }

  if (!window.kakao || !window.kakao.maps || !window.kakao.maps.services) return;

  const geocoder = new window.kakao.maps.services.Geocoder();

  bakeries.value.forEach((bakery) => {
    if ((!bakery.lat || !bakery.lng) && bakery.address) {
      geocoder.addressSearch(bakery.address, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          bakery.lat = parseFloat(result[0].y);
          bakery.lng = parseFloat(result[0].x);
        }
      });
    }
  });
};

// 데이터 로드 함수
const fetchBakeries = async (keyword = '', centerLat = null, centerLng = null) => {
  if (isLoading.value) return;
  isLoading.value = true;
  
  showReSearchBtn.value = false;
  isFallbackSearch.value = false; 

  try {
    const params = {};
    if (keyword) params.search = keyword;
    
    const response = await axios.get('http://127.0.0.1:8000/stores/', { params });
    const rawData = Array.isArray(response.data) ? response.data : (response.data.results || []);
    
    let mappedData = rawData.map((store) => {
      const fields = store.fields || store;
      const pk = store.pk || store.id; 
      const rawLat = fields.latitude || fields.lat;
      const rawLng = fields.longitude || fields.lng;
      const lat = rawLat ? parseFloat(String(rawLat).trim()) : null;
      const lng = rawLng ? parseFloat(String(rawLng).trim()) : null;

      return {
        id: pk, 
        name: fields.name,
        lat: lat, 
        lng: lng,
        address: fields.address || '',
        rating: parseFloat(fields.avg_rating) || 0.0, 
        image: `https://source.unsplash.com/random/400x300/?bakery&sig=${pk}`,
        tags: (fields.representative_tags && String(fields.representative_tags).trim() !== "") 
              ? String(fields.representative_tags).split(',') 
              : ['맛있는빵집', '추천'],
        distance: 0 
      };
    });

    if (centerLat && centerLng) {
      mappedData = mappedData.map(b => {
        if (b.lat && b.lng) {
          b.distance = getDistanceFromLatLonInKm(centerLat, centerLng, b.lat, b.lng);
        } else {
          b.distance = 99999; 
        }
        return b;
      });

      mappedData.sort((a, b) => a.distance - b.distance);

      const nearbyData = mappedData.filter(b => b.distance <= 10);

      if (nearbyData.length > 0) {
        bakeries.value = nearbyData.slice(0, 50);
      } else {
        bakeries.value = mappedData.slice(0, 20); 
        isFallbackSearch.value = true; 
      }
    } else {
      bakeries.value = mappedData.slice(0, 50);
    }

    fillMissingCoordinates();

    if (bakeries.value.length > 0) {
      if (!currentHotBakery.value) pickRandomHotBakery();
      if (keyword) isListOpen.value = true;
      
      // ✅ [핵심 수정] 가장 가까운 빵집(첫번째 결과)으로 지도 이동
      const nearest = bakeries.value[0];
      if (mapRef.value && nearest.lat && nearest.lng) {
        // 약간의 딜레이를 주어 지도가 준비된 후 이동하도록 함
        setTimeout(() => {
          mapRef.value.panTo(nearest.lat, nearest.lng);
        }, 300);
      }
    } else {
      if (keyword) alert(`'${keyword}'에 대한 검색 결과가 없습니다.`);
    }
    
  } catch (error) {
    console.error('빵집 데이터 로드 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

const searchStores = async () => {
  if (!searchKeyword.value.trim()) {
    alert("검색어를 입력해주세요!");
    return;
  }
  
  if (mapRef.value) {
    let center = mapRef.value.getMapCenter();
    
    if (!center && navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
            fetchBakeries(searchKeyword.value, pos.coords.latitude, pos.coords.longitude);
        }, () => {
            fetchBakeries(searchKeyword.value); 
        });
    } else if (center) {
        fetchBakeries(searchKeyword.value, center.lat, center.lng);
    } else {
        fetchBakeries(searchKeyword.value);
    }
  } else {
    fetchBakeries(searchKeyword.value);
  }
};

const handleReSearchInMap = () => {
  if (mapRef.value) {
    const center = mapRef.value.getMapCenter();
    if (center) {
      fetchBakeries(searchKeyword.value, center.lat, center.lng);
      showReSearchBtn.value = false; 
    }
  }
};

const handleMapMoved = () => {
  showReSearchBtn.value = true;
};

const handleMarkerClick = (bakery) => {
  selectedBakery.value = bakery;
  if (!isListOpen.value) isListOpen.value = true;
};

const handleListClick = (bakery) => {
  selectedBakery.value = bakery;
};

const filterByMood = (keyword) => {
  searchKeyword.value = keyword;
  searchStores();
};

const pickRandomHotBakery = () => {
  if (bakeries.value.length === 0) return;
  const randomIndex = Math.floor(Math.random() * bakeries.value.length);
  currentHotBakery.value = bakeries.value[randomIndex];
};

const handleMyLocationClick = () => {
  if (mapRef.value) {
    mapRef.value.moveToCurrentLocation().then(pos => {
      // 내 위치로 이동만 하고, 재검색은 사용자 선택에 맡김 (버튼이 뜨므로)
      // 원하시면 여기서 fetchBakeries 호출 가능
    });
  }
};

const refreshMap = () => {
  location.reload();
};

onMounted(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      
      // ✅ 초기 로딩 시 검색 실행
      // 이후 fetchBakeries 내부에서 가장 가까운 빵집으로 panTo 실행됨
      fetchBakeries('', lat, lng);
      
      // ⚠️ 기존의 moveToCurrentLocation 호출 제거함 (사용자 위치로 강제 이동 방지)

    }, (err) => {
      fetchBakeries('', 37.5665, 126.9780); 
    });
  } else {
    fetchBakeries('', 37.5665, 126.9780);
  }
});
</script>

<template>
  <KakaoMapLoader>
    <div class="fixed inset-0 z-50 flex w-full h-full bg-[#F9F7F2] overflow-hidden">
      
      <!-- GNB -->
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

      <!-- 사이드바 -->
      <div 
        class="absolute md:relative z-20 h-full bg-white shadow-xl transition-all duration-300 flex flex-col border-r border-[#1D4E45]/10 left-[72px] md:left-0"
        :class="isListOpen ? 'w-[320px] md:w-[380px] translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-0 overflow-hidden'"
      >
        <div class="p-5 border-b border-gray-100 bg-white shrink-0 z-10">
          <div class="relative mb-4 group">
            <input 
              v-model="searchKeyword"
              @keyup.enter="searchStores"
              type="text" 
              placeholder="지역, 빵집 이름 검색" 
              class="w-full pl-11 pr-4 py-3 bg-[#F9F7F2] rounded-lg border-none outline-none text-[#4A4036] placeholder-gray-400 focus:ring-2 focus:ring-[#1D4E45]/20 transition-all font-medium"
            />
            <Search 
              @click="searchStores"
              class="absolute left-3.5 top-3.5 w-5 h-5 text-[#1D4E45] cursor-pointer hover:scale-110 transition-transform" 
            />
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

        <div class="flex-1 overflow-y-auto p-5 space-y-6 hide-scrollbar bg-white">
          <div v-if="isLoading" class="flex flex-col items-center justify-center py-20 gap-4">
            <div class="animate-spin rounded-full h-10 w-10 border-4 border-[#1D4E45] border-t-transparent"></div>
            <span class="text-sm text-gray-500">맛있는 빵집을 찾고 있어요...</span>
          </div>

          <div v-else-if="bakeries.length === 0" class="flex flex-col items-center justify-center py-20 text-center opacity-60">
            <Search class="w-12 h-12 text-gray-300 mb-2" />
            <p class="text-sm text-gray-500">검색 결과가 없습니다.</p>
          </div>

          <div v-else>
            <div v-if="isFallbackSearch" class="mb-4 p-3 bg-orange-50 border border-orange-100 rounded-xl text-xs text-orange-700 font-medium text-center">
              📍 주변 10km 내 결과가 없어<br>가장 가까운 곳을 찾아보았어요!
            </div>

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

            <div>
              <h3 class="font-bold text-[#4A4036] mb-3 text-sm px-1 flex justify-between items-center">
                <span>{{ isFallbackSearch ? '추천 빵집 리스트' : '주변 빵집 리스트' }}</span>
                <span class="text-xs font-normal text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{{ bakeries.length }}개</span>
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
                      <span class="text-xs font-bold text-orange-500 flex items-center gap-0.5"><Star class="w-3 h-3 fill-current" /> {{ bakery.rating }}</span>
                    </div>
                    <p class="text-xs text-gray-500 line-clamp-1">{{ bakery.address }}</p>
                    <div class="flex justify-between items-end mt-1">
                      <div class="flex gap-1">
                        <span v-for="tag in bakery.tags.slice(0, 2)" :key="tag" class="px-1.5 py-0.5 bg-gray-100 rounded text-[10px] text-gray-500 font-medium">#{{ tag }}</span>
                      </div>
                      <span v-if="bakery.distance < 9999" class="text-xs font-bold" :class="bakery.distance > 10 ? 'text-orange-500' : 'text-[#1D4E45]'">
                        {{ bakery.distance < 1 ? (bakery.distance * 1000).toFixed(0) + 'm' : bakery.distance.toFixed(1) + 'km' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button @click="isListOpen = !isListOpen" class="absolute top-1/2 -translate-y-1/2 z-30 w-6 h-12 bg-white border border-l-0 border-gray-200 rounded-r-lg flex items-center justify-center text-gray-400 shadow-md hover:text-[#1D4E45] transition-all duration-300" :class="isListOpen ? 'left-[392px] md:left-[452px]' : 'left-[72px]'">
        <ChevronLeft v-if="isListOpen" class="w-4 h-4" />
        <ChevronRight v-else class="w-4 h-4" />
      </button>

      <!-- 지도 영역 -->
      <div class="flex-1 h-full relative z-0">
        <div v-if="showReSearchBtn" class="absolute top-4 left-1/2 -translate-x-1/2 z-20 animate-bounce-in">
          <button 
            @click="handleReSearchInMap"
            class="flex items-center gap-2 bg-white text-[#1D4E45] px-5 py-2.5 rounded-full shadow-lg border border-[#1D4E45]/10 font-bold hover:bg-[#1D4E45] hover:text-white transition-all transform hover:scale-105"
          >
            <RotateCw class="w-4 h-4" />
            현 지도에서 검색
          </button>
        </div>

        <BakeryMap 
          ref="mapRef"
          :bakeries="bakeries" 
          :selected-bakery="selectedBakery"
          @select-marker="handleMarkerClick"
          @map-moved="handleMapMoved" 
        />
        
        <div class="absolute top-4 right-4 flex flex-col gap-2 z-10">
          <button @click="handleMyLocationClick" class="bg-white p-2.5 rounded shadow-md text-gray-600 hover:text-[#1D4E45] hover:bg-gray-50 transition-colors" title="내 위치">
            <Navigation class="w-5 h-5" />
          </button>
          <button class="bg-white p-2.5 rounded shadow-md text-gray-600 hover:text-[#1D4E45] hover:bg-gray-50 transition-colors" title="지도 뷰 변경">
             <MapPin class="w-5 h-5" />
          </button>
        </div>
      </div>

    </div>
  </KakaoMapLoader>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

@keyframes bounceIn {
  0% { transform: translate(-50%, -20px); opacity: 0; }
  50% { transform: translate(-50%, 5px); opacity: 1; }
  100% { transform: translate(-50%, 0); opacity: 1; }
}
.animate-bounce-in {
  animation: bounceIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
</style>