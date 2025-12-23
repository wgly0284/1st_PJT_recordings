<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { Star, Award, Settings } from 'lucide-vue-next';
import { useRouter } from 'vue-router';
// 👇 1. 분리한 컴포넌트 import
import BreadPassport from './BreadPassport.vue';

const authStore = useAuthStore();
const isLoading = ref(true);
const userInfo = ref(null);
const router = useRouter();

// 팔로우 모달 관련
const showFollowModal = ref(false);
const followModalType = ref('followers');
const followList = ref([]);

// 1️⃣ 10단계 레벨 및 캐릭터 설정
const LEVEL_CONFIG = {
  1: { name: '아기빵쥐', icon: '🐭', color: 'text-gray-400', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  2: { name: '식빵햄찌', icon: '🐹', color: 'text-orange-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  3: { name: '호빵토끼', icon: '🐰', color: 'text-pink-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235372.png' },
  4: { name: '모닝코기', icon: '🐶', color: 'text-yellow-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235415.png' },
  5: { name: '크루아상여우', icon: '🦊', color: 'text-orange-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235368.png' },
  6: { name: '브리오슈곰', icon: '🐻', color: 'text-brown-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235388.png' },
  7: { name: '사워도우울프', icon: '🐺', color: 'text-gray-600', img: 'https://cdn-icons-png.flaticon.com/512/235/235356.png' },
  8: { name: '초코표범', icon: '🐆', color: 'text-yellow-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235377.png' },
  9: { name: '바게트호크', icon: '🦅', color: 'text-teal-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235386.png' },
  10: { name: '황금밀 유니콘', icon: '🦄', color: 'text-purple-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235359.png' },
};

const currentLevelInfo = computed(() => {
  if (!userInfo.value) return LEVEL_CONFIG[1];
  return LEVEL_CONFIG[userInfo.value.level] || LEVEL_CONFIG[1];
});

const progressWidth = computed(() => {
  if (!userInfo.value) return '0%';
  const percent = (userInfo.value.exp / userInfo.value.next_exp) * 100; 
  return `${Math.min(percent, 100)}%`;
});

// 더미 데이터
const dummyBadges = [
  { name: '식빵 장인', icon: '🍞', description: '같은 빵집 5회 방문' },
  { name: '크루아상 헌터', icon: '🥐', description: '크루아상 리뷰 10개' },
  { name: '부산 빵지순례자', icon: '🌊', description: '부산 지역 빵집 정복' }
];

const dummyStamps = [
  { id: 1, name: '성심당', date: '2024.12.25', location: '대전' },
  { id: 2, name: '이성당', date: '2025.01.01', location: '군산' },
  { id: 3, name: '태극당', date: '2025.01.10', location: '서울' },
];

const fetchUserProfile = async () => {
  try {
    const token = authStore.token;
    if (!token) return;

    // 실제로는 API 호출
    // const response = await axios.get('...', { headers... });
    
    setTimeout(() => {
        userInfo.value = {
            nickname: '빵순이',
            level: 6,
            level_title: '브리오슈곰',
            exp: 1850,
            next_exp: 2200,
            profile_image_url: null,
            follower_count: 128,
            following_count: 45,
            review_count: 32,
            post_count: 10,
            badges: dummyBadges,
            visited_stores: dummyStamps,
            taste_stats: { '하드계열': 15, '조리빵': 8, '디저트': 5 },
            date_joined: '2023-05-20'
        };
        isLoading.value = false;
    }, 800);

  } catch (error) {
    console.error('프로필 로드 실패:', error);
    isLoading.value = false;
  }
};

const handleImageError = (event) => {
  event.target.style.display = 'none';
};

const openFollowModal = async (type) => {
  followModalType.value = type;
  showFollowModal.value = true;
};
const closeFollowModal = () => {
  showFollowModal.value = false;
  followList.value = [];
};

onMounted(() => {
  fetchUserProfile();
});
</script>

<template>
  <div class="bg-[#F9F7F2] min-h-screen pb-20 font-sans">
    
    <!-- 로딩 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center h-screen">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-orange-400 border-t-transparent"></div>
      <p class="mt-4 text-[#4A4036] font-bold animate-pulse">오븐 예열 중...</p>
    </div>

    <!-- 데이터 로드 완료 -->
    <div v-else-if="userInfo">
      
      <!-- 1. 프로필 헤더 -->
      <div class="bg-[#1D4E45] text-white pt-12 pb-24 px-6 rounded-b-[60px] relative shadow-2xl overflow-hidden">
        <!-- 배경 데코레이션 -->
        <div class="absolute top-0 left-0 w-full h-full opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>
        <div class="absolute -right-10 -top-10 w-64 h-64 bg-yellow-400 rounded-full mix-blend-overlay filter blur-3xl opacity-20"></div>
        <div class="absolute -left-10 bottom-0 w-64 h-64 bg-orange-500 rounded-full mix-blend-overlay filter blur-3xl opacity-20"></div>

        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8 relative z-10">
          
          <!-- 캐릭터/프로필 이미지 -->
          <div class="relative group cursor-pointer transition-transform hover:scale-105 duration-300 shrink-0">
            <div class="absolute -inset-4 bg-gradient-to-tr from-orange-400 to-yellow-300 rounded-full blur-xl opacity-40 animate-pulse"></div>
            
            <div class="w-40 h-40 bg-[#F9F7F2] rounded-full border-[6px] border-orange-200 flex items-center justify-center overflow-hidden shadow-2xl relative z-10">
              <img v-if="userInfo.profile_image_url" :src="userInfo.profile_image_url" class="w-full h-full object-cover" @error="handleImageError">
              <img v-else :src="currentLevelInfo.img" class="w-28 h-28 object-contain drop-shadow-lg">
            </div>
            <!-- 레벨 뱃지 -->
            <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 bg-orange-500 text-white font-bold px-5 py-1.5 rounded-full border-4 border-[#1D4E45] shadow-lg whitespace-nowrap z-20 flex items-center gap-1">
              <span class="text-xs">Lv.{{ userInfo.level }}</span>
              <span class="text-sm">{{ currentLevelInfo.name }}</span>
            </div>
          </div>

          <!-- 정보 (오른쪽) -->
          <div class="flex-1 text-center md:text-left w-full">
            <div class="flex flex-col md:flex-row md:items-end gap-3 mb-4 justify-center md:justify-start">
              <h2 class="text-4xl font-extrabold tracking-tight">{{ userInfo.nickname }}</h2>
              <span class="text-2xl animate-bounce">{{ currentLevelInfo.icon }}</span>
            </div>

            <!-- 경험치 바 -->
            <div class="relative mb-2 group">
              <div class="w-full bg-black/20 h-6 rounded-full overflow-hidden backdrop-blur-sm border border-white/10">
                <div class="bg-gradient-to-r from-orange-400 via-yellow-400 to-orange-400 h-full rounded-full transition-all duration-1000 relative bg-[length:200%_100%] animate-[shimmer_2s_infinite]" 
                     :style="{ width: progressWidth }">
                </div>
              </div>
              <div class="absolute top-0 w-full text-center text-[11px] font-bold text-white/90 leading-6 drop-shadow-md">
                {{ userInfo.exp }} / {{ userInfo.next_exp }} EXP
              </div>
            </div>
            
            <p class="text-sm text-teal-200/80 text-center md:text-left mb-6">
              "{{ currentLevelInfo.name }}" 단계입니다. 맛있는 빵을 찾아 떠나보세요! 🚀
            </p>

            <!-- 스탯 요약 -->
            <div class="flex justify-center md:justify-start gap-8 p-4 bg-white/5 rounded-2xl backdrop-blur-sm border border-white/5 inline-flex">
              <div @click="openFollowModal('followers')" class="text-center cursor-pointer hover:text-orange-300 transition-colors">
                <p class="text-xl font-bold text-white">{{ userInfo.follower_count }}</p>
                <p class="text-[10px] text-teal-200 uppercase tracking-wider">Followers</p>
              </div>
              <div class="border-r border-white/10"></div>
              <div @click="openFollowModal('following')" class="text-center cursor-pointer hover:text-orange-300 transition-colors">
                <p class="text-xl font-bold text-white">{{ userInfo.following_count }}</p>
                <p class="text-[10px] text-teal-200 uppercase tracking-wider">Following</p>
              </div>
              <div class="border-r border-white/10"></div>
              <div class="text-center">
                <p class="text-xl font-bold text-white">{{ userInfo.review_count }}</p>
                <p class="text-[10px] text-teal-200 uppercase tracking-wider">Reviews</p>
              </div>
            </div>
          </div>

          <!-- 설정 버튼 -->
          <button @click="router.push({ name: 'editprofile' })" class="absolute top-0 right-0 p-2 text-white/50 hover:text-white hover:bg-white/10 rounded-full transition-all">
            <Settings class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- 메인 컨텐츠 영역 -->
      <div class="max-w-5xl mx-auto px-4 sm:px-6 -mt-16 space-y-8 relative z-20 pb-12">
        
        <!-- 그리드: 여권 & 취향분석 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          <!-- 👇 2. 컴포넌트로 교체! (코드가 훨씬 깔끔해졌죠?) -->
          <BreadPassport 
            :visited-stores="userInfo.visited_stores" 
            :date-joined="userInfo.date_joined"
          />

          <!-- 3. 취향 분석 -->
          <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0] h-full flex flex-col">
            <h3 class="text-xl font-bold text-[#4A4036] flex items-center gap-2 mb-6">
              <Star class="w-6 h-6 text-purple-500" /> Taste Analysis
            </h3>
            
            <div v-if="Object.keys(userInfo.taste_stats).length > 0" class="flex-1 flex flex-col justify-center">
              <div class="bg-gray-50 p-5 rounded-2xl border border-gray-100 mb-6 text-center">
                <p class="text-sm text-gray-500 mb-1">가장 많이 먹은 빵은?</p>
                <p class="text-2xl font-bold text-teal-700">
                  "{{ Object.keys(userInfo.taste_stats).reduce((a, b) => userInfo.taste_stats[a] > userInfo.taste_stats[b] ? a : b) }}" 
                  <span class="text-2xl">👑</span>
                </p>
              </div>
              
              <div class="space-y-4">
                <div v-for="(count, tag) in userInfo.taste_stats" :key="tag" class="space-y-1">
                  <div class="flex justify-between text-xs text-gray-500 font-bold px-1">
                    <span>{{ tag }}</span>
                    <span>{{ count }}회</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-3 overflow-hidden shadow-inner">
                    <div class="h-full bg-gradient-to-r from-teal-500 to-teal-400 rounded-full relative" 
                         :style="{ width: `${Math.min((count / 15) * 100, 100)}%` }">
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- 하단: 뱃지 컬렉션 (여기도 BadgeList.vue로 분리하면 좋습니다) -->
        <div class="bg-white rounded-3xl p-8 shadow-xl border border-[#F0EBE0]">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-[#1D4E45] flex items-center gap-2">
              <Award class="w-6 h-6 text-yellow-500" /> Badge Collection
            </h3>
            <span class="text-xs font-bold text-gray-400 bg-gray-100 px-3 py-1 rounded-full">
              {{ userInfo.badges.length }}개 획득
            </span>
          </div>
          
          <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-4">
            <div v-for="(badge, idx) in userInfo.badges" :key="idx" 
                 class="aspect-[3/4] bg-gradient-to-b from-[#FFFDF9] to-[#F2EFE9] border border-[#E5E0D8] rounded-2xl flex flex-col items-center justify-center p-2 shadow-sm hover:-translate-y-1 hover:shadow-md transition-all cursor-pointer group relative overflow-hidden">
              <div class="absolute inset-0 bg-yellow-400/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div class="absolute -top-1 right-2 w-4 h-6 bg-red-500/10 rounded-b-full"></div>
              <div class="text-3xl mb-3 filter drop-shadow-sm group-hover:scale-110 transition-transform duration-300">{{ badge.icon }}</div>
              <span class="text-[11px] font-bold text-[#4A4036] text-center leading-tight mb-1">{{ badge.name }}</span>
              <div class="absolute bottom-0 left-0 w-full bg-black/80 text-white text-[9px] py-1 text-center opacity-0 group-hover:opacity-100 transition-opacity">
                {{ badge.description }}
              </div>
            </div>
            
            <div v-for="i in 2" :key="`locked-${i}`" 
                 class="aspect-[3/4] bg-gray-50 border border-dashed border-gray-200 rounded-2xl flex flex-col items-center justify-center p-2 opacity-50 grayscale">
              <div class="text-3xl mb-2 opacity-20">🏆</div>
              <span class="text-[10px] font-bold text-gray-400">???</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 팔로우 모달 (기존 코드 유지) -->
    <Transition name="modal">
      <div v-if="showFollowModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" @click.self="closeFollowModal">
        <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full max-h-[80vh] overflow-hidden flex flex-col">
          <div class="bg-[#1D4E45] text-white p-5 flex items-center justify-between shrink-0">
            <h3 class="text-lg font-bold">
              {{ followModalType === 'followers' ? '나를 따르는 빵순이들' : '내가 팔로우한 빵순이들' }}
            </h3>
            <button @click="closeFollowModal" class="text-white/70 hover:text-white transition-colors">✕</button>
          </div>
          <div class="p-6 overflow-y-auto">
             <div class="text-center text-gray-400 py-8">목록을 불러오는 중...</div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Gaegu:wght@400;700&display=swap');

/* 전체 폰트 적용 */
div {
  font-family: 'Noto Sans KR', sans-serif;
}

/* 칭호 등 귀여운 부분에 포인트 폰트 */
h2, .font-serif {
  font-family: 'Gaegu', cursive; /* 귀여운 손글씨 폰트 */
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .bg-white, .modal-leave-active .bg-white { transition: transform 0.2s ease; }
.modal-enter-from .bg-white, .modal-leave-to .bg-white { transform: scale(0.95); }
</style>