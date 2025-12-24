<template>
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] py-10 overflow-hidden flex flex-col items-center justify-center">
    
    <!-- 타이틀 -->
    <div class="text-center mb-8 z-10 px-4">
      <div class="inline-flex items-center gap-2 bg-[#FFF3DD] border-2 border-[#FFE8CC] px-4 py-2 rounded-full shadow-sm mb-4">
        <span class="text-xl">🎲</span>
        <span class="text-[#C99768] font-jua">오늘의 빵 추천</span>
      </div>
      <h1 class="text-3xl md:text-5xl font-jua text-[#6B4A38] leading-tight break-keep">
        운명의 빵 다트! 🎯
      </h1>
      <p class="text-[#8B6A55] font-jua mt-2 text-base md:text-lg break-keep">
        오늘 뭐 먹지? 고민될 땐 돌려보세요!
      </p>
    </div>

    <!-- 룰렛 게임 컨테이너 -->
    <!-- 반응형 크기 조정: 모바일에서 화면 너비에 맞춤 -->
    <div class="relative w-[300px] h-[300px] sm:w-[400px] sm:h-[400px] md:w-[450px] md:h-[450px]">
      
      <!-- 1. 포인터 (화살표) -->
      <div class="absolute -top-5 left-1/2 -translate-x-1/2 z-20 w-10 h-14 md:w-12 md:h-16 drop-shadow-lg filter">
        <svg viewBox="0 0 24 24" fill="currentColor" class="text-[#EF6C00] w-full h-full">
          <path d="M12 22L2 2h20L12 22z" />
        </svg>
      </div>

      <!-- 2. 회전하는 룰렛 판 -->
      <div 
        class="w-full h-full rounded-full border-[8px] md:border-[12px] border-[#FFE8CC] shadow-2xl relative overflow-hidden bg-white transition-transform duration-[4000ms] cubic-bezier(0.25, 0.1, 0.25, 1)"
        :style="{ transform: `rotate(${currentRotation}deg)` }"
      >
        <!-- 룰렛 배경 (Conic Gradient로 분할) -->
        <div 
          class="absolute inset-0 w-full h-full rounded-full"
          :style="{ background: conicGradientStyle }"
        ></div>

        <!-- 룰렛 텍스트 아이템들 -->
        <!-- transform-origin을 bottom center로 명확히 지정 -->
        <div 
          v-for="(item, index) in breadList" 
          :key="index"
          class="absolute top-0 left-1/2 w-full h-1/2 flex justify-center pt-4 md:pt-8"
          :style="{ 
            transform: `translateX(-50%) rotate(${index * segmentAngle + segmentAngle / 2}deg)`,
            transformOrigin: '50% 100%' 
          }"
        >
          <div class="flex flex-col items-center gap-1">
            <span class="text-2xl md:text-3xl filter drop-shadow-sm">{{ item.icon }}</span>
            <!-- 텍스트 크기 조정 및 줄바꿈 방지 -->
            <span class="font-jua text-[#6B4A38] text-base md:text-xl font-bold drop-shadow-sm whitespace-nowrap">
              {{ item.name }}
            </span>
          </div>
        </div>
      </div>

      <!-- 3. 가운데 장식 (Start 버튼 겸용) -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-20">
        <button 
          @click="spinRoulette"
          :disabled="isSpinning"
          class="w-16 h-16 md:w-20 md:h-20 rounded-full bg-gradient-to-br from-[#F3B37A] to-[#EF6C00] border-4 border-white shadow-lg flex items-center justify-center font-jua text-xl md:text-2xl text-white hover:scale-105 active:scale-95 disabled:scale-100 disabled:opacity-80 transition-all"
        >
          {{ isSpinning ? '...' : 'GO!' }}
        </button>
      </div>
    </div>

    <!-- 결과 모달 (결과 나왔을 때 표시) -->
    <div v-if="result" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="closeResult"></div>
      
      <div class="bg-white rounded-[2rem] p-8 max-w-xs md:max-w-sm w-full relative z-10 text-center shadow-2xl animate-bounce-in border-4 border-[#FFE8CC]">
        <div class="text-5xl md:text-6xl mb-4 animate-pulse">{{ result.icon }}</div>
        <h2 class="text-xl md:text-2xl font-jua text-[#C99768] mb-2">오늘의 운명은...</h2>
        <h3 class="text-3xl md:text-4xl font-jua text-[#6B4A38] mb-6">{{ result.name }} 당첨!</h3>
        
        <p class="text-gray-500 font-jua mb-8 text-sm md:text-base break-keep">
          {{ getRandomMessage(result.name) }}
        </p>

        <div class="flex gap-3">
          <button 
            @click="closeResult"
            class="flex-1 py-3 bg-[#FFE8CC] text-[#8B6A55] rounded-xl font-jua text-base md:text-lg hover:bg-[#FFD180] transition-colors"
          >
            다시 돌리기
          </button>
          <button 
            @click="goToSearchWithKeyword(result.name)"
            class="flex-1 py-3 bg-[#EF6C00] text-white rounded-xl font-jua text-base md:text-lg hover:bg-[#E65100] transition-colors shadow-md"
          >
            가게 찾기 🥐
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 빵 리스트 데이터
const breadList = [
  { name: '소금빵', icon: '🧂' },
  { name: '크루아상', icon: '🥐' },
  { name: '단팥빵', icon: '🍘' },
  { name: '베이글', icon: '🥯' },
  { name: '식빵', icon: '🍞' },
  { name: '바게트', icon: '🥖' },
  { name: '케이크', icon: '🍰' },
  { name: '샌드위치', icon: '🥪' },
];

