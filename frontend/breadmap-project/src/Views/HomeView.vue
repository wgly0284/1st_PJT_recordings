<template>
  <main class="flex-grow bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] overflow-hidden">
    <!-- 1. Hero Section -->
    <section class="relative min-h-screen flex flex-col justify-center items-center pt-24 pb-24">
      <!-- 수채화 배경 얼룩 (위치와 투명도 미세 조정) -->
      <div
        class="absolute top-0 right-0 w-[600px] h-[600px]
               bg-[#F3B37A]/15 rounded-full blur-3xl -z-10 translate-x-1/3 -translate-y-1/4"
      ></div>
      <div
        class="absolute bottom-0 left-0 w-[500px] h-[500px]
               bg-[#9AC89A]/15 rounded-full blur-3xl -z-10 -translate-x-1/3 translate-y-1/4"
      ></div>

      <!-- 메인 컨텐츠 영역 (수직 정렬로 변경) -->
      <div class="max-w-[1000px] mx-auto px-6 w-full flex flex-col items-center gap-8 relative z-10 text-center">
        
        <!-- 1. 이미지 (중앙 배치 & 배경과 자연스럽게) -->
        <div class="relative w-full max-w-lg aspect-square sm:aspect-[4/3] flex items-center justify-center -mb-8 sm:-mb-12">
          <!-- 뒤쪽 은은한 광채 효과 -->
          <div class="absolute inset-10 bg-gradient-to-tr from-orange-100/60 to-yellow-100/60 rounded-full blur-[60px]"></div>
          
          <!-- 메인 이미지 -->
          <img
            :src="mainImage"
            class="relative w-full h-full object-contain drop-shadow-lg hover:scale-105 transition-transform duration-700 z-10"
            alt="Breadtopia Main"
          />

          <!-- 장식 스티커 (위치 재조정) -->
          <div
            class="absolute top-[10%] right-[5%] bg-white/90 px-4 py-2 rounded-2xl
                   shadow-[0_4px_12px_rgba(0,0,0,0.05)] rotate-12 animate-pulse
                   flex items-center gap-2 z-20"
          >
            <span class="text-2xl">🐶</span>
            <span class="text-xs font-jua text-[#6B4A38] text-left">
              바게트코기의<br />최애 빵집
            </span>
          </div>

          <div
            class="absolute bottom-[15%] left-[5%] bg-white/90 px-4 py-2 rounded-2xl
                   shadow-[0_4px_12px_rgba(0,0,0,0.05)] -rotate-6
                   flex items-center gap-2 z-20"
          >
            <span class="text-2xl">🐻</span>
            <div class="text-xs font-jua text-[#6B4A38] text-left">
              <p>곰 셰프 추천</p>
              <p class="text-[#C99768]">소금빵 맛집</p>
            </div>
          </div>
        </div>

        <!-- 2. 텍스트 (이미지 아래로 이동) -->
        <div class="space-y-6 flex flex-col items-center relative z-20">
          <div
            class="inline-flex items-center gap-2 bg-white/60 backdrop-blur-sm border border-[#F3B37A]/30
                   px-5 py-2 rounded-full shadow-sm"
          >
            <span class="text-xl">🥐</span>
            <span class="text-sm font-bold text-[#C99768] tracking-wide font-jua">
              포근한 빵 바구니, Breadtopia
            </span>
          </div>

          <h1 class="text-5xl md:text-7xl font-jua text-[#6B4A38] leading-tight drop-shadow-sm">
            몽글몽글한
            <span class="inline-block text-[#C99768] relative px-2">
              빵지순례
              <svg class="absolute -bottom-2 left-0 w-full h-3 text-[#F3B37A]/40" viewBox="0 0 100 10" preserveAspectRatio="none">
                <path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="8" fill="none" />
              </svg>
            </span>
            를<br class="hidden md:block" /> 떠나요
          </h1>

          <p
            class="text-lg md:text-xl text-[#8B6A55] font-jua leading-relaxed
                   max-w-lg opacity-90"
          >
            바구니 속 강아지 빵처럼, 동글동글 귀여운 빵집들을
            <br />
            지도 위에서 하나씩 찾아보세요. 🐶🍞
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
        <div class="w-full max-w-xl mt-8 relative z-30">
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

    <!-- 2. 어디로 갈까요? 지역 선택 -->
    <section id="content-start" class="py-20 bg-white relative overflow-hidden">
      <!-- 배경 장식 -->
      <div class="absolute top-10 right-10 w-64 h-64 bg-orange-100 rounded-full opacity-20 blur-3xl"></div>
      <div class="absolute bottom-10 left-10 w-72 h-72 bg-teal-100 rounded-full opacity-20 blur-3xl"></div>

      <div class="max-w-6xl mx-auto px-6 relative z-10">
        <div class="text-center mb-12">
          <h2 class="text-3xl md:text-4xl font-bold text-[#1D4E45] mb-3 font-jua">
            어디로 갈까요? 🗺️
          </h2>
          <p class="text-gray-600">지역을 선택하면 근처 빵집을 추천해드려요</p>
        </div>

        <!-- 지역 그리드 -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <button
            v-for="region in regions"
            :key="region.id"
            @click="goToRegion(region.id)"
            class="group relative bg-gradient-to-br from-white to-orange-50 p-8 rounded-3xl border-2 border-orange-100 hover:border-orange-400 hover:shadow-2xl hover:-translate-y-3 transition-all duration-300"
          >
            <!-- 발자국/빵 아이콘 -->
            <div class="text-6xl mb-4 group-hover:scale-110 transition-transform duration-300">
              {{ region.icon }}
            </div>
            <h3 class="text-xl font-bold text-[#1D4E45] group-hover:text-orange-600 transition-colors font-jua">
              {{ region.name }}
            </h3>
            <p class="text-sm text-gray-500 mt-1">{{ region.count }}개의 빵집</p>

            <!-- 호버 화살표 -->
            <div class="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
              <ArrowRight class="w-5 h-5 text-orange-500" />
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
            class="inline-flex items-center gap-1 text-[#C99768] tracking-widest text-sm
                   bg-[#FFF3DD] px-4 py-1 rounded-full font-jua"
          >
            <span>🍞</span>
            <span>Weekly Pick</span>
          </span>

          <h2 class="text-3xl md:text-5xl font-jua text-[#6B4A38] mt-4">
            이번 주
            <span class="text-[#C99768] underline decoration-wavy decoration-[#F3B37A]">
              빵지순례 코스
            </span>
            모음
          </h2>
          <p class="mt-3 text-[#8B6A55] font-jua">
            바구니에 쏙 담고 싶은 따뜻한 동네 빵집들을 모았어요. 🧺
          </p>
        </div>

        <BakeryGrid :bakeries="bakeries" @open-detail="openDetail" />

        <div class="text-center mt-24">
          <button
            class="inline-flex items-center gap-2 text-[#6B4A38] text-lg font-jua
                   hover:text-[#C99768] transition-colors border-b-2 border-transparent
                   hover:border-[#C99768] pb-1"
          >
            더 많은 빵집 보러가기
            <ArrowRight class="w-5 h-5" />
          </button>
        </div>
      </div>
    </section>

    <!-- 3. Featured Section -->
    <section class="py-32 bg-[#E6F4D7]/90 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-full pointer-events-none opacity-40">
        <div class="absolute top-10 left-10 w-32 h-12 bg-white/70 rounded-full blur-xl"></div>
        <div class="absolute top-24 right-16 w-40 h-16 bg-white/70 rounded-full blur-xl"></div>
      </div>

      <div class="max-w-[1200px] mx-auto px-6 relative z-10">
        <div class="flex flex-col md:flex-row items-center gap-16">
          <!-- 이미지 -->
          <div class="md:w-1/2 w-full relative">
            <div
              class="relative z-10 transform hover:scale-105 transition-transform duration-500 cursor-pointer"
            >
              <div
                class="absolute -inset-4 bg-[#F3B37A]/26 rounded-[2.5rem] blur-2xl"
              ></div>
              <img
                src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?q=80&w=900&auto=format&fit=crop"
                class="relative rounded-[2rem]
                       shadow-[0_20px_50px_-12px_rgba(201,151,104,0.35)]
                       border-8 border-[#FFF3DD] w-full object-cover h-[380px]"
                alt="featured bakery"
              />

              <div
                class="absolute -top-6 -right-4 bg-white/95 px-4 py-3 rounded-2xl rounded-bl-none
                       shadow-[0_10px_20px_rgba(0,0,0,0.06)]
                       flex items-center gap-2"
              >
                <span class="text-2xl">🐻</span>
                <span class="text-base text-[#6B4A38] font-jua">
                  이달의 추천 빵집이에요!
                </span>
              </div>
            </div>
          </div>

          <!-- 텍스트 -->
          <div class="md:w-1/2 w-full space-y-6 text-center md:text-left">
            <span
              class="inline-block px-4 py-1 bg-[#FFF3DD]/80 text-[#8B6A55]
                     rounded-full text-sm font-jua border border-[#C99768]/30"
            >
              Level Up Challenge
            </span>

            <h2 class="text-4xl md:text-5xl font-jua text-[#6B4A38] leading-tight">
              빵을 먹을수록
              <br />
              나만의 빵 캐릭터도 성장해요
            </h2>

            <p class="text-[#8B6A55] text-xl leading-relaxed font-jua opacity-90">
              첫 방문은 작고 귀여운 <strong>모닝빵</strong>이지만,
              <br />
              여러 빵집을 기록하다 보면
              <strong>든든한 식빵 히어로</strong>가 되어 있어요. 🍞
            </p>

            <button
              class="px-8 py-4 bg-[#C99768] text-white text-xl rounded-3xl
                     font-jua hover:bg-[#A6744C] transition-all
                     shadow-[0_10px_22px_rgba(201,151,104,0.5)]
                     hover:shadow-[0_6px_16px_rgba(201,151,104,0.35)]
                     w-full md:w-auto flex items-center justify-center gap-2 mx-auto md:mx-0"
            >
              내 캐릭터 확인하러 가기
              <ArrowRight class="w-5 h-5" />
            </button>
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
import { ArrowRight, ArrowDown, PawPrint, Search } from 'lucide-vue-next'
import axios from 'axios'

// Assets Import (확장자 .png 사용)
import mainImage from '@/assets/images/메인화면.png'

const router = useRouter()
const searchQuery = ref('')
const bakeries = ref([])

// 지역 데이터
const regions = ref([
  { id: 'gangnam', name: '강남', icon: '🥖', count: '12+' },
  { id: 'apgujeong', name: '압구정', icon: '🥐', count: '8+' },
  { id: 'seongsu', name: '성수', icon: '🍞', count: '15+' },
  { id: 'itaewon', name: '이태원', icon: '🥯', count: '10+' },
  { id: 'hongdae', name: '홍대', icon: '🥨', count: '20+' },
  { id: 'jamsil', name: '잠실', icon: '🧁', count: '9+' },
  { id: 'gangbuk', name: '강북', icon: '🍰', count: '6+' },
  { id: 'yeonnam', name: '연남', icon: '🎂', count: '11+' }
])

// 실제 데이터 로드 (Weekly Pick용)
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
  router.push({ name: 'map', query: { store_id: bakery.id } })
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
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}
</style>