<template>
  <div class="min-h-screen bg-cream-100 flex items-center justify-center p-4">
    <div class="w-full max-w-4xl bg-white rounded-2xl shadow-soft overflow-hidden flex flex-col md:flex-row">
      
      <!-- Image Section -->
      <div class="w-full md:w-1/2 flex items-center justify-center p-8 bg-cream-50">
        <img src="@/assets/images/메인화면.png" alt="A slice of toast" class="max-w-full h-auto object-contain" style="max-height: 400px;">
      </div>

      <!-- Form Section -->
      <div class="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center relative">
        <img :src="BaguetteCorgi" alt="바게트 코기" class="absolute top-4 right-4 w-20 opacity-80">
        
        <h1 class="text-4xl font-bold text-brown-text font-serif mb-2">다시 오셨군요!</h1>
        <p class="text-gray-600 mb-8">맛있는 빵집 정보를 확인하려면<br>로그인하세요.</p>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label for="email" class="text-sm font-medium text-brown-text">Email</label>
            <input 
              type="email" 
              v-model="email" 
              id="email" 
              required 
              class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800"
            >
          </div>
          <div>
            <label for="password" class="text-sm font-medium text-brown-text">Password</label>
            <input 
              type="password" 
              v-model="password" 
              id="password" 
              required 
              class="w-full px-4 py-2 mt-1 border rounded-lg bg-cream-50 border-cream-200 focus:ring-teal-800 focus:border-teal-800"
            >
          </div>
          <button 
            type="submit" 
            class="w-full py-3 font-semibold text-white transition-transform duration-200 transform rounded-lg bg-teal-800 hover:bg-teal-900 active:scale-95"
          >
            Sign In
          </button>
        </form>
        
        <div class="text-center mt-6 text-sm">
          <a href="#" class="text-gray-500 hover:underline">Forgot password?</a>
        </div>
        
        <div class="text-center mt-4 text-sm">
          <p class="text-gray-500">
            아직 계정이 없으신가요? 
            <router-link to="/signup" class="font-semibold text-teal-800 hover:underline">회원가입 하러가기</router-link>
          </p>
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
/* TailwindCSS is handling styling */
</style>