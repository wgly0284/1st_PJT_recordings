<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import KakaoMapLoader from '@/components/map/KakaoMapLoader.vue';
import BakeryMap from '@/components/map/BakeryMap.vue';
import BakeryInfoCard from '@/components/map/BakeryInfoCard.vue';
import StoreReviewWrite from '@/components/map/StoreReviewWrite.vue';
import { Search, MapPin, Star, Heart, Navigation, ThumbsUp, Home, Map as MapIcon, BookOpen, User, ChevronLeft, ChevronRight, RotateCw } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

// 데이터 상태
const bakeries = ref([]);
const allBakeries = ref([]); // 전체 데이터 저장
const isLoading = ref(false);
const searchKeyword = ref('');
const displayLimit = ref(20); // 초기 표시 개수
const hasMore = ref(false); // 더 로드할 데이터가 있는지

const selectedBakery = ref(null);
const currentHotBakery = ref(null);
const isListOpen = ref(true);
const currentTab = ref('map');
const mapRef = ref(null);

const showReSearchBtn = ref(false);
const isFallbackSearch = ref(false);

// 프로필 데이터
const userProfile = ref(null);

// 캐릭터 이미지 매핑
const characterImages = {
  hamster: 'https://cdn-icons-png.flaticon.com/512/235/235394.png',
  bear: 'https://cdn-icons-png.flaticon.com/512/235/235388.png',
  lion: 'https://cdn-icons-png.flaticon.com/512/235/235352.png'
};

// 리뷰 작성 모달 상태
const showReviewWrite = ref(false);
const reviewStoreId = ref(null);
const reviewStoreName = ref('');

// 키워드 필터
const selectedMood = ref(null);
const moods = [
  { label: "☁️ 우울할 땐", keyword: "달달한" },
  { label: "😊 기분 좋을 땐", keyword: "상큼한" },
  { label: "☕ 브런치", keyword: "담백한" },
  { label: "❤️ 데이트", keyword: "꾸덕한" },
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
  
  // 검색 시에는 선택된 빵집 정보 초기화 (리스트 모드로 복귀)
  selectedBakery.value = null;

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
        preview_image: fields.image || `https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600`,
        tags: (fields.representative_tags && String(fields.representative_tags).trim() !== "")
              ? String(fields.representative_tags).split(',')
              : ['맛있는빵집', '추천'],
        business_hours: fields.business_hours || '09:00 ~ 20:00',
        contact: fields.contact || '',
        // ✅ [수정] 메뉴 데이터 매핑
        // 백엔드에서 'products'로 보내준 데이터를 프론트엔드 'menu'로 연결
        menu: fields.products ? fields.products.map(p => ({
            name: p.name,
            price: p.price,
            image_url: p.image_url // InfoCard는 item.image_url을 사용함
        })) : [],
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
        allBakeries.value = nearbyData;
      } else {
        allBakeries.value = mappedData;
        isFallbackSearch.value = true;
      }
    } else {
      allBakeries.value = mappedData;
    }

    // 초기에는 20개만 표시
    displayLimit.value = 20;
    bakeries.value = allBakeries.value.slice(0, displayLimit.value);
    hasMore.value = allBakeries.value.length > displayLimit.value;

    fillMissingCoordinates();

    if (bakeries.value.length > 0) {
      if (!currentHotBakery.value) pickRandomHotBakery();
      if (keyword) isListOpen.value = true;

      const nearest = bakeries.value[0];
      if (mapRef.value && nearest.lat && nearest.lng) {
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

// 마커 클릭 -> InfoCard 모드
const handleMarkerClick = (bakery) => {
  selectedBakery.value = bakery;
  isListOpen.value = true; 
};

// 리스트 클릭 -> InfoCard 모드 & 지도 이동
const handleListClick = (bakery) => {
  selectedBakery.value = bakery;
  if (mapRef.value) {
    mapRef.value.panTo(bakery.lat, bakery.lng);
  }
};

// InfoCard 닫기 -> 리스트 모드
const closeInfoCard = () => {
  selectedBakery.value = null;
};

// 상세보기 이동
const goToDetail = (id) => {
  router.push({ name: 'detail', params: { id: id } });
};

const filterByMood = (mood) => {
  if (selectedMood.value === mood.keyword) {
    // 이미 선택된 키워드를 다시 클릭하면 필터 해제
    selectedMood.value = null;
    searchKeyword.value = '';
  } else {
    selectedMood.value = mood.keyword;
    searchKeyword.value = mood.keyword;
  }
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
    });
  }
};

