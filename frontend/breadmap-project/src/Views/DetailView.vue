<template>
  <div class="bg-white min-h-screen pt-20">
    <div class="max-w-[1200px] mx-auto px-6 py-20">
      
      <!-- 뒤로 가기 버튼 -->
      <button @click="$router.go(-1)" class="mb-10 flex items-center gap-2 text-gray-500 hover:text-teal-800 transition-colors font-medium group">
        <div class="w-8 h-8 rounded-full border border-gray-200 flex items-center justify-center group-hover:bg-teal-800 group-hover:text-white group-hover:border-teal-800 transition-all">
          <i data-lucide="arrow-left" class="w-4 h-4"></i>
        </div>
        <span>Back</span>
      </button>

      <!-- 1. 로딩 중일 때 -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center h-64 gap-4">
        <div class="animate-spin rounded-full h-10 w-10 border-4 border-teal-800 border-t-transparent"></div>
        <span class="text-gray-500 font-medium">맛있는 빵 굽는 중...</span>
      </div>

      <!-- 2. 데이터 로드 완료 시 (정상) -->
      <div v-else-if="selectedBakery" class="grid lg:grid-cols-2 gap-16 items-start animate-fade-in">
        
        <!-- Image Gallery (Sticky) -->
        <div class="lg:sticky lg:top-24 space-y-6">
          <div class="aspect-[4/3] rounded-[2rem] overflow-hidden shadow-2xl bg-gray-100">
            <img :src="selectedBakery.image" class="w-full h-full object-cover">
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div class="aspect-square rounded-2xl overflow-hidden bg-gray-100" v-for="i in 3" :key="i">
              <img :src="`https://source.unsplash.com/random/200x200/?bakery,bread&sig=${selectedBakery.id + i}`" class="w-full h-full object-cover hover:opacity-80 transition-opacity cursor-pointer">
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="pt-4">
          <span class="text-orange-600 font-bold tracking-wider text-sm uppercase mb-3 block">Premium Bakery</span>
          <h2 class="text-5xl md:text-6xl font-playfair font-bold text-teal-900 mb-6 leading-tight">{{ selectedBakery.bakeryName }}</h2>
          
          <div class="flex flex-wrap gap-4 mb-10 text-sm">
            <span class="px-4 py-2 border border-gray-200 rounded-full text-gray-600 flex items-center gap-2">
              <i data-lucide="map-pin" class="w-4 h-4"></i> {{ selectedBakery.location }}
            </span>
            <span class="px-4 py-2 border border-gray-200 rounded-full text-gray-600 flex items-center gap-2">
              <i data-lucide="star" class="w-4 h-4 text-orange-500 fill-current"></i> {{ selectedBakery.rating }}
            </span>
            <span v-for="tag in selectedBakery.tags" :key="tag" class="px-4 py-2 bg-teal-50 text-teal-800 rounded-full font-bold">
              #{{ tag }}
            </span>
          </div>

          <p class="text-xl text-gray-600 leading-relaxed mb-12 font-light">
            {{ selectedBakery.description || "이곳은 매일 아침 갓 구운 신선한 빵을 제공하는 베이커리입니다. 고소한 버터 향과 부드러운 식감을 즐겨보세요." }}
          </p>

          <!-- AI Summary -->
          <div class="bg-[#F9F7F2] rounded-[2rem] p-10 relative mb-12 overflow-hidden group border border-teal-800/5">
            <div class="absolute top-0 right-0 p-10 opacity-10 group-hover:opacity-20 transition-opacity duration-700">
              <i data-lucide="quote" class="w-32 h-32 text-teal-900"></i>
            </div>
            
            <div class="relative z-10">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-8 h-8 rounded-full bg-teal-800 flex items-center justify-center text-white">
                  <i data-lucide="sparkles" class="w-4 h-4"></i>
                </div>
                <h3 class="font-bold text-teal-900 text-lg">AI Review Summary</h3>
              </div>
              
              <div v-if="!aiSummary">
                <button @click="generateAISummary" class="w-full py-5 bg-white border-2 border-dashed border-teal-800/20 rounded-2xl text-teal-800 font-bold hover:bg-teal-50 hover:border-teal-800/40 transition-all flex items-center justify-center gap-2">
                  <span>분석 리포트 생성하기</span>
                  <i data-lucide="loader" class="w-4 h-4 animate-spin hidden"></i>
                </button>
              </div>
              <div v-else class="animate-fade-in">
                <p class="text-lg text-teal-900 font-medium leading-relaxed mb-6">"{{ aiSummary.text }}"</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="keyword in aiSummary.keywords" :key="keyword" class="px-4 py-2 bg-white rounded-full text-sm text-teal-800 font-bold shadow-sm">#{{ keyword }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Menu List -->
          <div>
            <h3 class="font-bold text-teal-900 mb-6 text-xl">Signature Menu</h3>
            <div v-if="selectedBakery.menu && selectedBakery.menu.length > 0" class="space-y-4">
              <div v-for="menu in selectedBakery.menu" :key="menu.id" class="flex justify-between items-center p-6 rounded-2xl border border-gray-100 hover:border-teal-800/20 hover:shadow-lg transition-all cursor-pointer bg-white group">
                <div class="flex items-center gap-6">
                  <div class="w-20 h-20 rounded-xl bg-gray-100 overflow-hidden shrink-0">
                    <img :src="menu.img" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500">
                  </div>
                  <div>
                    <h4 class="text-lg font-bold text-gray-900 mb-1">{{ menu.name }}</h4>
                    <p class="text-sm text-gray-400">{{ menu.category || 'Bakery' }}</p>
                  </div>
                </div>
                <span class="text-lg font-bold text-teal-800">{{ Number(menu.price).toLocaleString() }}원</span>
              </div>
            </div>
            <div v-else class="text-gray-400 py-10 text-center border-2 border-dashed border-gray-200 rounded-2xl flex flex-col items-center justify-center gap-2">
              <span class="text-2xl grayscale opacity-50">🥐</span>
              <span>등록된 메뉴 정보가 없습니다.</span>
            </div>
          </div>

        </div>
      </div>
      
      <!-- 3. 데이터 로드 실패 또는 없음 (에러 화면) -->
      <div v-else class="flex flex-col items-center justify-center py-32 text-center">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6 text-4xl grayscale opacity-50">🏚️</div>
        <h3 class="text-xl font-bold text-gray-700 mb-2">정보를 찾을 수 없어요</h3>
        <p class="text-gray-500 mb-8">요청하신 빵집 정보가 삭제되었거나 존재하지 않습니다.</p>
        <button @click="$router.push('/map')" class="px-6 py-3 bg-teal-800 text-white rounded-xl font-bold hover:bg-teal-900 transition-colors">
          지도로 돌아가기
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { createIcons, icons } from 'lucide';

