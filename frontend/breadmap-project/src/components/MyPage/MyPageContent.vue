<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { BookOpen, Star, Award, Settings } from 'lucide-vue-next';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const isLoading = ref(true);
const userInfo = ref(null);
const router = useRouter();

// 캐릭터 이미지 매핑
const characterImages = {
  hamster: 'https://cdn-icons-png.flaticon.com/512/235/235394.png',
  bear: 'https://cdn-icons-png.flaticon.com/512/235/235388.png',
  lion: 'https://cdn-icons-png.flaticon.com/512/235/235352.png'
};

const characterName = computed(() => {
  if (!userInfo.value) return '';
  const type = userInfo.value.character_type;
  if (type === 'hamster') return '아기 빵스터 🐹';
  if (type === 'bear') return '미식가 곰돌이 🐻';
  if (type === 'lion') return '전설의 사자왕 🦁';
  return '빵지순례자';
});

const progressWidth = computed(() => {
  if (!userInfo.value) return '0%';
  const percent = (userInfo.value.exp / userInfo.value.max_exp) * 100;
  return `${Math.min(percent, 100)}%`;
});

// 더미 뱃지 데이터 (백엔드에 아직 없다면 UI용으로 사용)
const dummyBadges = [
  { name: '첫 리뷰', icon: '📝' },
  { name: '소금빵 러버', icon: '🥐' },
  { name: '오픈런', icon: '🏃' },
  { name: '빵지순례자', icon: '🗺️' }
];

