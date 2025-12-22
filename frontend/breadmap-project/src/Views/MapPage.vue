<script setup>
import { ref, onMounted } from 'vue';
import KakaoMapLoader from '@/components/map/KakaoMapLoader.vue';
import BakeryMap from '@/components/map/BakeryMap.vue';
import { Search, MapPin, Star, Heart, Navigation, ThumbsUp, Home, Map as MapIcon, BookOpen, User } from 'lucide-vue-next';

// 더미 데이터
const bakeries = ref([
  { id: 1, name: "버터하우스", lat: 37.5666805, lng: 126.9784147, address: "서울 중구 태평로1가", rating: 4.8, image: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=400", tags: ["우울할때", "달달함"] },
  { id: 2, name: "무슈 크루아상", lat: 37.5652, lng: 126.980, address: "서울 중구 을지로", rating: 4.9, image: "https://images.unsplash.com/photo-1530610476181-d8ceb28bc272?q=80&w=400", tags: ["데이트", "바삭함"] },
  { id: 3, name: "선데이 베이글", lat: 37.560, lng: 126.975, address: "서울 중구 남대문로", rating: 4.5, image: "https://images.unsplash.com/photo-1620916297397-a4a5402a3c6c?q=80&w=400", tags: ["식사대용", "담백함"] },
]);

const selectedBakery = ref(null);
const currentHotBakery = ref(null);
const isListOpen = ref(true); // 사이드바 토글 상태
const currentTab = ref('map'); // 현재 탭 상태

// 기분/상황별 필터
const moods = [
  { label: "☁️ 우울할 땐", keyword: "달달함" },
  { label: "🤯 스트레스", keyword: "매콤" },
  { label: "☕ 브런치", keyword: "담백함" },
  { label: "❤️ 데이트", keyword: "데이트" },
];

// 마커 클릭 -> 리스트에서 해당 빵집 강조
const handleMarkerClick = (bakery) => {
  selectedBakery.value = bakery;
  // 모바일이거나 리스트가 닫혀있다면 열어주기
  if (!isListOpen.value) isListOpen.value = true;
};

// 리스트 항목 클릭 -> 지도 이동
const handleListClick = (bakery) => {
  selectedBakery.value = bakery;
};

const filterByMood = (keyword) => {
  console.log("Filtering by:", keyword);
};

// 랜덤 핫한 빵집 추천
const pickRandomHotBakery = () => {
  const randomIndex = Math.floor(Math.random() * bakeries.value.length);
  currentHotBakery.value = bakeries.value[randomIndex];
};

onMounted(() => {
  pickRandomHotBakery();
});
</script>

<template>
  <KakaoMapLoader>
    <!-- 상단 여백 없이 화면 꽉 채움 (h-screen) -->
    <div class="flex h-screen w-full overflow-hidden relative bg-[#F9F7F2]">
      
      <!-- 0. 세로형 네비게이션 바 (가장 왼쪽) -->
      <nav class="w-[72px] h-full bg-[#1D4E45] flex flex-col items-center py-6 z-50 shrink-0 shadow-lg text-white/70">
        <!-- 로고 -->
        <div class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center text-xl mb-10 cursor-pointer hover:bg-white/20 transition-colors text-white">
          🥐
        </div>

        <!-- 메뉴 아이콘들 -->
        <div class="flex flex-col gap-8 w-full">
          <button @click="currentTab = 'home'" :class="{'text-white scale-110': currentTab === 'home'}" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group">
            <Home class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">홈</span>
          </button>
          
          <button @click="currentTab = 'map'" :class="{'text-orange-400 scale-110': currentTab === 'map'}" class="flex flex-col items-center gap-1 hover:text-orange-400 hover:scale-110 transition-all group relative">
            <MapIcon class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">지도</span>
            <!-- 활성 표시 -->
            <div v-if="currentTab === 'map'" class="absolute -right-[18px] top-1/2 -translate-y-1/2 w-1 h-8 bg-orange-400 rounded-l-full"></div>
          </button>

          <button @click="currentTab = 'magazine'" :class="{'text-white scale-110': currentTab === 'magazine'}" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group">
            <BookOpen class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">매거진</span>
          </button>

          <button @click="currentTab = 'mypage'" :class="{'text-white scale-110': currentTab === 'mypage'}" class="flex flex-col items-center gap-1 hover:text-white hover:scale-110 transition-all group">
            <User class="w-6 h-6 group-hover:stroke-[2.5px]" />
            <span class="text-[10px] font-medium">마이</span>
          </button>
        </div>

        <!-- 하단 설정 -->
        <div class="mt-auto">
           <button class="w-10 h-10 rounded-full overflow-hidden border-2 border-white/20 hover:border-white transition-colors">
             <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="w-full h-full bg-white/10">
           </button>
        </div>
      </nav>

      <!-- 1. 사이드바 (리스트 및 검색) -->
      <div 
        class="absolute md:relative z-20 h-full bg-white shadow-xl transition-all duration-300 flex flex-col border-r border-[#1D4E45]/10 left-[72px] md:left-0"
        :class="isListOpen ? 'w-[320px] md:w-[380px] translate-x-0' : 'w-0 -translate-x-full md:w-0 md:-translate-x-0 overflow-hidden'"
      >
        <!-- 사이드바 헤더: 검색 & 필터 -->
        <div class="p-5 border-b border-gray-100 bg-white shrink-0 z-10">
          <div class="relative mb-4">
            <input 
              type="text" 
              placeholder="장소, 주소, 빵 검색" 
              class="w-full pl-11 pr-4 py-3 bg-[#F9F7F2] rounded-lg border-none outline-none text-[#4A4036] placeholder-gray-400 focus:ring-2 focus:ring-[#1D4E45]/20 transition-all font-medium"
            >
            <Search class="absolute left-3.5 top-3.5 w-5 h-5 text-[#1D4E45]" />
          </div>

          <!-- 필터 칩 -->
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

        <!-- 사이드바 컨텐츠: 추천 & 리스트 -->
        <div class="flex-1 overflow-y-auto p-5 space-y-6 hide-scrollbar bg-white">
          
          <!-- 추천 카드 (Hot Pick) -->
          <div v-if="currentHotBakery" class="bg-gradient-to-br from-[#1D4E45] to-[#12352E] rounded-2xl p-5 text-white shadow-lg relative overflow-hidden group cursor-pointer" @click="handleListClick(currentHotBakery)">
             <div class="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>
             
             <div class="flex justify-between items-start mb-3 relative z-10">
               <span class="px-2 py-1 bg-white/20 backdrop-blur rounded text-[10px] font-bold tracking-wider flex items-center gap-1">
                 <ThumbsUp class="w-3 h-3" /> 오늘의 추천
               </span>
               <button class="text-white/70 hover:text-white"><Heart class="w-4 h-4" /></button>
             </div>
             
             <div class="flex gap-4 items-center relative z-10">
               <div class="w-16 h-16 rounded-full bg-white/10 border-2 border-white/20 overflow-hidden shrink-0">
                 <img :src="currentHotBakery.image" class="w-full h-full object-cover">
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
            <h3 class="font-bold text-[#4A4036] mb-3 text-sm px-1">내 주변 빵집 리스트</h3>
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
                <!-- 썸네일 -->
                <div class="w-20 h-20 rounded-lg bg-gray-100 overflow-hidden shrink-0">
                  <img :src="bakery.image" class="w-full h-full object-cover">
                </div>
                
                <!-- 정보 -->
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

        <!-- 사이드바 접기/펼치기 버튼 -->
        <button 
          @click="isListOpen = !isListOpen"
          class="absolute top-1/2 -right-6 w-6 h-12 bg-white border border-l-0 border-gray-200 rounded-r-lg flex items-center justify-center text-gray-400 shadow-md hover:text-[#1D4E45] z-30"
        >
          <span v-if="isListOpen">◀</span>
          <span v-else>▶</span>
        </button>
      </div>

      <!-- 2. 지도 영역 (오른쪽) -->
      <div class="flex-1 h-full relative z-0">
        <BakeryMap 
          :bakeries="bakeries" 
          :selected-bakery="selectedBakery"
          @select-marker="handleMarkerClick"
        />
        
        <!-- 지도 위 플로팅 버튼들 -->
        <div class="absolute top-4 right-4 flex flex-col gap-2 z-10">
          <button class="bg-white p-2.5 rounded shadow-md text-gray-600 hover:text-[#1D4E45] hover:bg-gray-50 transition-colors" title="내 위치">
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
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>