const refreshMap = () => {
  location.reload();
};

// 프로필 정보 가져오기
const fetchUserProfile = async () => {
  try {
    const token = authStore.token;
    if (!token) return;

    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: { Authorization: `Token ${token}` }
    });
    userProfile.value = response.data;
  } catch (error) {
    console.error('프로필 로드 실패:', error);
  }
};

// 프로필 이미지 URL 계산
const profileImageUrl = () => {
  if (!userProfile.value) return characterImages.hamster;
  if (userProfile.value.profile_image_url) {
    return `http://127.0.0.1:8000${userProfile.value.profile_image_url}`;
  }
  return characterImages[userProfile.value.character_type] || characterImages.hamster;
};

// 리뷰 작성 모달 열기
const openReviewWrite = (storeId) => {
  const store = bakeries.value.find(b => b.id === storeId);
  if (store) {
    reviewStoreId.value = storeId;
    reviewStoreName.value = store.name;
    showReviewWrite.value = true;
  }
};

// 리뷰 작성 완료 후
const handleReviewCreated = () => {
  showReviewWrite.value = false;
  // 리뷰 목록 새로고침 (BakeryInfoCard에서 자동으로 처리됨)
};

// 스크롤 이벤트 핸들러 - 더 많은 데이터 로드
const handleScroll = (event) => {
  const element = event.target;
  const scrollPosition = element.scrollTop + element.clientHeight;
  const scrollHeight = element.scrollHeight;

  // 스크롤이 바닥에서 100px 이내에 도달하면 추가 로드
  if (scrollHeight - scrollPosition < 100 && hasMore.value && !isLoading.value) {
    loadMoreBakeries();
  }
};

// 추가 데이터 로드
const loadMoreBakeries = () => {
  const newLimit = displayLimit.value + 20;
  displayLimit.value = newLimit;
  bakeries.value = allBakeries.value.slice(0, newLimit);
  hasMore.value = allBakeries.value.length > newLimit;
};