const fetchUserProfile = async () => {
  try {
    const token = authStore.token;
    if (!token) return;

    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: { Authorization: `Token ${token}` }
    });
    
    // 백엔드 데이터에 뱃지가 없으면 더미 데이터 병합 (UI 확인용)
    userInfo.value = {
      ...response.data,
      badges: response.data.badges || dummyBadges 
    };
  } catch (error) {
    console.error('프로필 로드 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<template>
  <div class="bg-[#F9F7F2] min-h-screen pb-20">
    
    <!-- 로딩 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center h-screen">
      <div class="animate-spin rounded-full h-10 w-10 border-4 border-teal-800 border-t-transparent"></div>
      <p class="mt-4 text-teal-800 font-bold">내 정보를 불러오는 중...</p>
    </div>

    <!-- 데이터 로드 완료 -->
    <div v-else-if="userInfo">
      
      <!-- 1. 프로필 헤더 (캐릭터 & 레벨) -->
      <div class="bg-[#1D4E45] text-white pt-12 pb-20 px-6 rounded-b-[50px] relative shadow-xl">
        <!-- 배경 패턴 -->
        <div class="absolute top-0 left-0 w-full h-full opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>

        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8 relative z-10">
          
          <!-- 캐릭터 (왼쪽) -->
          <div class="relative group cursor-pointer transition-transform hover:scale-105 duration-300 shrink-0">
            <div class="absolute -inset-4 bg-white/10 rounded-full blur-2xl animate-pulse"></div>
            <div class="w-40 h-40 bg-[#F9F7F2] rounded-full border-4 border-orange-400 flex items-center justify-center overflow-hidden shadow-2xl relative z-10">
              <img :src="characterImages[userInfo.character_type] || characterImages.hamster" class="w-24 h-24 object-contain">
            </div>
            <div class="absolute -bottom-2 -right-2 bg-orange-500 text-white font-bold px-4 py-1.5 rounded-full border-2 border-white shadow-lg">
              Lv.{{ userInfo.level }}
            </div>
          </div>

          <!-- 정보 (오른쪽) -->
          <div class="flex-1 text-center md:text-left w-full">
            <div class="flex flex-col md:flex-row md:items-end gap-2 mb-2 justify-center md:justify-start">
              <h2 class="text-3xl font-bold font-serif">{{ userInfo.nickname }}</h2>
              <span class="text-teal-200 text-sm pb-1">{{ characterName }}</span>
            </div>

            <!-- 경험치 바 -->
            <div class="w-full bg-black/20 h-5 rounded-full overflow-hidden relative border border-white/10 mb-2">
              <div class="bg-gradient-to-r from-orange-400 to-yellow-400 h-full rounded-full transition-all duration-1000 relative" :style="{ width: progressWidth }">
                <div class="absolute top-0 left-0 w-full h-full bg-white/30 animate-[shimmer_2s_infinite]"></div>
              </div>
              <span class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[10px] font-bold tracking-widest text-white/90 drop-shadow-md">
                EXP {{ userInfo.exp }} / {{ userInfo.max_exp }}
              </span>
            </div>
            
            <p class="text-xs text-teal-300 text-center md:text-left">
              다음 레벨까지 <strong>{{ userInfo.max_exp - userInfo.exp }} EXP</strong> 남았어요! 힘내세요 🐾
            </p>

            <!-- 스탯 요약 -->
            <div class="flex justify-center md:justify-start gap-8 mt-6">
                          <div class="text-center md:text-left">
                            <p class="text-2xl font-bold text-white">{{ userInfo.visit_count }}</p>
                            <p class="text-xs text-teal-300 uppercase tracking-wider">Visits</p>
                          </div>
                          <router-link :to="{ name: 'myreview' }" class="text-center cursor-pointer hover:opacity-80 transition-opacity">
                            <p class="text-2xl font-bold text-white">{{ userInfo.review_count }}</p>
                            <p class="text-xs text-teal-300 uppercase tracking-wider">Reviews</p>
                          </router-link>              <div class="text-center md:text-left">
                <p class="text-2xl font-bold text-white">{{ userInfo.badges.length }}</p>
                <p class="text-xs text-teal-300 uppercase tracking-wider">Badges</p>
              </div>
            </div>
          </div>

          <!-- 상단 설정 버튼 -->
          <div class="absolute top-0 right-0 flex gap-4">     
          <button @click="router.push({ name: 'editprofile' })" class="text-white/70 hover:text-white transition-colors">
            <Settings class="w-6 h-6" />
          </button>
          </div>
        </div>
      </div>

      <!-- 메인 컨텐츠 영역 (그리드 레이아웃 적용) -->
      <div class="max-w-5xl mx-auto px-6 -mt-12 space-y-6 relative z-20">
        
        <!-- 상단 2열 그리드: 여권 & 취향분석 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <!-- 2. 📜 베이커리 여권 -->
          <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0] h-full flex flex-col">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2">
                <BookOpen class="w-6 h-6 text-orange-500" /> 
                My Bread Passport
              </h3>
              <span class="text-xs font-bold text-teal-600 bg-teal-50 px-2 py-1 rounded-lg">
                {{ userInfo.visited_stores.length }}개 정복완료
              </span>
            </div>

            <!-- 스탬프 그리드 (4열) -->
            <div class="grid grid-cols-4 gap-4 flex-1 content-start">
              <div v-for="(store, idx) in userInfo.visited_stores" :key="store.id" 
                   class="aspect-square rounded-2xl border-2 border-orange-200 bg-orange-50/30 flex flex-col items-center justify-center p-1 cursor-pointer hover:-translate-y-1 transition-transform shadow-sm group"
                   title="방문 완료!">
                <div class="text-3xl mb-1 group-hover:scale-110 transition-transform">🥐</div>
                <p class="text-[10px] text-center text-[#4A4036] font-bold leading-tight line-clamp-1 w-full px-1">{{ store.name }}</p>
              </div>
              <!-- 빈 칸 채우기 (최소 8개 유지하도록 계산) -->
              <div v-for="i in Math.max(0, 8 - userInfo.visited_stores.length)" :key="`empty-${i}`"
                   class="aspect-square rounded-2xl border-2 border-dashed border-gray-200 flex items-center justify-center opacity-30">
                <span class="text-gray-300 text-xl font-bold">?</span>
              </div>
            </div>
          </div>

          <!-- 3. 🔮 취향 분석 -->
          <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0] h-full flex flex-col">
            <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2 mb-6">
              <Star class="w-6 h-6 text-purple-500" /> 
              Taste Analysis
            </h3>
            
            <div v-if="Object.keys(userInfo.taste_stats).length > 0" class="flex-1 flex flex-col justify-center">
              <p class="text-sm text-gray-600 mb-6 bg-gray-50 p-4 rounded-xl border border-gray-100">
                <strong class="text-teal-800">{{ userInfo.nickname }}</strong>님은<br> 
                <span class="text-orange-500 font-bold text-lg">"{{ Object.keys(userInfo.taste_stats)[0] }}"</span> 스타일을 가장 선호해요! 😋
              </p>
              
              <div class="space-y-4">
                <div v-for="(count, tag) in userInfo.taste_stats" :key="tag" class="space-y-1">
                  <div class="flex justify-between text-xs text-gray-500 font-bold px-1">
                    <span>{{ tag }}</span>
                    <span>{{ count }}회</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-3 overflow-hidden shadow-inner">
                    <div class="h-full bg-teal-600 rounded-full transition-all duration-1000 relative overflow-hidden" 
                         :style="{ width: `${Math.min((count / 5) * 100, 100)}%` }">
                         <div class="absolute top-0 left-0 w-full h-full bg-white/20"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="flex-1 flex flex-col items-center justify-center text-center py-6 text-gray-400">
              <div class="bg-gray-100 p-4 rounded-full mb-3">
                <Star class="w-8 h-8 text-gray-300" />
              </div>
              <p class="text-sm">아직 데이터가 부족해요.<br>리뷰를 남겨주시면 분석해드릴게요! 📝</p>
            </div>
          </div>

        </div>

        <!-- 하단: 뱃지 컬렉션 (가로 전체) -->
        <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0]">
          <h3 class="text-xl font-bold text-[#1D4E45] flex items-center gap-2 mb-6">
            <Award class="w-6 h-6 text-yellow-500" /> 
            Badge Collection
          </h3>
          
          <div class="flex gap-4 overflow-x-auto pb-4 hide-scrollbar">
            <!-- 획득한 뱃지 -->
            <div v-for="(badge, idx) in userInfo.badges" :key="idx" 
                 class="flex-shrink-0 w-24 h-32 bg-gradient-to-b from-[#FFFDF9] to-[#F2EFE9] border border-[#E5E0D8] rounded-2xl flex flex-col items-center justify-center p-3 shadow-sm hover:-translate-y-2 transition-transform duration-300 cursor-pointer group">
              <div class="text-4xl mb-3 filter drop-shadow-md group-hover:scale-110 transition-transform">{{ badge.icon }}</div>
              <span class="text-xs font-bold text-[#4A4036] text-center leading-tight">{{ badge.name }}</span>
            </div>
            
            <!-- 잠긴 뱃지 (예시) -->
            <div v-for="i in 3" :key="`locked-${i}`" 
                 class="flex-shrink-0 w-24 h-32 bg-gray-50 border border-gray-100 rounded-2xl flex flex-col items-center justify-center p-3 opacity-60">
              <div class="text-3xl mb-3 grayscale opacity-30">🔒</div>
              <span class="text-xs font-bold text-gray-400">Locked</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>