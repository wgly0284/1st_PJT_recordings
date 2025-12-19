<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
    <div v-for="(bakery, idx) in bakeries" :key="bakery.id" 
         @click="$emit('open-detail', bakery)"
         :class="{'lg:translate-y-16': idx % 2 !== 0}"
         class="group cursor-pointer">
      <div class="img-zoom-container rounded-[2rem] mb-6 shadow-soft relative aspect-[3/4]">
        <img :src="bakery.image" class="w-full h-full object-cover">
        <div class="absolute top-4 right-4 bg-white/90 backdrop-blur w-10 h-10 rounded-full flex items-center justify-center shadow-sm opacity-0 group-hover:opacity-100 transition-opacity duration-500 translate-y-2 group-hover:translate-y-0">
          <i data-lucide="arrow-up-right" class="w-5 h-5 text-teal-900"></i>
        </div>
        <div class="absolute bottom-4 left-4 flex gap-2">
          <span class="px-3 py-1 bg-white/90 backdrop-blur rounded-full text-xs font-bold text-teal-900">#{{ bakery.tags[0] }}</span>
        </div>
      </div>
      <div class="px-2">
        <div class="flex justify-between items-center mb-2">
          <h3 class="text-2xl font-playfair font-bold text-teal-900">{{ bakery.bakeryName }}</h3>
          <div class="flex items-center gap-1 text-orange-600 font-bold text-sm">
            <i data-lucide="star" class="w-3 h-3 fill-current"></i> {{ bakery.rating }}
          </div>
        </div>
        <p class="text-sm text-gray-500">{{ bakery.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['bakeries'])
defineEmits(['open-detail'])
</script>
