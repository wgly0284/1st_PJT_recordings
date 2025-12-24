<template>
  <!-- pt-32를 추가하여 상단 헤더와의 간격을 확보했습니다 -->
  <div class="min-h-screen bg-gradient-to-b from-[#FFF9F0] to-[#E6F4D7] flex items-center justify-center p-4 pt-32 pb-10">
    <div class="w-full max-w-4xl bg-white rounded-[3rem] shadow-xl border-8 border-white overflow-hidden flex flex-col md:flex-row relative">
      
      <!-- 장식용 코기 이미지 -->
      <img :src="BaguetteCorgi" alt="바게트 코기" class="absolute top-4 right-4 w-24 z-10 animate-bounce-slow">

      <!-- Image Section -->
      <div class="w-full md:w-1/2 flex items-center justify-center p-10 bg-[#FFF3DD] relative overflow-hidden">
        <!-- 배경 장식 -->
        <div class="absolute top-[-50px] left-[-50px] w-40 h-40 bg-[#FFE8CC] rounded-full blur-3xl"></div>
        <div class="absolute bottom-[-50px] right-[-50px] w-40 h-40 bg-[#F3B37A]/30 rounded-full blur-3xl"></div>
        
        <img src="@/assets/images/메인화면.png" alt="Bakery Main" class="max-w-full h-auto object-contain drop-shadow-lg relative z-10 transform hover:scale-105 transition-transform duration-500" style="max-height: 350px;">
      </div>

      <!-- Form Section -->
      <div class="w-full md:w-1/2 p-10 md:p-14 flex flex-col justify-center bg-white">
        
        <div class="mb-8">
          <span class="inline-block px-3 py-1 bg-[#FFF9F0] border border-[#FFE8CC] rounded-full text-[#C99768] font-jua text-sm mb-2">
            Welcome Back! 👋
          </span>
          <h1 class="text-4xl md:text-5xl font-bold text-[#6B4A38] font-jua mb-2">다시 오셨군요!</h1>
          <p class="text-[#8B6A55] font-jua text-lg">
            맛있는 빵 냄새가 기다리고 있어요.<br>로그인하고 빵지순례를 떠나보세요! 🥐
          </p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label for="email" class="block text-lg font-jua text-[#6B4A38] mb-1.5 ml-1">이메일</label>
            <input 
              type="email" 
              v-model="email" 
              id="email" 
              required 
              placeholder="example@bakery.com"
              class="w-full px-6 py-4 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] text-[#6B4A38] placeholder-[#C99768]/50 font-jua focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all shadow-sm"
            >
          </div>
          <div>
            <label for="password" class="block text-lg font-jua text-[#6B4A38] mb-1.5 ml-1">비밀번호</label>
            <input 
              type="password" 
              v-model="password" 
              id="password" 
              required 
              placeholder="••••••••"
              class="w-full px-6 py-4 rounded-2xl bg-[#F9F7F2] border-2 border-[#FFE8CC] text-[#6B4A38] placeholder-[#C99768]/50 font-jua focus:outline-none focus:border-[#F3B37A] focus:bg-white transition-all shadow-sm"
            >
          </div>
          
          <button 
            type="submit" 
            class="w-full py-4 mt-4 font-jua text-xl text-white transition-all duration-300 transform rounded-2xl bg-gradient-to-r from-[#F3B37A] to-[#EF6C00] hover:shadow-lg hover:-translate-y-1 active:scale-95 shadow-md flex items-center justify-center gap-2"
          >
            <span>로그인하기</span>
            <span>🔑</span>
          </button>
        </form>
        
        <div class="flex items-center justify-center gap-4 mt-8 font-jua text-[#8B6A55]">
          <a href="#" class="hover:text-[#EF6C00] transition-colors text-sm">비밀번호를 잊으셨나요?</a>
          <span class="text-gray-300">|</span>
          <router-link to="/signup" class="text-[#EF6C00] hover:text-[#E65100] hover:underline transition-colors text-lg">
            회원가입 하기
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { RouterLink } from 'vue-router';
import BaguetteCorgi from '@/assets/images/바게트코기.png';

const email = ref('');
const password = ref('');
const authStore = useAuthStore();

const handleLogin = () => {
  authStore.login({
    email: email.value,
    password: password.value,
  });
};
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
</style>