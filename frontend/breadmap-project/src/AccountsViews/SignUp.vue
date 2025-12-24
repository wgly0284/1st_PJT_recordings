<template>
  <!-- pt-32로 상단 여백을 늘려 헤더와 겹치지 않게 수정 -->
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] flex items-center justify-center p-4 pt-32 pb-10">
    <div class="w-full max-w-5xl bg-white rounded-[2.5rem] shadow-2xl border-8 border-white overflow-hidden flex flex-col md:flex-row transition-all duration-500 ease-in-out min-h-[600px] relative">
      
      <!-- 귀여운 코기 장식 -->
      <img :src="BaguetteCorgi" alt="바게트 코기" class="absolute top-6 right-6 w-24 opacity-90 z-20 animate-wiggle origin-bottom">

      <!-- Image Section (Step 1 전용) -->
      <div v-if="step === 1" class="w-full md:w-5/12 hidden md:flex items-center justify-center p-8 bg-[#FFF3DD] relative overflow-hidden">
        <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>
        <img src="@/assets/images/메인화면.png" alt="Bakery" class="max-w-full h-auto object-contain drop-shadow-xl relative z-10 hover:rotate-3 transition-transform duration-500" style="max-height: 350px;">
      </div>

      <!-- Form Section -->
      <div :class="['p-8 md:p-12 flex flex-col relative transition-all duration-500 bg-white', step === 1 ? 'w-full md:w-7/12' : 'w-full']">
        
        <!-- Step 1: User Info -->
        <div v-if="step === 1" class="flex flex-col justify-center h-full">
          <div class="mb-8">
            <span class="text-[#EF6C00] font-jua text-lg bg-[#FFF3DD] px-3 py-1 rounded-lg">STEP 1</span>
            <h1 class="text-4xl md:text-5xl font-bold text-[#6B4A38] font-jua mt-3 mb-2">환영합니다! 🎉</h1>
            <p class="text-[#8B6A55] font-jua text-lg">빵순이 빵돌이들의 천국에 오신 걸 환영해요.<br>AI 빵 소믈리에가 당신을 기다립니다.</p>
          </div>
          
          <form @submit.prevent="nextStep" class="space-y-4 max-w-md">
            <div>
              <label class="block text-[#6B4A38] font-jua mb-1 ml-1">이메일</label>
              <input type="email" v-model="form.email" placeholder="email@example.com" required 
                class="w-full px-5 py-3.5 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] font-jua text-[#6B4A38] placeholder-[#C99768]/60 focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all">
            </div>
            <div>
              <label class="block text-[#6B4A38] font-jua mb-1 ml-1">닉네임</label>
              <input type="text" v-model="form.nickname" placeholder="빵 굽는 곰돌이" required 
                class="w-full px-5 py-3.5 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] font-jua text-[#6B4A38] placeholder-[#C99768]/60 focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all">
            </div>
            <div>
              <label class="block text-[#6B4A38] font-jua mb-1 ml-1">비밀번호</label>
              <input type="password" v-model="form.password1" placeholder="••••••••" required 
                class="w-full px-5 py-3.5 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] font-jua text-[#6B4A38] placeholder-[#C99768]/60 focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all">
            </div>
            <div>
              <label class="block text-[#6B4A38] font-jua mb-1 ml-1">비밀번호 확인</label>
              <input type="password" v-model="form.password2" placeholder="••••••••" required 
                class="w-full px-5 py-3.5 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] font-jua text-[#6B4A38] placeholder-[#C99768]/60 focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all">
            </div>
            
            <button type="submit" class="w-full py-4 mt-4 font-jua text-xl text-white transition-all duration-300 transform rounded-2xl bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] hover:shadow-lg hover:-translate-y-1 active:scale-95 shadow-md">
              다음 단계로 🥐
            </button>
          </form>

          <div class="mt-6 text-center font-jua text-[#8B6A55]">
            <p>이미 계정이 있으신가요? <router-link to="/login" class="text-[#EF6C00] hover:underline">로그인 하러가기</router-link></p>
          </div>
        </div>

        <!-- Step 2: Bread Preferences -->
        <div v-if="step === 2" class="h-full flex flex-col">
          <div class="flex-none mb-6 text-center md:text-left">
            <div class="flex items-center gap-3 mb-2">
              <span class="text-[#EF6C00] font-jua text-lg bg-[#FFF3DD] px-3 py-1 rounded-lg">STEP 2/2</span>
              <span class="h-px bg-[#FFE8CC] flex-1"></span>
            </div>
            <h1 class="text-3xl md:text-4xl font-bold text-[#6B4A38] font-jua leading-tight">
              <span class="text-[#EF6C00]">{{ form.nickname || 'USER' }}</span>님의<br>
              빵 취향 DNA 분석 🧬
            </h1>
            <p class="text-[#8B6A55] font-jua mt-2 text-lg">자세히 알려주실수록 인생 빵집을 찾아드려요!</p>
          </div>
          
          <!-- Scrollable Area -->
          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar pb-6">
            
            <div v-for="(category, index) in preferenceCategories" :key="index" class="mb-8">
              <h3 class="text-xl font-bold text-[#6B4A38] mb-4 flex items-center gap-2 font-jua bg-[#F9F7F2] p-3 rounded-xl inline-block">
                <component :is="category.icon" class="w-5 h-5 text-[#EF6C00]" /> {{ category.title }}
              </h3>
              
              <!-- 카드형 그리드 -->
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <button v-for="opt in category.options" :key="opt.name" 
                        @click="togglePreference(opt.name)"
                        :class="['relative p-3 border-2 rounded-2xl flex flex-col items-center justify-center transition-all duration-300 aspect-[4/3] group', 
                                  form.bread_preferences.includes(opt.name) 
                                  ? 'bg-[#EF6C00] border-[#EF6C00] text-white shadow-lg transform -translate-y-1' 
                                  : 'bg-white border-[#FFE8CC] text-[#8B6A55] hover:border-[#F3B37A] hover:bg-[#FFF9F0] hover:shadow-md']">
                  <!-- 체크 아이콘 (선택 시 표시) -->
                  <div v-if="form.bread_preferences.includes(opt.name)" class="absolute top-2 right-2 w-5 h-5 bg-white text-[#EF6C00] rounded-full flex items-center justify-center text-xs font-bold shadow-sm">✓</div>
                  
                  <span class="text-3xl mb-2 filter drop-shadow-sm group-hover:scale-110 transition-transform">{{ opt.emoji }}</span>
                  <span class="text-sm font-bold font-jua whitespace-nowrap">{{ opt.name }}</span>
                </button>
              </div>
            </div>

          </div>

          <!-- 하단 버튼 영역 -->
          <div class="flex-none flex gap-4 mt-4 pt-6 border-t-2 border-[#FFE8CC] bg-white">
            <button @click="step = 1" class="w-1/4 py-4 font-jua text-lg text-[#8B6A55] bg-[#FFF3DD] rounded-2xl hover:bg-[#FFE8CC] transition-colors">
              이전으로
            </button>
            <button @click="handleSignup" class="w-3/4 py-4 font-jua text-xl text-white transition-all duration-300 transform rounded-2xl bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] hover:shadow-lg hover:-translate-y-1 active:scale-95 shadow-md flex items-center justify-center gap-2">
              <span>빵지순례 시작하기</span>
              <span class="animate-bounce">🚀</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router';
