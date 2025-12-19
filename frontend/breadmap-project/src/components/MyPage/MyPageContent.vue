
<template>
  <div class="bg-white rounded-[2.5rem] shadow-soft p-8 md:p-16 border border-gray-100" v-scroll>
    <div class="flex flex-col md:flex-row gap-12 items-center md:items-start">
      <!-- Profile Left -->
      <div class="md:w-1/3 flex flex-col items-center text-center">
        <div class="relative w-40 h-40 mb-6 group">
          <div class="absolute inset-0 bg-teal-800 rounded-full opacity-0 group-hover:opacity-10 transition-opacity"></div>
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg">
          <button class="absolute bottom-0 right-0 w-10 h-10 bg-teal-800 text-white rounded-full flex items-center justify-center border-4 border-white">
            <i data-lucide="camera" class="w-4 h-4"></i>
          </button>
        </div>
        <h2 class="text-3xl font-bold text-teal-900 mb-1">Bread Lover</h2>
        <p class="text-gray-400 mb-8">Seoul, Korea</p>
        <button class="w-full py-4 border-2 border-gray-100 rounded-2xl font-bold text-gray-600 hover:bg-teal-50 hover:border-teal-100 hover:text-teal-800 transition-colors">
          Edit Profile
        </button>
      </div>
      
      <!-- Stats Right -->
      <div class="flex-1 w-full space-y-10">
        <div class="bg-[#F9F7F2] p-8 rounded-[2rem]">
          <div class="flex justify-between items-end mb-4">
            <div>
              <p class="text-xs font-bold text-orange-600 uppercase tracking-widest mb-1">Current Level</p>
              <h3 class="text-3xl font-bold text-teal-900">Lv.3 빵수집가</h3>
            </div>
            <span class="text-4xl font-playfair italic text-gray-300">70%</span>
          </div>
          <div class="w-full bg-white rounded-full h-4 p-1">
            <div class="bg-teal-800 h-full rounded-full w-[70%] shadow-lg"></div>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <div class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all">
            <div class="text-3xl font-bold text-teal-900 mb-1">12</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Visits</div>
          </div>
          <div class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all">
            <div class="text-3xl font-bold text-teal-900 mb-1">45</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Reviews</div>
          </div>
          <div class="text-center p-4 border border-gray-100 rounded-2xl hover:border-teal-800/20 hover:bg-white hover:shadow-lg transition-all">
            <div class="text-3xl font-bold text-teal-900 mb-1">8</div>
            <div class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">Badges</div>
          </div>
        </div>

        <div>
          <h4 class="font-bold text-teal-900 mb-6 text-lg">Collection</h4>
          <div class="flex gap-4 overflow-x-auto pb-4">
            <div class="w-20 h-20 bg-orange-50 rounded-2xl flex items-center justify-center text-3xl border border-orange-100 shrink-0" title="리뷰 스타터">���</div>
            <div class="w-20 h-20 bg-teal-50 rounded-2xl flex items-center justify-center text-3xl border border-teal-100 shrink-0" title="소금빵 러버">���</div>
            <div class="w-20 h-20 border-2 border-dashed border-gray-200 rounded-2xl flex items-center justify-center text-gray-300 shrink-0">?</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 빈 script setup - 원본 그대로
</script>
