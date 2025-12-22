<template>
  <div class="bg-white rounded-[2.5rem] shadow-soft p-8 md:p-16 border border-gray-100">
    <div class="flex flex-col md:flex-row gap-12 items-center md:items-start">
      <!-- 프로필 왼쪽 -->
      <div class="md:w-1/2 flex flex-col items-center text-center">
        <div class="relative w-40 h-40 mb-6 group">
          <div class="absolute inset-0 bg-teal-800 rounded-full opacity-0 group-hover:opacity-10 transition-opacity"></div>
          
          <!-- 프로필 이미지 (미리보기 우선) -->
          <img
            v-if="localProfileImageUrl || authStore.currentUser?.profile_image_url"
            :src="localProfileImageUrl || `http://127.0.0.1:8000${authStore.currentUser.profile_image_url}`"
            class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg object-cover"
          />
          <div v-else class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg bg-gray-200 flex items-center justify-center text-5xl">
            🥖
          </div>

          
          <!-- 숨겨진 파일 입력 -->
          <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
          
          <!-- 카메라 버튼 -->
          <button
            type="button"
            @click="openFileDialog"
            class="absolute bottom-0 right-0 w-10 h-10 bg-teal-800 text-white rounded-full 
                   flex items-center justify-center border-4 border-white hover:bg-teal-700"
          >
            📷
          </button>
        </div>
        
        <h2 class="text-3xl font-bold text-teal-900 mb-1">
          {{ authStore.currentUser?.nickname || 'Guest' }}
        </h2>
        <p class="text-gray-400 mb-8">
          {{ authStore.currentUser?.email || 'Not logged in' }}
        </p>
        
        <!-- 👇 confirm 버튼: 실제 저장 API 호출 -->
        <button
          @click="saveProfile"
          :disabled="isSaving"
          class="w-full py-4 bg-teal-900 text-white font-bold rounded-2xl 
                 hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed
                 transition-all duration-200 flex items-center justify-center gap-2"
        >
          <span v-if="isSaving">저장 중...</span>
          <span v-else>confirm</span>
        </button>
      </div>
      
      <!-- 빵 선호도 -->
      <div class="flex-1 w-full space-y-10">
        <div class="bg-[#F9F7F2] p-8 rounded-[2rem]">
          <div class="flex justify-between items-center mb-4">
            <p class="text-xs font-bold text-orange-600 uppercase tracking-widest">My Bread Preferences</p>
            <button @click="showPreferencesModal = true" class="px-4 py-1 bg-teal-900 text-white text-xs font-bold rounded-full hover:bg-teal-800">
              수정하기
            </button>
          </div>
          <div v-if="currentPreferences.length" class="flex flex-wrap gap-2">
            <span v-for="pref in currentPreferences" :key="pref" class="px-3 py-1 bg-teal-800 text-white text-sm rounded-full">
              {{ pref }}
            </span>
          </div>
          <p v-else class="text-sm text-gray-500">선호하는 빵 종류가 없습니다.</p>
        </div>
      </div>
    </div>

    <!-- 빵 선호도 모달 (기존과 동일) -->
    <div v-if="showPreferencesModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <!-- 모달 내용 동일 -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'

const authStore = useAuthStore()
const fileInput = ref(null)
const showPreferencesModal = ref(false)
const selectedPreferences = ref([])
const localProfileImageUrl = ref(null)  // 👈 로컬 미리보기
const isSaving = ref(false)  // 👈 저장 중 상태

// 빵 선호도 옵션 (동일)
const breadPreferences = [/* 동일 */]

// 현재 선호도 (동일)
const currentPreferences = computed(() => {
  return authStore.currentUser?.bread_preferences?.split(',') || []
})

// 카메라 버튼
const openFileDialog = () => fileInput.value?.click()

// 이미지 업로드 (미리보기만)
const handleImageUpload = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  localProfileImageUrl.value = URL.createObjectURL(file)  // 👈 즉시 미리보기
}

// 👇 confirm 버튼: 실제 저장
const saveProfile = async () => {
  isSaving.value = true
  try {
    const file = fileInput.value?.files?.[0]
    if (file) {
      const formData = new FormData()
      formData.append('profile_image', file)

      const res = await apiClient.patch('/accounts/profile-image/', formData)
      const url = `http://127.0.0.1:8000${res.data.profile_image_url}`

      console.log('이미지 응답:', res.data)
      localProfileImageUrl.value = url
    }

    await authStore.fetchUser()
    alert('프로필이 저장되었습니다!')
  } catch (e) {
    console.error('저장 실패:', e.response?.status, e.response?.data)
    alert('저장 중 오류가 발생했습니다.')
  } finally {
    isSaving.value = false
  }
}



// 빵 선호도 저장 (동일)
const savePreferences = async () => {
  // 동일한 로직
}
</script>