import { Smile, Coffee, Utensils } from 'lucide-vue-next';
import BaguetteCorgi from '@/assets/images/바게트코기.png';

const step = ref(1);
const form = reactive({
  email: '',
  nickname: '',
  password1: '', 
  password2: '',
  bread_preferences: [],
});

const preferenceCategories = ref([
  {
    title: '선호하는 식감',
    icon: Smile,
    options: [
      { name: '쫄깃한', emoji: '🥯' },
      { name: '부드러운', emoji: '🍞' },
      { name: '바삭한', emoji: '🥖' },
      { name: '꾸덕한', emoji: '🍫' },
      { name: '결이살아있는', emoji: '🥐' },
      { name: '포슬포슬', emoji: '🧁' },
    ]
  },
  {
    title: '선호하는 맛',
    icon: Coffee,
    options: [
      { name: '담백/슴슴', emoji: '🌾' },
      { name: '고소한', emoji: '🥜' },
      { name: '달콤한', emoji: '🍯' },
      { name: '짭짤한', emoji: '🧂' },
      { name: '상큼한', emoji: '🍋' },
      { name: '매콤/자극', emoji: '🌶️' },
    ]
  },
  {
    title: '선호하는 종류',
    icon: Utensils,
    options: [
      { name: '하드계열', emoji: '🥖' },
      { name: '식사빵', emoji: '🥪' },
      { name: '구움과자', emoji: '🍪' },
      { name: '케이크', emoji: '🍰' },
      { name: '조리빵', emoji: '🌭' },
      { name: '비건/건강', emoji: '🥗' },
    ]
  }
]);

const authStore = useAuthStore();

const nextStep = () => {
  if (form.password1 !== form.password2) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }
  if (form.email && form.nickname && form.password1) {
    step.value = 2;
  } else {
    alert('모든 필드를 입력해주세요.');
  }
};

const togglePreference = (prefName) => {
  const index = form.bread_preferences.indexOf(prefName);
  if (index > -1) {
    form.bread_preferences.splice(index, 1);
  } else {
    form.bread_preferences.push(prefName);
  }
};

const handleSignup = () => {
  if (form.bread_preferences.length < 3) {
    if(!confirm('취향을 3개 이상 선택하면 더 정확한 추천이 가능해요! 그래도 진행할까요?')) return;
  }

  authStore.signup({
    email: form.email,
    nickname: form.nickname,
    password1: form.password1,
    password2: form.password2,
    bread_preferences: form.bread_preferences.join(','),
  });
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.font-jua {
  font-family: 'Jua', sans-serif;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #FFF9F0;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #FFE8CC;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #F3B37A;
}

@keyframes wiggle {
  0%, 100% { transform: rotate(-3deg); }
  50% { transform: rotate(3deg); }
}

.animate-wiggle {
  animation: wiggle 2s infinite ease-in-out;
}
</style>