const isSpinning = ref(false);
const currentRotation = ref(0);
const result = ref(null);

// 각 조각의 각도 (360도 / 아이템 개수)
const segmentAngle = 360 / breadList.length;

// 배경 색상 (교차 패턴)
const conicGradientStyle = computed(() => {
  const colors = ['#FFF9F0', '#FFF3DD']; // 두 가지 색 교차
  let gradientStr = '';
  
  breadList.forEach((_, index) => {
    const start = index * segmentAngle;
    const end = (index + 1) * segmentAngle;
    const color = colors[index % colors.length];
    gradientStr += `${color} ${start}deg ${end}deg, `;
  });
  
  return `conic-gradient(${gradientStr.slice(0, -2)})`;
});

const spinRoulette = () => {
  if (isSpinning.value) return;
  
  isSpinning.value = true;
  result.value = null;

  // 최소 5바퀴(1800도) + 랜덤 각도(0~360)
  const randomDegree = Math.floor(Math.random() * 360);
  const totalSpins = 1800; // 5바퀴
  const targetRotation = currentRotation.value + totalSpins + randomDegree;
  
  currentRotation.value = targetRotation;

  // 회전 애니메이션 시간(4초) 후에 결과 계산
  setTimeout(() => {
    isSpinning.value = false;
    calculateResult(targetRotation);
  }, 4000); // CSS transition duration과 일치시켜야 함
};

const calculateResult = (finalAngle) => {
  // 실제 360도 내에서의 각도 (나머지 연산)
  const normalizedAngle = finalAngle % 360;
  
  // 포인터가 위쪽(0도/360도)에 있다고 가정.
  // 판이 시계방향으로 돌면, 실제 당첨된 아이템은 반시계 방향으로 계산됨.
  // 360 - normalizedAngle 은 포인터가 가리키는 판의 위치 각도
  const pointingAngle = (360 - normalizedAngle) % 360;
  
  // 인덱스 계산
  const winningIndex = Math.floor(pointingAngle / segmentAngle);
  
  result.value = breadList[winningIndex];
};

const closeResult = () => {
  result.value = null;
};

const goToSearchWithKeyword = (keyword) => {
  // 검색 페이지로 이동하면서 키워드 전달
  router.push({ path: '/search', query: { search: keyword } });
};

const getRandomMessage = (breadName) => {
  const messages = [
    `오늘은 ${breadName} 어떠세요? 입안 가득 행복이 퍼질 거예요!`,
    `지금 당장 ${breadName} 사러 달려가야 할 운명입니다!`,
    `${breadName} 한 입이면 스트레스가 확 풀릴 거예요.`,
    `커피와 함께 ${breadName}, 완벽한 조합이죠?`
  ];
  return messages[Math.floor(Math.random() * messages.length)];
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

/* 팝업 등장 애니메이션 */
@keyframes bounceIn {
  0% { transform: scale(0.3); opacity: 0; }
  50% { transform: scale(1.05); opacity: 1; }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

.animate-bounce-in {
  animation: bounceIn 0.5s cubic-bezier(0.215, 0.610, 0.355, 1.000) both;
}
</style>