const route = useRoute();
const selectedBakery = ref(null);
const isLoading = ref(true);
const isError = ref(false); // ✅ 에러 상태 추가
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

    // 데이터 매핑
    selectedBakery.value = {
      id: data.id,
      bakeryName: data.name,
      location: data.address,
      rating: parseFloat(data.avg_rating) || 0.0,
      description: data.description,
      image: `https://source.unsplash.com/random/800x600/?bakery&sig=${data.id}`,
      tags: (data.representative_tags && String(data.representative_tags).trim() !== "") 
            ? String(data.representative_tags).split(',') 
            : ['추천맛집'],
      menu: data.products ? data.products.map(p => ({
        id: p.id,
        name: p.name,
        price: p.price,
        category: p.category,
        img: p.image_url || `https://source.unsplash.com/random/200x200/?bread&sig=${p.id}`
      })) : []
    };

  } catch (error) {
    console.error('상세 정보 로드 실패:', error);
    isError.value = true; // ✅ 에러 발생 시 플래그 설정
    selectedBakery.value = null; // 데이터 초기화
  } finally {
    isLoading.value = false;
    // 아이콘 렌더링
    setTimeout(() => {
      if (window.lucide) window.lucide.createIcons();
    }, 100);
  }
};

const generateAISummary = async () => {
  // 로딩 표시용 임시 데이터
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

onMounted(() => {
  fetchBakeryDetail();
});
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>