onMounted(() => {
  fetchUserProfile();
  // 초기 로딩 시 데이터를 가져오지 않고 지도만 표시
  // 사용자가 검색하거나 키워드를 선택할 때만 데이터 로드
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      // 현재 위치로 지도만 이동
      setTimeout(() => {
        if(mapRef.value) mapRef.value.moveToCurrentLocation();
      }, 500);
    }, (err) => {
      // 위치 권한 없어도 서울 중심으로 지도만 표시
      console.log('위치 권한 없음, 기본 위치로 지도 표시');
    });
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
          
          <button @click="refreshMap" class="flex flex-col items-center gap-1 text-orange-400 scale-110 transition-all group relative">
            <MapIcon class="w-6 h-6 stroke-[2.5px]" />
            <span class="text-[10px] font-medium">지도</span>
            <div class="absolute -right-[18px] top-1/2 -translate-y-1/2 w-1 h-8 bg-orange-400 rounded-l-full"></div>
          </button>

          <router-link :to="{ name: 'community' }" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group no-underline text-white/70">
            <BookOpen class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">커뮤니티</span>
          </router-link>
        </div>

        <div class="mt-auto">
           <router-link :to="{ name: 'mypage' }" class="block w-10 h-10 rounded-full overflow-hidden border-2 border-white/20 hover:border-white hover:scale-110 transition-all cursor-pointer">
             <img :src="profileImageUrl()" class="w-full h-full object-cover bg-white/10" />
           </router-link>
        </div>
      </nav>

      <!-- 사이드바 -->
      <div 
        class="absolute md:relative z-20 h-full bg-white shadow-xl transition-all duration-300 flex flex-col border-r border-[#1D4E45]/10 left-[72px] md:left-0"
        :class="isListOpen ? 'w-[320px] md:w-[380px] translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-0 overflow-hidden'"
      >
        <!-- 🟢 선택된 빵집이 있으면 InfoCard 표시 -->
        <div v-if="selectedBakery" class="h-full flex flex-col">
          <BakeryInfoCard
            :bakery="selectedBakery"
            @close="closeInfoCard"
            @view-detail="goToDetail"
            @write-review="openReviewWrite"
          />
        </div>

        <!-- 🟢 선택된 빵집이 없으면 리스트 표시 -->
        <div v-else class="h-full flex flex-col">
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
                v-if="!isLoading"
                @click="searchStores"
                class="absolute left-3.5 top-3.5 w-5 h-5 text-[#1D4E45] cursor-pointer hover:scale-110 transition-transform"
              />
              <div v-else class="absolute left-3.5 top-3.5 w-5 h-5">
                <div class="animate-spin rounded-full h-5 w-5 border-2 border-[#1D4E45] border-t-transparent"></div>
              </div>
            </div>
          </div>

          <div class="flex-1 overflow-y-auto p-5 space-y-6 hide-scrollbar bg-white" @scroll="handleScroll">
            <div v-if="isLoading && bakeries.length === 0" class="flex flex-col items-center justify-center py-20 gap-4">
              <div class="animate-spin rounded-full h-10 w-10 border-4 border-[#1D4E45] border-t-transparent"></div>
              <span class="text-sm text-gray-500">맛있는 빵집을 찾고 있어요...</span>
            </div>

            <div v-else-if="bakeries.length === 0" class="flex flex-col items-center justify-center py-20 text-center opacity-60">
              <Search class="w-12 h-12 text-gray-300 mb-2" />
              <p class="text-sm text-gray-500">키워드를 검색하여 빵집을 찾아보세요!</p>
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
                     <img
                       :src="currentHotBakery.preview_image"
                       @error="e => e.target.src = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80'"
                       class="w-full h-full object-cover"
                     />
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
                      <img
                        :src="bakery.preview_image"
                        @error="e => e.target.src = 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80'"
                        class="w-full h-full object-cover"
                      />
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

                <!-- 더 불러오기 인디케이터 -->
                <div v-if="hasMore" class="flex items-center justify-center py-4">
                  <div class="animate-spin rounded-full h-6 w-6 border-2 border-[#1D4E45] border-t-transparent"></div>
                  <span class="ml-2 text-xs text-gray-500">더 불러오는 중...</span>
                </div>
                <div v-else-if="bakeries.length > 0" class="text-center py-4 text-xs text-gray-400">
                  모든 빵집을 불러왔습니다 ({{ bakeries.length }}개)
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
        <!-- 키워드 필터 버튼 (네이버 지도 스타일) -->
        <div class="absolute top-4 left-1/2 -translate-x-1/2 z-20 flex flex-col gap-3 items-center">
          <!-- 키워드 버튼 그룹 -->
          <div class="flex gap-2 bg-white/95 backdrop-blur-sm p-2 rounded-full shadow-lg border border-gray-200">
            <button
              v-for="mood in moods"
              :key="mood.label"
              @click="filterByMood(mood)"
              class="px-4 py-2 rounded-full text-sm font-bold transition-all whitespace-nowrap"
              :class="selectedMood === mood.keyword
                ? 'bg-[#1D4E45] text-white shadow-md'
                : 'bg-white text-gray-700 hover:bg-gray-100'"
            >
              {{ mood.label }}
            </button>
          </div>

          <!-- 현 지도에서 검색 버튼 -->
          <button
            v-if="showReSearchBtn"
            @click="handleReSearchInMap"
            class="flex items-center gap-2 bg-white text-[#1D4E45] px-5 py-2.5 rounded-full shadow-lg border border-[#1D4E45]/10 font-bold hover:bg-[#1D4E45] hover:text-white transition-all transform hover:scale-105 animate-bounce-in"
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

    <!-- 리뷰 작성 모달 -->
    <StoreReviewWrite
      v-if="showReviewWrite"
      :store-id="reviewStoreId"
      :store-name="reviewStoreName"
      @close="showReviewWrite = false"
      @review-created="handleReviewCreated"
    />
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