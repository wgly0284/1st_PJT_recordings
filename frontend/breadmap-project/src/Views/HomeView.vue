<template>
  <main class="flex-grow bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] overflow-hidden">
    <!-- 1. Hero Section -->
    <section class="relative min-h-screen flex flex-col justify-center items-center pt-24 pb-24">
      <!-- 수채화 배경 얼룩 -->
      <div
        class="absolute top-0 right-0 w-[600px] h-[600px]
               bg-[#F3B37A]/15 rounded-full blur-3xl -z-10 translate-x-1/3 -translate-y-1/4"
      ></div>
      <div
        class="absolute bottom-0 left-0 w-[500px] h-[500px]
               bg-[#9AC89A]/15 rounded-full blur-3xl -z-10 -translate-x-1/3 translate-y-1/4"
      ></div>

      <!-- 메인 컨텐츠 영역 -->
      <div class="w-full px-4 md:px-8 flex flex-col items-center gap-10 relative z-10 text-center">
        
        <!-- 2. 이미지 영역 (진열대) -->
        <div class="relative w-full max-w-6xl flex items-center justify-center -mb-8 sm:-mb-12 mt-4">
          <div class="absolute inset-x-20 inset-y-24 bg-gradient-to-r from-orange-100/40 via-yellow-100/40 to-orange-100/40 rounded-full blur-[60px]"></div>
          
          <img
            :src="shelfImage"
            class="relative w-full h-auto object-contain drop-shadow-md z-10 opacity-95"
            style="-webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%); mask-image: linear-gradient(to bottom, black 60%, transparent 100%);"
            alt="Breadtopia Shelf"
          />
        </div>

        <!-- 3. 텍스트 및 버튼 -->
        <div class="space-y-6 flex flex-col items-center relative z-20 mt-[-2rem]">
          <h1 class="text-5xl md:text-7xl font-jua text-[#6B4A38] leading-tight drop-shadow-sm">
            친구들과
            <span class="inline-block text-[#C99768] relative px-2">
              빵지순례
              <svg class="absolute -bottom-2 left-0 w-full h-3 text-[#F3B37A]/40" viewBox="0 0 100 10" preserveAspectRatio="none">
                <path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="8" fill="none" />
              </svg>
            </span>
            <br class="hidden md:block" /> 떠나기
          </h1>

          <p class="text-lg md:text-xl text-[#8B6A55] font-jua leading-relaxed max-w-lg opacity-90">
            진열대에 가득 찬 갓 구운 빵들처럼,<br />
            동글동글 귀여운 빵집들을 지도 위에서 찾아보세요. 🐶🍞
          </p>

          <div class="flex flex-col sm:flex-row gap-4 pt-4 font-jua w-full justify-center">
            <button
              @click="$router.push('/map')"
              class="group px-8 py-4 bg-[#F3B37A] text-white text-xl
                     rounded-3xl shadow-[0_6px_14px_rgba(201,151,104,0.4)]
                     hover:bg-[#C99768] hover:shadow-[0_4px_10px_rgba(201,151,104,0.3)]
                     active:translate-y-[1px]
                     transition-all flex items-center justify-center gap-2"
            >
              <span>빵 지도 열기</span>
              <span class="group-hover:rotate-12 transition-transform">🗺️</span>
            </button>

            <button
              class="px-8 py-4 bg-white/80 border border-[#F3B37A]/40 backdrop-blur-sm
                     text-[#C99768] text-xl rounded-3xl
                     hover:bg-[#FFF3DD] transition-colors
                     shadow-sm"
            >
              내 빵 취향 보기
            </button>
          </div>
        </div>

        <!-- 검색바 -->
        <div class="w-full max-w-xl mt-4 relative z-30">
          <div class="bg-white/90 backdrop-blur p-2 rounded-full shadow-[0_8px_24px_rgba(201,151,104,0.25)] flex items-center gap-3 border-4 border-[#FFF3DD]/80 hover:border-[#F3B37A]/50 transition-all duration-300">
            <div class="pl-5 text-[#C99768]">
              <Search class="w-6 h-6" />
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="어떤 빵 친구를 찾으시나요?"
              class="flex-grow py-3 px-2 bg-transparent focus:outline-none text-[#6B4A38] placeholder-[#C99768]/60 font-jua text-lg"
              @keyup.enter="handleSearch"
            >
            <button
              @click="handleSearch"
              class="bg-[#F3B37A] text-white w-14 h-14 rounded-full flex items-center justify-center hover:bg-[#C99768] transition transform hover:scale-110 shadow-md group"
            >
              <PawPrint class="w-7 h-7 fill-white/20 group-hover:rotate-12 transition-transform" />
            </button>
          </div>
        </div>

      </div>

      <!-- 스크롤 유도 -->
      <div
        class="absolute bottom-8 text-center animate-bounce opacity-60 font-jua text-[#8B6A55] z-10 cursor-pointer hover:opacity-100 transition-opacity"
        @click="scrollToContent"
      >
        <p class="text-sm mb-1">아래로 스크롤</p>
        <ArrowDown class="w-6 h-6 text-[#C99768] mx-auto" />
      </div>
    </section>

    <!-- 1.5 Daily Recommendation (AI 추천) -->
    <DailyBakeryCard />

    <!-- 2. 어디로 갈까요? 지역 선택 -->
    <section id="content-start" class="py-20 bg-white relative overflow-hidden">
      <!-- 배경 장식 -->
      <div class="absolute top-10 right-10 w-64 h-64 bg-orange-100 rounded-full opacity-20 blur-3xl"></div>
      <div class="absolute bottom-10 left-10 w-72 h-72 bg-teal-100 rounded-full opacity-20 blur-3xl"></div>

      <div class="max-w-[1400px] mx-auto px-6 relative z-10">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-[#1D4E45] mb-3 font-jua">
            어디로 갈까요? 🗺️
          </h2>
          <p class="text-gray-600 font-jua">지역을 선택하면 근처 빵집을 추천해드려요</p>
        </div>

        <!-- 지역 그리드 -->
        <div class="grid grid-cols-4 md:grid-cols-8 gap-6 md:gap-8">
          <button
            v-for="region in regions"
            :key="region.id"
            @click="goToRegion(region.id)"
            class="group relative flex flex-col items-center justify-center w-full aspect-square hover:scale-110 hover:-translate-y-2 transition-all duration-300 active:scale-95"
          >
            <!-- 큼직하고 단순한 곰돌이 발바닥 SVG 배경 -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[130%] h-[130%] z-0">
              <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" class="w-full h-full drop-shadow-sm">
                <!-- 메인 패드 -->
                <circle cx="100" cy="115" r="55" 
                        class="fill-[#FFF3DD] group-hover:fill-[#FFE8CC] transition-colors duration-300" />
                <!-- 발가락들 -->
                <circle cx="45" cy="70" r="22" 
                        class="fill-[#FFF3DD] group-hover:fill-[#FFE8CC] transition-colors duration-300" />
                <circle cx="100" cy="45" r="22" 
                        class="fill-[#FFF3DD] group-hover:fill-[#FFE8CC] transition-colors duration-300" />
                <circle cx="155" cy="70" r="22" 
                        class="fill-[#FFF3DD] group-hover:fill-[#FFE8CC] transition-colors duration-300" />
              </svg>
            </div>

            <!-- 콘텐츠 -->
            <div class="relative z-10 flex flex-col items-center pt-6">
              <div class="text-4xl md:text-5xl mb-1 transform group-hover:scale-125 transition-transform duration-300 drop-shadow-sm filter">
                {{ region.icon }}
              </div>
              <h3 class="text-sm md:text-base font-jua text-[#6B4A38] font-bold bg-white/40 px-3 py-0.5 rounded-full backdrop-blur-[2px] group-hover:text-orange-600 transition-colors">
                {{ region.name }}
              </h3>
            </div>
          </button>
        </div>
      </div>
    </section>

    <!-- 3. Weekly Curation -->
    <section class="py-24 bg-[#FFF9F0]/90 relative">
      <div class="absolute top-0 left-0 w-full overflow-hidden leading-none rotate-180">
        <svg
          class="relative block w-[calc(100%+1.3px)] h-[50px]"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1200 120"
          preserveAspectRatio="none"
        >
          <path
            d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"
            fill="#FCD5CF"
          />
        </svg>
      </div>

      <div class="max-w-[1200px] mx-auto px-6 relative z-10">
        <div class="text-center mb-16">
          <span
            class="inline-flex items-center gap-2 text-[#C99768] tracking-wide text-base
                   bg-[#FFF3DD] px-6 py-2 rounded-full font-jua shadow-md border-2 border-[#FFE8CC]"
          >
            <span>🍞</span>
            <span>Weekly Pick</span>
          </span>

          <h2 class="text-4xl md:text-5xl font-jua text-[#6B4A38] mt-6 leading-relaxed">
            이번 주
            <span class="text-[#C99768] relative inline-block">
              <span class="relative z-10">빵지순례 코스</span>
              <span class="absolute bottom-1 left-0 w-full h-3 bg-[#F3B37A]/30 -rotate-1"></span>
            </span>
            모음
          </h2>
          <p class="mt-4 text-lg text-[#8B6A55] font-jua">
            바구니에 쏙 담고 싶은 따뜻한 동네 빵집들을 모았어요 🧺
          </p>
        </div>

        <BakeryGrid :bakeries="bakeries" @open-detail="openDetail" class="font-jua" />

        <div class="text-center mt-24">
          <button
            @click="$router.push('/map')"
            class="group inline-flex items-center gap-3 px-8 py-3 bg-[#FFF3DD] border-2 border-[#F3B37A] rounded-3xl
                   text-[#8B6A55] text-xl font-jua
                   shadow-[0_4px_0_#F3B37A] hover:shadow-[0_2px_0_#F3B37A]
                   hover:translate-y-[2px] transition-all duration-200"
          >
            <span>다른 빵집도 구경갈래요!</span>
            <ArrowRight class="w-6 h-6 group-hover:translate-x-1 transition-transform text-[#C99768]" />
          </button>
        </div>
      </div>
    </section>

    <!-- [수정됨] 4. Featured Section (나만의 빵 캐릭터) -->
    <!-- 디자인 컨셉: 폴라로이드 사진관 + 도감 수집 느낌 -->
    <section class="py-32 relative overflow-hidden">
      <!-- 배경: 부드러운 그라데이션과 패턴 -->
      <div class="absolute inset-0 bg-gradient-to-br from-[#FFF3DD] to-[#F9F7F2] z-0"></div>
      <div class="absolute inset-0 opacity-10 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] z-0"></div>

      <!-- 장식용 부유물 (떠다니는 느낌) -->
      <div class="absolute top-10 left-10 text-4xl animate-bounce-slow opacity-60">🥨</div>
      <div class="absolute bottom-20 right-10 text-4xl animate-bounce-slow opacity-60 delay-700">🥯</div>
      <div class="absolute top-1/3 right-20 w-32 h-32 bg-[#F3B37A]/10 rounded-full blur-2xl"></div>

      <div class="max-w-[1100px] mx-auto px-6 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-12 md:gap-20">
          
          <!-- 왼쪽: 캐릭터 카드 (폴라로이드 스타일) -->
          <div class="md:w-1/2 w-full flex justify-center">
            <div class="relative group cursor-pointer perspective-1000">
              <!-- 카드 본체 -->
              <div class="relative bg-white p-4 pb-16 rounded shadow-[0_15px_30px_rgba(0,0,0,0.1)] transform transition-transform duration-500 hover:rotate-2 hover:scale-105 border border-gray-100 w-[320px] sm:w-[380px]">
                
                <!-- 상단 테이프 장식 -->
                <div class="absolute -top-4 left-1/2 -translate-x-1/2 w-32 h-8 bg-[#F3B37A]/40 rotate-1 backdrop-blur-sm shadow-sm z-20"></div>

                <!-- 이미지 프레임 -->
                <div class="aspect-square w-full bg-[#FFF9F0] rounded-inner overflow-hidden border-2 border-[#EAEaea] relative">
                  <!-- 캐릭터 이미지 -->
                  <img
                    :src="randomMascot"
                    class="w-full h-full object-contain p-6 hover:scale-110 transition-transform duration-500"
                    alt="My Bread Character"
                  />
                  <!-- 레벨 뱃지 -->
                </div>

                <!-- 하단 텍스트 (손글씨 느낌) -->
                <div class="absolute bottom-4 left-0 w-full text-center">
                  <p class="font-jua text-2xl text-[#6B4A38] mb-1">나의 빵 친구</p>
                  <p class="font-jua text-sm text-[#C99768]">총 9종류를 모아보세요!</p>
                </div>

                <!-- 스탬프 장식 (우측 하단) -->
                <div class="absolute bottom-4 right-4 w-12 h-12 border-2 border-[#EF6C00] rounded-full flex items-center justify-center opacity-20 -rotate-12">
                  <span class="text-[10px] font-bold text-[#EF6C00] uppercase">Collection</span>
                </div>
              </div>

              <!-- 뒷배경 장식 카드 (겹쳐진 느낌) -->
              <div class="absolute top-2 -right-4 w-full h-full bg-white rounded shadow-sm -z-10 rotate-6 border border-gray-100"></div>
            </div>
          </div>

          <!-- 오른쪽: 텍스트 설명 -->
          <div class="md:w-1/2 w-full text-center md:text-left space-y-6">
            <span class="inline-flex items-center gap-2 px-4 py-1.5 bg-[#1D4E45]/10 text-[#1D4E45] rounded-full text-sm font-bold tracking-wide">
              <span>🧬</span> 빵지순례 성장 시스템
            </span>

            <h2 class="text-4xl md:text-5xl font-jua text-[#6B4A38] leading-tight">
              빵 하나 먹을 때마다<br>
              <span class="text-[#EF6C00] inline-block mt-2 transform -rotate-1 bg-[#FFF3DD] px-2">경험치 +1 UP!</span>
            </h2>

            <p class="text-[#8B6A55] text-lg leading-relaxed font-jua opacity-90">
              처음엔 작고 소중한 <strong>밀가루 반죽</strong>이지만,<br>
              리뷰를 남기고 빵지순례를 다닐수록<br>
              멋진 <strong>식빵 히어로</strong>로 성장한답니다.
            </p>

            <!-- 경험치 바 예시 -->
            <div class="bg-white p-4 rounded-2xl shadow-sm border border-[#FFE8CC] max-w-md mx-auto md:mx-0">
              <div class="flex justify-between text-sm font-bold text-[#6B4A38] mb-1">
                <span>현재 레벨</span>
                <span>다음 레벨까지 30xp</span>
              </div>
              <div class="w-full h-3 bg-[#F0F0F0] rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] w-[70%] rounded-full relative">
                  <div class="absolute right-0 top-0 h-full w-2 bg-white/30 animate-pulse"></div>
                </div>
              </div>
            </div>

            <div class="pt-4">
              <button
                class="px-8 py-4 bg-[#6B4A38] text-white text-xl rounded-2xl
                       font-jua hover:bg-[#5A3E2F] transition-all
                       shadow-[0_8px_20px_rgba(107,74,56,0.3)]
                       hover:shadow-[0_4px_10px_rgba(107,74,56,0.2)]
                       hover:-translate-y-1
                       w-full md:w-auto flex items-center justify-center gap-2 mx-auto md:mx-0"
              >
                <span>내 캐릭터 도감 보기</span>
                <ArrowRight class="w-5 h-5" />
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BakeryGrid from '@/components/common/BakeryGrid.vue'
import DailyBakeryCard from '@/AccountsViews/DailyBakeryCard.vue'
import { ArrowRight, ArrowDown, PawPrint, Search } from 'lucide-vue-next'
import axios from 'axios'

// Assets Import
import shelfImage from '@/assets/images/진열대.png'

// --- [수정됨] 마스코트 이미지 로드 로직 (mascots 폴더의 png 파일) ---
// assets/mascots 폴더 내의 모든 png 파일을 불러옵니다.
const mascotImagesGlob = import.meta.glob('@/assets/mascot/*.png', {
  eager: true,
  import: 'default'
})

const randomMascot = ref('')

const router = useRouter()
const searchQuery = ref('')
const bakeries = ref([])

// 지역 데이터
const regions = ref([
  { id: 'sasang', name: '사상구', searchKeyword: '사상', icon: '🥖', count: '200+' },
  { id: 'busanjin', name: '부산진구', searchKeyword: '부산진', icon: '🥐', count: '800+' },
  { id: 'jung', name: '중구', searchKeyword: '중구', icon: '🍞', count: '200+' },
  { id: 'dong', name: '동구', searchKeyword: '동구', icon: '🥯', count: '100+' },
  { id: 'buk', name: '북구', searchKeyword: '북구', icon: '🥨', count: '100+' },
  { id: 'suyeong', name: '수영구', searchKeyword: '수영', icon: '🧁', count: '100+' },
  { id: 'haeundae', name: '해운대구', searchKeyword: '해운대', icon: '🍰', count: '200+' },
  { id: 'nam', name: '남구', searchKeyword: '남구', icon: '🎂', count: '100+' }
])

const fetchBakeries = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/stores/weekly-pick/')
    bakeries.value = response.data.map(bakery => ({
      id: bakery.id,
      bakeryName: bakery.name,
      name: bakery.name,
      location: bakery.address,
      rating: bakery.avg_rating || 4.5,
      image: bakery.image || 'https://source.unsplash.com/random/800x600/?bakery',
      tags: bakery.product_keywords || ['신선함', '맛있어요'],
      menu: []
    }))
  } catch (error) {
    console.error('빵집 로드 실패:', error)
  }
}

const openDetail = bakery => {
  router.push({ name: 'detail', params: { id: bakery.id } })
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: 'search', query: { search: searchQuery.value } })
  }
}

const goToRegion = (regionId) => {
  router.push({ name: 'region', params: { region: regionId } })
}

const scrollToContent = () => {
  const contentStart = document.getElementById('content-start')
  if (contentStart) {
    contentStart.scrollIntoView({ behavior: 'smooth' })
  }
}

onMounted(() => {
  fetchBakeries()

  // [수정됨] 랜덤 마스코트 이미지 선택 로직
  const imagesArray = Object.values(mascotImagesGlob)
  if (imagesArray.length > 0) {
    const randomIndex = Math.floor(Math.random() * imagesArray.length)
    randomMascot.value = imagesArray[randomIndex]
  } else {
    // 이미지가 없을 경우 기본 이미지
    randomMascot.value = 'https://cdn-icons-png.flaticon.com/512/3014/3014275.png' 
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

@keyframes bounceSlow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.animate-bounce-slow {
  animation: bounceSlow 3s infinite ease-in-out;
}

/* 3D 효과를 위한 Perspective */
.perspective-1000 {
  perspective: 1000px;
}
</style>