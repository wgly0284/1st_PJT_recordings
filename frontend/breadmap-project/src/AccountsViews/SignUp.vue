<template>
  <div class="min-h-screen bg-cream-100 flex items-center justify-center p-4">
    <div class="w-full max-w-4xl bg-white rounded-2xl shadow-soft overflow-hidden flex flex-col md:flex-row transition-all duration-500 ease-in-out">
      
      <!-- Image Section (only for Step 1) -->
      <div v-if="step === 1" class="w-full md:w-1/2 flex items-center justify-center p-8 bg-cream-50">
        <img src="@/assets/images/식빵.png" alt="A slice of toast" class="max-w-full h-auto object-contain" style="max-height: 400px;">
      </div>

      <!-- Form Section -->
      <!-- 📌 위치 조정: Step 1일 때는 절반(md:w-1/2), Step 2일 때는 전체(w-full) 사용 -->
      <div :class="['p-8 md:p-12 flex flex-col justify-center relative transition-all duration-500', step === 1 ? 'w-full md:w-1/2' : 'w-full']">
        <img :src="BaguetteCorgi" alt="바게트 코기" class="absolute top-4 right-4 w-20 opacity-80">
        
        <!-- Step 1: User Info -->
        <div v-if="step === 1">
          <p class="text-teal-800 font-semibold">STEP 1</p>
          <h1 class="text-4xl font-bold text-brown-text font-serif mb-2">환영합니다!</h1>
          <p class="text-gray-600 mb-8">지금 가입하고<br>AI 빵 소믈리에의 추천을 받아보세요.</p>
          
          <form @submit.prevent="nextStep" class="space-y-4">
            <input type="email" v-model="form.email" placeholder="Email" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="text" v-model="form.nickname" placeholder="Nickname" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="password" v-model="form.password1" placeholder="Password" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <input type="password" v-model="form.password2" placeholder="Confirm Password" required class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800">
            <button type="submit" class="w-full py-3 font-semibold text-white transition-transform duration-200 transform rounded-lg bg-teal-800 hover:bg-teal-900 active:scale-95">Next</button>
          </form>

          <div class="text-center mt-4 text-sm">
            <p class="text-gray-500">이미 계정이 있으신가요? <router-link to="/login" class="font-semibold text-teal-800 hover:underline">로그인 하러가기</router-link></p>
          </div>
        </div>

        <!-- Step 2: Bread Preferences (AI Data Collection) -->
        <div v-if="step === 2" class="h-full flex flex-col">
          <div class="flex-none mb-4 text-center md:text-left">
            <p class="text-teal-800 font-semibold">STEP 2/2</p>
            <h1 class="text-3xl font-bold text-brown-text font-serif mb-1">{{ form.nickname || 'USER' }}님의<br>빵 취향 DNA 분석 🧬</h1>
            <p class="text-sm text-gray-500">자세히 알려주실수록 더 맛있는 빵집을 찾아드려요!</p>
          </div>
          
          <!-- Scrollable Area for Preferences -->
          <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar">
            
            <div v-for="(category, index) in preferenceCategories" :key="index" class="mb-6">
              <h3 class="text-lg font-bold text-teal-900 mb-3 flex items-center gap-2">
                <component :is="category.icon" class="w-5 h-5" /> {{ category.title }}
              </h3>
              <!-- 📌 넓어진 공간에 맞춰 그리드 조정 (최대 6열) -->
              <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
                <button v-for="opt in category.options" :key="opt.name" 
                        @click="togglePreference(opt.name)"
                        :class="['p-2 border rounded-lg flex flex-col items-center justify-center transition-all aspect-[4/3] hover:shadow-sm', 
                                 form.bread_preferences.includes(opt.name) 
                                 ? 'bg-teal-800 text-white border-teal-800 shadow-md transform scale-105' 
                                 : 'bg-white border-cream-200 text-gray-600 hover:border-teal-600 hover:bg-cream-50']">
                  <span class="text-2xl mb-1">{{ opt.emoji }}</span>
                  <span class="text-xs font-bold whitespace-nowrap">{{ opt.name }}</span>
                </button>
              </div>
            </div>

          </div>

          <div class="flex-none flex gap-4 mt-6 pt-4 border-t border-cream-200">
            <button @click="step = 1" class="w-1/3 py-3 font-semibold text-gray-600 bg-gray-200 rounded-lg hover:bg-gray-300">Back</button>
            <button @click="handleSignup" class="w-2/3 py-3 font-semibold text-white transition-transform duration-200 transform rounded-lg bg-teal-800 hover:bg-teal-900 active:scale-95 shadow-lg">
              빵지순례 시작하기 🚀
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
import { Smile, Coffee, Utensils } from 'lucide-vue-next'; // 카테고리 아이콘용
import BaguetteCorgi from '@/assets/images/바게트코기.png';

const step = ref(1);
const form = reactive({
  email: '',
  nickname: '',
  password1: '', // 변수명 일치 (template과 script)
  password2: '',
  bread_preferences: [],
});

// 📌 AI 추천을 위한 상세 취향 카테고리
const preferenceCategories = ref([
  {
    title: '선호하는 식감',
    icon: Smile,
    options: [
      { name: '쫄깃한', emoji: '🥯' }, // 베이글, 치아바타
      { name: '부드러운', emoji: '🍞' }, // 식빵, 카스테라
      { name: '바삭한', emoji: '🥖' }, // 바게트, 크룽지
      { name: '꾸덕한', emoji: '🍫' }, // 브라우니, 테린느
      { name: '결이살아있는', emoji: '🥐' }, // 크루아상, 몽블랑
      { name: '포슬포슬', emoji: '🧁' }, // 스콘, 머핀
    ]
  },
  {
    title: '선호하는 맛',
    icon: Coffee,
    options: [
      { name: '담백/슴슴', emoji: '🌾' }, // 건강빵, 사워도우
      { name: '고소한', emoji: '🥜' }, // 견과류, 버터
      { name: '달콤한', emoji: '🍯' }, // 디저트, 크림
      { name: '짭짤한', emoji: '🧂' }, // 소금빵, 프레첼
      { name: '상큼한', emoji: '🍋' }, // 과일 타르트
      { name: '매콤/자극', emoji: '🌶️' }, // 소세지빵, 피자빵
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
  // 최소 3개 이상 선택 유도 (AI 정확도를 위해)
  if (form.bread_preferences.length < 3) {
    if(!confirm('취향을 3개 이상 선택하면 더 정확한 추천이 가능해요! 그래도 진행할까요?')) return;
  }

  authStore.signup({
    email: form.email,
    nickname: form.nickname,
    password1: form.password1,
    password2: form.password2,
    // 배열을 콤마로 구분된 문자열로 변환하여 저장
    bread_preferences: form.bread_preferences.join(','),
  });
};
</script>

<style scoped>
/* 커스텀 스크롤바 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #9ca3af;
}
</style>