<template>
  <main class="flex-grow bg-[#FFFDF9] overflow-hidden">
    
    <!-- 1. Hero Section: 귀엽고 환영하는 분위기 -->
    <section class="relative min-h-screen flex items-center pt-20">
      <!-- 배경 장식 (구름, 언덕) -->
      <div class="absolute top-0 left-0 w-full h-full -z-10 bg-gradient-to-b from-[#FFFDF9] to-[#FFF8E7]"></div>
      <div class="absolute top-20 right-[-10%] w-[600px] h-[600px] bg-[#FFE4C4]/40 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-[#E8F3E8]/50 rounded-full blur-3xl"></div>

      <div class="max-w-[1200px] mx-auto px-6 w-full flex flex-col md:flex-row items-center gap-12">
        
        <!-- 텍스트 -->
        <div class="md:w-1/2 space-y-6 relative z-10 text-center md:text-left">
          <div class="inline-flex items-center gap-2 bg-white border border-orange-100 px-4 py-2 rounded-full shadow-sm animate-bounce-slow">
            <span class="text-xl">🐰</span>
            <span class="text-sm font-bold text-orange-600 tracking-wide font-jua">Breadtopia Open!</span>
          </div>
          
          <!-- 폰트 변경: font-serif -> font-jua -->
          <h1 class="text-5xl md:text-7xl font-jua text-[#4A4036] leading-tight tracking-tight">
            빵 냄새 가득한 <br>
            <span class="text-orange-500 relative inline-block">
              모험을 떠나요!
              <svg class="absolute -bottom-2 left-0 w-full h-3 text-orange-300" viewBox="0 0 100 10" preserveAspectRatio="none"><path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="4" fill="none"/></svg>
            </span>
          </h1>
          
          <p class="text-lg text-gray-500 font-medium leading-relaxed max-w-md mx-auto md:mx-0 font-jua opacity-80">
            동물 친구들이 숨겨놓은 보물 같은 빵집을 찾아보세요.<br>
            당신의 취향을 저격할 갓 구운 빵이 기다리고 있어요. 🥐
          </p>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start pt-4 font-jua">
            <button @click="$router.push('/map')" class="group px-8 py-4 bg-[#FF9F43] text-white text-xl rounded-2xl shadow-[0_6px_0_#E67E22] hover:translate-y-1 hover:shadow-[0_3px_0_#E67E22] active:translate-y-2 active:shadow-none transition-all flex items-center justify-center gap-2">
              <span>지도 탐험하기</span>
              <span class="group-hover:rotate-12 transition-transform">🗺️</span>
            </button>
            <button class="px-8 py-4 bg-white border-2 border-[#FF9F43] text-[#FF9F43] text-xl rounded-2xl hover:bg-[#FF9F43]/10 transition-colors shadow-sm">
              내 취향 분석 🐻
            </button>
          </div>
        </div>

        <!-- 이미지 (메인 비주얼) -->
        <div class="md:w-1/2 relative w-full h-[400px] md:h-[600px] flex items-center justify-center">
          <div class="relative w-full h-full">
            <!-- 메인 이미지 프레임 -->
            <div class="absolute inset-4 bg-white p-3 rounded-[3rem] shadow-2xl rotate-3 z-10 transform transition-transform hover:rotate-0 duration-500">
              <img src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=800&auto=format&fit=crop" class="w-full h-full object-cover rounded-[2.5rem]">
            </div>
            <!-- 장식 요소들 (Floating) -->
            <div class="absolute -top-4 -right-4 bg-white p-4 rounded-2xl shadow-xl z-20 animate-float">
              <span class="text-4xl">🥯</span>
            </div>
            <div class="absolute bottom-10 -left-8 bg-white p-3 rounded-2xl shadow-xl z-20 animate-float delay-700 flex items-center gap-2">
              <span class="text-2xl">🦁</span>
              <div class="text-xs font-bold text-[#4A4036] font-jua">
                <p>사자왕의 원픽!</p>
                <p class="text-orange-500 text-sm">소금빵 맛집</p>
              </div>
            </div>
          </div>
        </div>

      </div>
      
      <!-- 스크롤 유도 -->
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 text-center animate-bounce opacity-60 font-jua text-[#4A4036]">
        <p class="text-sm mb-1">아래로 스크롤!</p>
        <ArrowDown class="w-5 h-5 text-orange-400 mx-auto" />
      </div>
    </section>

    <!-- 2. Weekly Curation: 숲속 오솔길 느낌 -->
    <section class="py-24 bg-white relative">
      <!-- 물결 모양 구분선 -->
      <div class="absolute top-0 left-0 w-full overflow-hidden leading-none rotate-180">
        <svg class="relative block w-[calc(100%+1.3px)] h-[50px]" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" fill="#FFFDF9"></path>
        </svg>
      </div>

      <div class="max-w-[1200px] mx-auto px-6">
        <div class="text-center mb-16">
          <span class="text-orange-500 tracking-widest text-sm bg-orange-50 px-3 py-1 rounded-full font-jua">Weekly Pick</span>
          <!-- 폰트 변경: font-serif -> font-jua -->
          <h2 class="text-3xl md:text-5xl font-jua text-[#4A4036] mt-3">
            이번 주 <span class="text-[#1D4E45] underline decoration-wavy decoration-orange-300">핫한 빵집</span> 모음
          </h2>
        </div>

        <BakeryGrid :bakeries="bakeries" @open-detail="openDetail" />
        
        <div class="text-center mt-12">
          <button class="inline-flex items-center gap-2 text-[#4A4036] text-lg font-jua hover:text-orange-500 transition-colors border-b-2 border-transparent hover:border-orange-500 pb-1">
            더 많은 빵집 보러가기 <ArrowRight class="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>

    <!-- 3. Featured Section: 쉐프 곰의 추천 (Breadtopia Concept) -->
    <section class="py-32 bg-[#E8F3E8] relative overflow-hidden">
        <!-- 배경 장식 -->
        <div class="absolute top-0 left-0 w-full h-full pointer-events-none opacity-40">
           <div class="absolute top-10 left-10 w-32 h-12 bg-white rounded-full blur-xl animate-float-slow"></div>
           <div class="absolute top-20 right-20 w-48 h-16 bg-white rounded-full blur-xl animate-float-slow" style="animation-delay: 2s;"></div>
        </div>

        <div class="max-w-[1200px] mx-auto px-6 relative z-10">
            <div class="flex flex-col md:flex-row items-center gap-16">
                
                <!-- 왼쪽: 쉐프 곰 이미지 -->
                <div class="md:w-1/2 w-full relative">
                    <div class="relative z-10 transform hover:scale-105 transition-transform duration-500 cursor-pointer">
                        <div class="absolute -inset-4 bg-[#FFD700]/20 rounded-full blur-2xl animate-pulse"></div>
                        <img src="https://images.unsplash.com/photo-1579619626372-9694d209e99a?q=80&w=800&auto=format&fit=crop" class="relative rounded-[2rem] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] border-8 border-white w-full object-cover h-[400px]">
                        
                        <!-- 말풍선 -->
                        <div class="absolute -top-6 -right-6 bg-white p-4 rounded-2xl rounded-bl-none shadow-lg animate-bounce-slow">
                            <span class="text-2xl">🐻‍❄️</span>
                            <span class="text-base text-[#4A4036] ml-2 font-jua">"이달의 추천 빵집이야!"</span>
                        </div>
                    </div>
                </div>

                <!-- 오른쪽: 텍스트 -->
                <div class="md:w-1/2 w-full space-y-6 text-center md:text-left">
                    <span class="inline-block px-3 py-1 bg-white/60 text-[#2C5F2D] rounded-full text-sm font-jua border border-[#2C5F2D]/20">Level Up Challenge</span>
                    <!-- 폰트 변경: font-serif -> font-jua -->
                    <h2 class="text-4xl md:text-6xl font-jua text-[#2C5F2D] leading-tight">
                        동물 친구들과 함께 <br>
                        성장해볼까요?
                    </h2>
                    <p class="text-gray-600 text-xl leading-relaxed font-jua opacity-80">
                        빵을 먹을수록 <strong>'아기 햄스터'</strong>에서 <br>
                        <strong>'전설의 사자왕'</strong>으로 진화합니다! 🦁<br>
                        숨겨진 히든 맵을 잠금 해제하세요.
                    </p>
                    
                    <button class="px-8 py-4 bg-[#2C5F2D] text-white text-xl rounded-2xl font-jua hover:bg-[#1D4E45] transition-all shadow-lg hover:shadow-xl w-full md:w-auto flex items-center justify-center gap-2 mx-auto md:mx-0">
                        내 캐릭터 확인하러 가기 <ArrowRight class="w-5 h-5" />
                    </button>
                </div>
            </div>
        </div>
    </section>

  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BakeryGrid from '@/components/common/BakeryGrid.vue'
import { ArrowRight, ArrowDown, ArrowUpRight } from 'lucide-vue-next'

const router = useRouter()

// 더미 데이터 (실제로는 API 연동)
const bakeries = ref([
  {
    id: 1,
    bakeryName: "버터하우스",
    name: "클래식 소금빵",
    location: "부산 전포동",
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&q=80&w=800",
    tags: ["버터가득", "겉바속촉"],
    menu: [{ name: "소금빵", price: "3,500", img: "" }]
  },
  {
    id: 2,
    bakeryName: "무슈 크루아상",
    name: "말차 크루아상",
    location: "서울 성수동",
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1530610476181-d8ceb28bc272?auto=format&fit=crop&q=80&w=800",
    tags: ["결이살아있는", "프랑스밀가루"],
    menu: []
  },
  {
    id: 3,
    bakeryName: "선데이 베이글",
    name: "블루베리 샌드",
    location: "서울 연남동",
    rating: 4.5,
    image: "https://images.unsplash.com/photo-1620916297397-a4a5402a3c6c?auto=format&fit=crop&q=80&w=800",
    tags: ["런던스타일", "크림치즈"],
    menu: []
  },
  {
    id: 4,
    bakeryName: "건강한 통밀",
    name: "사워도우",
    location: "제주 애월읍",
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=800",
    tags: ["비건", "건강식"],
    menu: []
  }
])

const openDetail = (bakery) => {
  router.push(`/detail/${bakery.id}`)
}
</script>

<style scoped>
/* 구글 폰트 (Jua) 불러오기 */
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

/* .font-jua 클래스 정의 */
.font-jua {
  font-family: 'Jua', sans-serif;
}

/* 부드러운 애니메이션 */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-float {
  animation: float 4s ease-in-out infinite;
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.05); }
}
.animate-pulse-slow {
  animation: pulse-slow 6s ease-in-out infinite;
}

/* 스크롤 바 숨기기 */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>