<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
    <BakeryCard
      v-for="bakery in bakeries"
      :key="bakery.id"
      :bakery="bakery"
      @click="openDetail(bakery)"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BakeryCard from './BakeryCard.vue'
import { useBakeryStore } from '@/stores/bakeries'

const bakeryStore = useBakeryStore()
const bakeries = ref([])

onMounted(async () => {
  bakeries.value = await bakeryStore.fetchBakeries()  // 비동기 API 호출
})

const emit = defineEmits(['openDetail'])
const openDetail = (bakery) => emit('openDetail', bakery)
</script>
