<template>
  <div class="bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] min-h-screen pt-20">
    <div class="max-w-[1200px] mx-auto px-6 py-20">

      <!-- 뒤로 가기 버튼 -->
      <button 
        @click="$router.go(-1)" 
        class="mb-10 group flex items-center gap-3 px-6 py-3 
               bg-white/80 backdrop-blur-sm border-2 border-[#FFE8CC] rounded-full
               shadow-[0_4px_12px_rgba(201,151,104,0.1)]
               hover:border-[#F3B37A] hover:bg-white hover:shadow-[0_8px_20px_rgba(201,151,104,0.2)]
               hover:-translate-y-1 transition-all duration-300"
      >
        <div class="w-10 h-10 rounded-full bg-[#FFF3DD] flex items-center justify-center group-hover:bg-[#F3B37A] transition-colors duration-300">
          <PawPrint class="w-5 h-5 text-[#F3B37A] group-hover:text-white transition-colors duration-300" />
        </div>
        <span class="font-jua text-xl text-[#6B4A38] pt-1 group-hover:text-[#C99768] transition-colors">
          목록으로 가기
        </span>
      </button>

      <!-- 1. 로딩 중일 때 -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center h-64 gap-4">
        <div class="text-6xl animate-bounce">🥐</div>
        <span class="text-[#C99768] font-jua text-2xl">맛있는 빵 굽는 중...</span>
      </div>

      <!-- 2. 데이터 로드 완료 시 (정상) -->
      <div v-else-if="selectedBakery" class="animate-fade-in space-y-12">
        
        <!-- [수정됨] 1. 상단 중앙 타이틀 영역 -->
        <div class="text-center flex flex-col items-center">
          <div class="inline-flex items-center gap-2 bg-[#FFF3DD] border-2 border-[#FFE8CC] px-5 py-2 rounded-full shadow-md mb-6">
            <span class="text-2xl">🍞</span>
            <span class="text-[#C99768] font-jua text-lg">동네 빵집</span>
          </div>
          <h2 class="text-5xl md:text-6xl font-jua text-[#6B4A38] leading-tight">
            {{ selectedBakery.bakeryName }}
          </h2>
        </div>

        <!-- [수정됨] 2. 대표 사진 영역 (높이 축소: h-96 -> h-72) -->
        <div class="w-full h-72 rounded-[2.5rem] overflow-hidden shadow-2xl bg-white border-8 border-white relative z-0 group">
          <img :src="selectedBakery.image" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" alt="베이커리 대표 사진">
          <!-- 사진 위에 살짝 텍스트 오버레이 (선택사항) -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent pointer-events-none"></div>
        </div>

        <!-- [수정됨] 3. 중간 정보 영역 (2단 컬럼: 왼쪽 정보 / 오른쪽 메뉴) -->
        <div class="grid lg:grid-cols-2 gap-12 items-start">
          
          <!-- 왼쪽 컬럼: 매장 정보 & 설명 & AI 요약 -->
          <div class="space-y-8">
            <!-- 기본 정보 박스 -->
            <div class="space-y-4">
               <div class="bg-white/80 backdrop-blur-sm border-2 border-[#FFE8CC] rounded-2xl p-6 shadow-md">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 rounded-full bg-[#FFF3DD] flex items-center justify-center shrink-0">
                    <MapPin class="w-5 h-5 text-[#C99768]" />
                  </div>
                  <div class="flex-1">
                    <p class="text-lg text-[#C99768] font-jua mb-1">주소</p>
                    <p class="text-[#6B4A38] font-jua text-xl">{{ selectedBakery.location }}</p>
                  </div>
                </div>
              </div>

              <!-- 평점 & 태그 -->
              <div class="flex flex-wrap gap-3">
                <span class="px-5 py-3 bg-white border-2 border-[#FFE8CC] rounded-full text-[#8B6A55] flex items-center gap-2 shadow-sm font-jua text-lg">
                  <Star class="w-5 h-5 text-orange-500 fill-current" /> {{ selectedBakery.rating }}
                </span>
                <span v-for="tag in selectedBakery.tags" :key="tag" class="px-5 py-3 bg-[#FFCCBC]/30 text-[#EF6C00] rounded-full font-jua border-2 border-[#FFE0B2] text-lg">
                  #{{ tag }}
                </span>
              </div>
            </div>

            <!-- 설명 -->
            <p class="text-xl text-[#8B6A55] leading-relaxed font-jua bg-white/60 backdrop-blur-sm p-8 rounded-3xl border-2 border-[#FFE8CC]">
              {{ selectedBakery.description || "이곳은 매일 아침 갓 구운 신선한 빵을 제공하는 베이커리입니다. 고소한 버터 향과 부드러운 식감을 즐겨보세요. 🥐" }}
            </p>

            <!-- AI Summary -->
            <div class="bg-gradient-to-br from-[#FFF3DD] to-[#FFE8CC] rounded-[2.5rem] p-8 relative overflow-hidden border-4 border-white shadow-xl">
              <div class="absolute -top-8 -right-8 w-32 h-32 bg-[#F3B37A]/20 rounded-full blur-2xl"></div>
              <div class="absolute -bottom-6 -left-6 w-24 h-24 bg-[#C99768]/20 rounded-full blur-xl"></div>

              <div class="relative z-10">
                <div class="flex items-center gap-3 mb-6">
                  <div class="w-12 h-12 rounded-full bg-[#C99768] flex items-center justify-center text-white shadow-lg">
                    <Sparkles class="w-6 h-6" />
                  </div>
                  <h3 class="font-jua text-[#6B4A38] text-3xl">AI 리뷰 요약</h3>
                </div>

                <div v-if="!aiSummary">
                  <button @click="generateAISummary" class="w-full py-6 bg-white/80 backdrop-blur-sm border-3 border-dashed border-[#F3B37A] rounded-2xl text-[#C99768] font-jua text-xl hover:bg-white hover:border-[#C99768] hover:shadow-lg transition-all flex items-center justify-center gap-2 group">
                    <span>🤖 분석 리포트 생성하기</span>
                    <ArrowRight class="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
                <div v-else class="animate-fade-in space-y-5">
                  <p class="text-xl text-[#6B4A38] font-jua leading-relaxed bg-white/60 backdrop-blur-sm p-6 rounded-2xl border-2 border-white">
                    "{{ aiSummary.text }}"
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <span v-for="keyword in aiSummary.keywords" :key="keyword" class="px-5 py-2 bg-white rounded-full text-lg text-[#C99768] font-jua shadow-md border-2 border-[#FFE8CC]">
                      #{{ keyword }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 오른쪽 컬럼: 메뉴 리스트 -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <h3 class="font-jua text-[#6B4A38] text-3xl">시그니처 메뉴</h3>
              <span class="text-4xl">🍞</span>
            </div>
            <div v-if="selectedBakery.menu && selectedBakery.menu.length > 0" class="space-y-4">
              <div v-for="menu in selectedBakery.menu" :key="menu.id" class="flex justify-between items-center p-6 rounded-3xl bg-white border-3 border-[#FFE8CC] hover:border-[#F3B37A] hover:shadow-xl transition-all cursor-pointer group">
                <div class="flex items-center gap-6">
                  <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[#FFF3DD] to-[#FFE8CC] flex items-center justify-center shrink-0 text-5xl group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 shadow-md">
                    {{ getMenuIcon(menu.name) }}
                  </div>
                  <div>
                    <h4 class="text-2xl font-jua text-[#6B4A38] mb-2">{{ menu.name }}</h4>
                    <p class="text-lg text-[#C99768] font-jua">{{ menu.category || '베이커리' }}</p>
                  </div>
                </div>
                <span class="text-2xl font-jua text-[#C99768]">{{ Number(menu.price).toLocaleString() }}원</span>
              </div>
            </div>
            <div v-else class="text-[#C99768] py-16 text-center border-3 border-dashed border-[#FFE8CC] bg-white/50 rounded-3xl flex flex-col items-center justify-center gap-4">
              <span class="text-6xl">🥐</span>
              <span class="font-jua text-xl">등록된 메뉴 정보가 없습니다</span>
            </div>
          </div>

        </div>

        <!-- [수정됨] 4. 카카오맵 영역 (맨 밑으로 이동) -->
        <div class="space-y-6 pt-8 border-t-2 border-[#FFE8CC]/50">
           <div class="flex items-center justify-center gap-3 mb-2">
             <span class="text-3xl">🗺️</span>
             <h3 class="font-jua text-[#6B4A38] text-3xl">찾아오시는 길</h3>
           </div>
           <div class="w-full h-96 rounded-[2.5rem] overflow-hidden shadow-2xl bg-white border-8 border-white relative z-0">
            <!-- 지도가 로드되지 않았을 때 로딩 표시 -->
            <div v-if="!isMapLoaded" class="absolute inset-0 flex flex-col items-center justify-center bg-gray-50 z-10">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#C99768] mb-2"></div>
              <span class="text-[#C99768] font-jua">지도 로딩 중...</span>
            </div>
            <div id="map" class="w-full h-full"></div>
          </div>
        </div>

      </div>
      
      <!-- 3. 에러 화면 -->
      <div v-else class="flex flex-col items-center justify-center py-32 text-center">
        <div class="w-32 h-32 bg-white rounded-full flex items-center justify-center mb-6 text-6xl shadow-xl border-4 border-[#FFE8CC]">
          🏚️
        </div>
        <h3 class="text-3xl font-jua text-[#6B4A38] mb-4">정보를 찾을 수 없어요</h3>
        <p class="text-[#C99768] font-jua text-xl mb-10">요청하신 빵집 정보가 삭제되었거나 존재하지 않습니다</p>
        <button @click="$router.push('/')" class="px-10 py-5 bg-gradient-to-r from-[#C99768] to-[#F3B37A] text-white rounded-3xl font-jua text-xl hover:shadow-xl hover:-translate-y-1 transition-all shadow-lg">
          홈으로 돌아가기 🏠
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { PawPrint, MapPin, Star, Sparkles, ArrowRight } from 'lucide-vue-next';

const route = useRoute();
const selectedBakery = ref(null);
const isLoading = ref(true);
const isError = ref(false);
const isMapLoaded = ref(false); // 지도 로드 상태
const aiSummary = ref(null);

// 환경 변수에서 키 가져오기
const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY;

// [수정됨] 카카오 스크립트 로드 함수 (제공해주신 로직 적용)
const loadKakaoMapScript = () => {
  return new Promise((resolve, reject) => {
    // 1. 이미 kakao 객체가 있고, maps까지 로드된 상태인지 체크
    if (window.kakao && window.kakao.maps) {
      window.kakao.maps.load(() => resolve());
      return;
    }

    // 2. 스크립트 중복 삽입 방지 및 로드
    const scriptId = 'kakao-map-script';
    const existingScript = document.getElementById(scriptId);

    if (!existingScript) {
      const script = document.createElement('script');
      script.id = scriptId;
      // services 라이브러리 필수 포함
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_API_KEY}&libraries=services`;
      
      script.onload = () => {
        window.kakao.maps.load(() => resolve());
      };
      
      script.onerror = () => {
        console.error('카카오맵 스크립트 로드 실패');
        reject(new Error('Kakao map script load failed'));
      };
      
      document.head.appendChild(script);
    } else {
      // 스크립트 태그는 있는데 아직 로딩이 안 끝난 경우
      if (window.kakao && window.kakao.maps) {
         window.kakao.maps.load(() => resolve());
      } else {
        // 기존 스크립트의 로드가 끝날 때까지 대기해야 하지만, 
        // 간단히 처리하기 위해 약간의 텀을 두고 재시도하거나 onload에 훅을 거는 방식 등을 쓸 수 있습니다.
        // 여기서는 기존 로직과 동일하게 onload에 덮어씌우지 않고, 안전하게 대기하는 방식(Polling)을 쓰거나
        // 기존 스크립트가 로드되길 기다립니다. (사용자 코드를 존중하여 최대한 단순화)
        existingScript.addEventListener('load', () => {
             window.kakao.maps.load(() => resolve());
        });
      }
    }
  });
};

// [수정됨] 지도 초기화 및 마커 표시
const initMap = () => {
  const container = document.getElementById('map');
  if (!container || !window.kakao || !window.kakao.maps) return;

  const options = {
    center: new window.kakao.maps.LatLng(33.450701, 126.570667),
    level: 3
  };

  const map = new window.kakao.maps.Map(container, options);
  
  // 주소-좌표 변환
  const geocoder = new window.kakao.maps.services.Geocoder();

  geocoder.addressSearch(selectedBakery.value.location, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const coords = new window.kakao.maps.LatLng(result[0].y, result[0].x);

      const marker = new window.kakao.maps.Marker({
        map: map,
        position: coords
      });

      map.setCenter(coords);
      isMapLoaded.value = true; // 지도 로딩 완료
    } else {
      console.warn('주소 검색 실패:', status);
      // 실패시에도 로딩 상태는 해제해주는 것이 좋음 (지도 자체는 떴으므로)
      isMapLoaded.value = true; 
    }
  });
};

const fetchBakeryDetail = async () => {
  const bakeryId = route.params.id;
  
  if (!bakeryId) {
    isLoading.value = false;
    isError.value = true;
    return;
  }

  try {
    isLoading.value = true;
    isError.value = false;
    
    // API 호출
    const response = await axios.get(`http://127.0.0.1:8000/stores/${bakeryId}/`);
    const data = response.data;

    const getImageUrl = (imageUrl) => {
      if (!imageUrl) return 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800&h=600&fit=crop'
      if (imageUrl.startsWith('http')) return imageUrl
      return `http://127.0.0.1:8000${imageUrl}`
    }

    selectedBakery.value = {
      id: data.id,
      bakeryName: data.name,
      location: data.address,
      rating: parseFloat(data.avg_rating) || 0.0,
      description: data.description,
      image: getImageUrl(data.image),
      tags: (data.representative_tags && String(data.representative_tags).trim() !== "")
            ? String(data.representative_tags).split(',')
            : ['추천맛집'],
      menu: data.products ? data.products.map(p => ({
        id: p.id,
        name: p.name,
        price: p.price,
        category: p.category
      })) : []
    };

    // [수정됨] 데이터 로드 후 -> 스크립트 로드 -> 지도 초기화 순서로 실행
    nextTick(async () => {
      try {
        await loadKakaoMapScript(); // 스크립트 로딩 대기
        initMap(); // 지도 그리기
      } catch (e) {
        console.error("지도 로딩 중 에러 발생", e);
      }
    });

  } catch (error) {
    console.error('상세 정보 로드 실패:', error);
    isError.value = true; 
    selectedBakery.value = null; 
  } finally {
    isLoading.value = false;
  }
};

const generateAISummary = async () => {
  aiSummary.value = { text: "AI가 리뷰를 분석 중입니다... 🤖", keywords: [] };

  try {
    const bakeryId = route.params.id;
    const response = await axios.get(`http://127.0.0.1:8000/stores/${bakeryId}/ai-summary/`);

    aiSummary.value = {
      text: response.data.summary,
      keywords: response.data.keywords
    };
  } catch (error) {
    console.error("AI 요약 실패:", error);
    aiSummary.value = {
      text: "분석할 리뷰가 충분하지 않습니다.",
      keywords: ["데이터부족"]
    };
  }
};

const getMenuIcon = (menuName) => {
  const name = menuName.toLowerCase();
  if (name.includes('크루아상') || name.includes('croissant')) return '🥐';
  if (name.includes('바게트') || name.includes('baguette')) return '🥖';
  if (name.includes('식빵') || name.includes('토스트')) return '🍞';
  if (name.includes('베이글') || name.includes('bagel')) return '🥯';
  if (name.includes('도넛') || name.includes('doughnut')) return '🍩';
  if (name.includes('케이크') || name.includes('cake')) return '🍰';
  if (name.includes('컵케이크') || name.includes('cupcake')) return '🧁';
  if (name.includes('파이') || name.includes('pie')) return '🥧';
  if (name.includes('쿠키') || name.includes('cookie')) return '🍪';
  if (name.includes('프레첼') || name.includes('pretzel')) return '🥨';
  if (name.includes('샌드위치') || name.includes('sandwich')) return '🥪';
  if (name.includes('햄버거') || name.includes('burger')) return '🍔';
  if (name.includes('타르트') || name.includes('tart')) return '🥮';
  if (name.includes('마카롱') || name.includes('macaron')) return '🍬';
  if (name.includes('빵') || name.includes('bread')) return '🍞';
  if (name.includes('롤') || name.includes('roll')) return '🥐';
  if (name.includes('푸딩') || name.includes('pudding')) return '🍮';
  if (name.includes('아이스크림') || name.includes('ice cream')) return '🍦';
  if (name.includes('커피') || name.includes('coffee')) return '☕';
  if (name.includes('라떼') || name.includes('latte')) return '🥛';
  if (name.includes('주스') || name.includes('juice')) return '🧃';
  return '🥐';
};

onMounted(() => {
  fetchBakeryDetail();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>