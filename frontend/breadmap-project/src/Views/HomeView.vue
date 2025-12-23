<template>
  <main class="flex-grow bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] overflow-hidden">
    <!-- 1. Hero Section -->
    <!-- flex-col과 justify-center를 사용하여 내용이 수직 중앙에 오도록 하고, pb-20으로 하단 여백 확보 -->
    <section class="relative min-h-screen flex flex-col justify-center items-center pt-20 pb-20">
      <!-- 수채화 배경 얼룩 -->
      <div
        class="absolute top-16 right-[-10%] w-[520px] h-[520px]
               bg-[#F3B37A]/22 rounded-[999px] blur-3xl -z-10"
      ></div>
      <div
        class="absolute bottom-[-12%] left-[-10%] w-[480px] h-[480px]
               bg-[#9AC89A]/20 rounded-[999px] blur-3xl -z-10"
      ></div>

      <!-- 메인 컨텐츠 영역 -->
      <div class="max-w-[1200px] mx-auto px-6 w-full flex flex-col md:flex-row items-center gap-12 mb-12">
        <!-- 텍스트 -->
        <div class="md:w-1/2 space-y-6 relative z-10 text-center md:text-left">
          <div
            class="inline-flex items-center gap-2 bg-white/85 border border-[#F3B37A]/40
                   px-4 py-2 rounded-full shadow-[0_4px_10px_rgba(0,0,0,0.04)]"
          >
            <span class="text-xl">🥐</span>
            <span class="text-sm font-bold text-[#C99768] tracking-wide font-jua">
              포근한 빵 바구니, Breadtopia
            </span>
          </div>

          <h1 class="text-5xl md:text-6xl font-jua text-[#6B4A38] leading-tight">
            몽글몽글한
            <br />
            <span class="inline-block text-[#C99768] relative">
              빵지순례를 떠나요
              <span
                class="absolute -bottom-1 left-0 w-full h-[6px]
                       bg-[#F3B37A]/45 rounded-full"
              ></span>
            </span>
          </h1>

          <p
            class="text-lg text-[#8B6A55] font-jua leading-relaxed
                   max-w-md mx-auto md:mx-0 opacity-90"
          >
            바구니 속 강아지 빵처럼, 동글동글 귀여운 빵집들을
            <br />
            지도 위에서 하나씩 찾아보세요. 🐶🍞
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center md:justify-start pt-4 font-jua">
            <button
              @click="$router.push('/map')"
              class="group px-8 py-4 bg-[#F3B37A] text-white text-xl
                     rounded-3xl shadow-[0_6px_14px_rgba(201,151,104,0.45)]
                     hover:bg-[#C99768] hover:shadow-[0_4px_10px_rgba(201,151,104,0.3)]
                     active:translate-y-[2px]
                     transition-all flex items-center justify-center gap-2"
            >
              <span>빵 지도 열기</span>
              <span class="group-hover:rotate-6 transition-transform">🗺️</span>
            </button>

            <button
              class="px-8 py-4 bg-white/90 border border-[#F3B37A]/50
                     text-[#C99768] text-xl rounded-3xl
                     hover:bg-[#FFF3DD] transition-colors
                     shadow-[0_3px_8px_rgba(0,0,0,0.03)]"
            >
              내 빵 취향 보기
            </button>
          </div>
        </div>

        <!-- 이미지 -->
        <div class="md:w-1/2 relative w-full h-[400px] md:h-[540px] flex items-center justify-center">
          <div class="relative w-full h-full">
            <div
              class="absolute inset-4 bg-[#FFF3DD] p-4 rounded-[3rem]
                     shadow-[0_16px_32px_rgba(201,151,104,0.25)]
                     transform rotate-1 transition-transform hover:rotate-0 duration-500"
            >
              <img
                src="https://images.unsplash.com/photo-1514996937319-344454492b37?q=80&w=900&auto=format&fit=crop"
                class="w-full h-full object-cover rounded-[2.5rem]"
                alt="bread basket"
              />
            </div>

            <div
              class="absolute -top-3 -right-2 bg-white/90 px-4 py-3 rounded-2xl
                     shadow-[0_6px_14px_rgba(0,0,0,0.05)]
                     flex items-center gap-2"
            >
              <span class="text-3xl">🐶</span>
              <span class="text-xs font-jua text-[#6B4A38]">
                바게트코기의<br />최애 빵집
              </span>
            </div>

            <div
              class="absolute bottom-6 -left-3 bg-white/90 px-3 py-3 rounded-2xl
                     shadow-[0_6px_14px_rgba(0,0,0,0.05)]
                     flex items-center gap-2"
            >
              <span class="text-3xl">🐻</span>
              <div class="text-xs font-jua text-[#6B4A38]">
                <p>곰 셰프 추천</p>
                <p class="text-[#C99768] text-sm">소금빵 맛집</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 둥글둥글 검색바 (위치 수정됨) -->
      <!-- absolute 제거 및 margin-top 추가로 겹침 방지 -->
      <div class="w-full max-w-xl px-6 relative z-20 mt-4 md:mt-8">
        <div class="bg-white p-2.5 rounded-full shadow-[0_8px_24px_rgba(201,151,104,0.35)] flex items-center gap-3 border-4 border-[#FFF3DD] hover:border-[#F3B37A]/50 transition-all duration-300">
          <div class="pl-5 text-[#C99768]">
            <!-- 돋보기 아이콘 교체 -->
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
            <!-- 동물 발바닥 아이콘 교체 -->
            <PawPrint class="w-7 h-7 fill-white/20 group-hover:rotate-12 transition-transform" />
          </button>
        </div>
      </div>

      <!-- 스크롤 유도 (위치 및 배치 방식 전면 수정) -->
      <!-- absolute를 제거하고, margin-top(mt-16)을 넉넉히 주어 검색바 아래에 겹치지 않게 배치 -->
      <!-- text-center와 mx-auto로 가로 중앙 정렬 보장 -->
      <div
        class="mt-16 text-center animate-bounce opacity-70 font-jua text-[#8B6A55] z-10"
      >
        <p class="text-sm mb-1">아래로 스크롤해서 빵집을 더 만나보세요</p>
        <ArrowDown class="w-5 h-5 text-[#C99768] mx-auto" />
      </div>
    </section>

    <!-- 2. 어디로 갈까요? 지역 선택 -->
    <section class="py-20 bg-white relative overflow-hidden">
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

        <!-- mt-12 -> mt-24로 변경하여 상단 여백 추가 -->
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