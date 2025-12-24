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
        <!-- 폰트 크기 통일: text-xl -->
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
      <div v-else-if="selectedBakery" class="grid lg:grid-cols-2 gap-12 items-start animate-fade-in">

        <!-- Image Gallery (Sticky) -->
        <div class="lg:sticky lg:top-24 space-y-4">
          <div class="aspect-[4/3] rounded-[2.5rem] overflow-hidden shadow-2xl bg-white border-8 border-white">
            <img :src="selectedBakery.image" class="w-full h-full object-cover">
          </div>
          <div class="grid grid-cols-3 gap-3">
            <div class="aspect-square rounded-2xl overflow-hidden bg-white border-4 border-white shadow-md hover:shadow-xl transition-all" v-for="i in 3" :key="i">
              <img :src="`https://source.unsplash.com/random/200x200/?bakery,bread&sig=${selectedBakery.id + i}`" class="w-full h-full object-cover hover:scale-110 transition-transform duration-300 cursor-pointer">
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="pt-4 space-y-8"> <!-- 간격 조금 더 넓힘 -->
          
          <!-- 뱃지 -->
          <div class="inline-flex items-center gap-2 bg-[#FFF3DD] border-2 border-[#FFE8CC] px-5 py-2 rounded-full shadow-md">
            <span class="text-2xl">🍞</span>
            <!-- 폰트 크기 통일: text-lg -->
            <span class="text-[#C99768] font-jua text-lg">동네 빵집</span>
          </div>

          <!-- 제목 (상호명만 크게 유지) -->
          <h2 class="text-5xl md:text-6xl font-jua text-[#6B4A38] leading-tight">
            {{ selectedBakery.bakeryName }}
          </h2>

          <!-- 정보 박스들 -->
          <div class="space-y-4">
            <!-- 주소 -->
            <div class="bg-white/80 backdrop-blur-sm border-2 border-[#FFE8CC] rounded-2xl p-5 shadow-md">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-full bg-[#FFF3DD] flex items-center justify-center shrink-0">
                  <MapPin class="w-5 h-5 text-[#C99768]" />
                </div>
                <div class="flex-1">
                  <!-- 폰트 크기 통일: 라벨 text-lg, 내용 text-xl -->
                  <p class="text-lg text-[#C99768] font-jua mb-1">주소</p>
                  <p class="text-[#6B4A38] font-jua text-xl">{{ selectedBakery.location }}</p>
                </div>
              </div>
            </div>

            <!-- 평점 & 태그 -->
            <div class="flex flex-wrap gap-3">
              <!-- 폰트 크기 통일: text-lg -->
              <span class="px-5 py-3 bg-white border-2 border-[#FFE8CC] rounded-full text-[#8B6A55] flex items-center gap-2 shadow-sm font-jua text-lg">
                <Star class="w-5 h-5 text-orange-500 fill-current" /> {{ selectedBakery.rating }}
              </span>
              <span v-for="tag in selectedBakery.tags" :key="tag" class="px-5 py-3 bg-[#FFCCBC]/30 text-[#EF6C00] rounded-full font-jua border-2 border-[#FFE0B2] text-lg">
                #{{ tag }}
              </span>
            </div>
          </div>

          <!-- 설명 (폰트 크기 text-xl로 통일) -->
          <p class="text-xl text-[#8B6A55] leading-relaxed font-jua bg-white/60 backdrop-blur-sm p-8 rounded-3xl border-2 border-[#FFE8CC]">
            {{ selectedBakery.description || "이곳은 매일 아침 갓 구운 신선한 빵을 제공하는 베이커리입니다. 고소한 버터 향과 부드러운 식감을 즐겨보세요. 🥐" }}
          </p>

          <!-- AI Summary -->
          <div class="bg-gradient-to-br from-[#FFF3DD] to-[#FFE8CC] rounded-[2.5rem] p-8 relative overflow-hidden border-4 border-white shadow-xl">
            <!-- 장식 요소 -->
            <div class="absolute -top-8 -right-8 w-32 h-32 bg-[#F3B37A]/20 rounded-full blur-2xl"></div>
            <div class="absolute -bottom-6 -left-6 w-24 h-24 bg-[#C99768]/20 rounded-full blur-xl"></div>

            <div class="relative z-10">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 rounded-full bg-[#C99768] flex items-center justify-center text-white shadow-lg">
                  <Sparkles class="w-6 h-6" />
                </div>
                <!-- 섹션 제목 text-3xl -->
                <h3 class="font-jua text-[#6B4A38] text-3xl">AI 리뷰 요약</h3>
              </div>

              <div v-if="!aiSummary">
                <!-- 버튼 텍스트 text-xl -->
                <button @click="generateAISummary" class="w-full py-6 bg-white/80 backdrop-blur-sm border-3 border-dashed border-[#F3B37A] rounded-2xl text-[#C99768] font-jua text-xl hover:bg-white hover:border-[#C99768] hover:shadow-lg transition-all flex items-center justify-center gap-2 group">
                  <span>🤖 분석 리포트 생성하기</span>
                  <ArrowRight class="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
              <div v-else class="animate-fade-in space-y-5">
                <!-- 내용 텍스트 text-xl -->
                <p class="text-xl text-[#6B4A38] font-jua leading-relaxed bg-white/60 backdrop-blur-sm p-6 rounded-2xl border-2 border-white">
                  "{{ aiSummary.text }}"
                </p>
                <div class="flex flex-wrap gap-2">
                  <!-- 키워드 text-lg -->
                  <span v-for="keyword in aiSummary.keywords" :key="keyword" class="px-5 py-2 bg-white rounded-full text-lg text-[#C99768] font-jua shadow-md border-2 border-[#FFE8CC]">
                    #{{ keyword }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Menu List -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <!-- 섹션 제목 text-3xl -->
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
                    <!-- 메뉴 이름 text-2xl, 카테고리 text-lg -->
                    <h4 class="text-2xl font-jua text-[#6B4A38] mb-2">{{ menu.name }}</h4>
                    <p class="text-lg text-[#C99768] font-jua">{{ menu.category || '베이커리' }}</p>
                  </div>
                </div>
                <!-- 가격 text-2xl -->
                <span class="text-2xl font-jua text-[#C99768]">{{ Number(menu.price).toLocaleString() }}원</span>
              </div>
            </div>
            <div v-else class="text-[#C99768] py-16 text-center border-3 border-dashed border-[#FFE8CC] bg-white/50 rounded-3xl flex flex-col items-center justify-center gap-4">
              <span class="text-6xl">🥐</span>
              <span class="font-jua text-xl">등록된 메뉴 정보가 없습니다</span>
            </div>
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
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { PawPrint, MapPin, Star, Sparkles, ArrowRight } from 'lucide-vue-next';

const route = useRoute();
const selectedBakery = ref(null);
const isLoading = ref(true);
const isError = ref(false);
const aiSummary = ref(null);

const fetchBakeryDetail = async () => {
  const bakeryId = route.params.id;
  
  if (!bakeryId) {
    console.warn("Bakery ID is missing");
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