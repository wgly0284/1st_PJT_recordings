<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'

const route = useRoute()
const authStore = useAuthStore()
const userId = ref(route.params.userId)
const userInfo = ref(null)
const isLoading = ref(true)
const isFollowed = ref(false)
const isFollowing = ref(false)

// 레벨 설정
const LEVEL_CONFIG = {
  1: { name: '아기빵쥐', icon: '🐭', color: 'text-gray-400', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  2: { name: '식빵햄찌', icon: '🐹', color: 'text-orange-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235394.png' },
  3: { name: '호빵토끼', icon: '🐰', color: 'text-pink-300', img: 'https://cdn-icons-png.flaticon.com/512/235/235372.png' },
  4: { name: '모닝코기', icon: '🐶', color: 'text-yellow-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235415.png' },
  5: { name: '크루아상여우', icon: '🦊', color: 'text-orange-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235368.png' },
  6: { name: '브리오슈곰', icon: '🐻', color: 'text-brown-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235388.png' },
  7: { name: '사워도우울프', icon: '🐺', color: 'text-gray-600', img: 'https://cdn-icons-png.flaticon.com/512/235/235356.png' },
  8: { name: '초코표범', icon: '🐆', color: 'text-yellow-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235377.png' },
  9: { name: '바게트호크', icon: '🦅', color: 'text-teal-700', img: 'https://cdn-icons-png.flaticon.com/512/235/235386.png' },
  10: { name: '황금밀 유니콘', icon: '🦄', color: 'text-purple-500', img: 'https://cdn-icons-png.flaticon.com/512/235/235359.png' },
}

const currentLevelInfo = computed(() => {
  if (!userInfo.value) return LEVEL_CONFIG[1]
  return LEVEL_CONFIG[userInfo.value.level] || LEVEL_CONFIG[1]
})

const progressWidth = computed(() => {
  if (!userInfo.value) return '0%'
  const percent = (userInfo.value.exp / userInfo.value.next_exp) * 100
  return `${Math.min(percent, 100)}%`
})

const characterImages = {
  hamster: 'https://cdn-icons-png.flaticon.com/512/235/235394.png',
  bear: 'https://cdn-icons-png.flaticon.com/512/235/235388.png',
  lion: 'https://cdn-icons-png.flaticon.com/512/235/235352.png'
}

const getProfileImage = computed(() => {
  if (!userInfo.value) return LEVEL_CONFIG[1].img
  if (userInfo.value.profile_image_url) return userInfo.value.profile_image_url
  if (userInfo.value.character_type && characterImages[userInfo.value.character_type]) {
    return characterImages[userInfo.value.character_type]
  }
  return currentLevelInfo.value.img
})

const handleImageError = (event) => {
  event.target.src = currentLevelInfo.value.img
}

// 유저 프로필 가져오기
const fetchUserProfile = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/accounts/profile/${userId.value}/`, {
      headers: authStore.token ? { Authorization: `Token ${authStore.token}` } : {}
    })

    const data = response.data

    userInfo.value = {
      id: data.id,
      nickname: data.nickname || data.username,
      level: data.level || 1,
      level_title: LEVEL_CONFIG[data.level || 1].name,
      exp: data.exp || 0,
      next_exp: data.max_exp || 100,
      profile_image_url: data.profile_image_url ? `http://127.0.0.1:8000${data.profile_image_url}` : null,
      character_type: data.character_type || 'hamster',
      follower_count: data.follower_count || 0,
      following_count: data.following_count || 0,
      review_count: data.review_count || 0,
      post_count: data.post_count || 0,
      date_joined: data.date_joined || new Date().toISOString().split('T')[0]
    }
    isLoading.value = false
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    isLoading.value = false
  }
}

// 팔로우 상태 확인
const checkFollowStatus = async () => {
  if (!authStore.isAuthenticated) return
  try {
    const response = await apiClient.get('/accounts/following/')
    const followingIds = response.data.following?.map(u => u.id) || []
    isFollowed.value = followingIds.includes(Number(userId.value))
  } catch (error) {
    console.error('팔로우 상태 확인 실패:', error)
  }
}

// 팔로우/언팔로우 처리
const handleFollow = async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }
  if (isFollowing.value) return

  try {
    isFollowing.value = true
    const response = await apiClient.post(`/accounts/follow/${userId.value}/`)
    isFollowed.value = response.data.status === 'followed'

    // 팔로워 카운트 업데이트
    if (userInfo.value) {
      userInfo.value.follower_count += isFollowed.value ? 1 : -1
    }
  } catch (error) {
    console.error('팔로우 실패:', error)
    alert('팔로우 처리 중 오류가 발생했습니다.')
  } finally {
    isFollowing.value = false
  }
}

onMounted(async () => {
  await fetchUserProfile()
  await checkFollowStatus()
})
</script>

<template>
  <div class="max-w-[1000px] mx-auto px-6 py-20 pt-24">
    <div v-if="isLoading" class="flex justify-center items-center h-96">
      <div class="text-xl text-[#8D6E63]">로딩 중...</div>
    </div>

    <div v-else-if="userInfo" class="space-y-6">
      <!-- 프로필 헤더 -->
      <div class="bg-white rounded-3xl shadow-lg p-8 border-4 border-[#F3B37A]/20">
        <div class="flex flex-col md:flex-row items-center md:items-start gap-6">
          <!-- 프로필 이미지 -->
          <div class="relative">
            <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-[#F3B37A] shadow-lg">
              <img
                :src="getProfileImage"
                @error="handleImageError"
                alt="프로필"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="absolute -bottom-2 -right-2 bg-[#F3B37A] text-white px-3 py-1 rounded-full text-sm font-bold shadow-md">
              Lv.{{ userInfo.level }}
            </div>
          </div>

          <!-- 프로필 정보 -->
          <div class="flex-1 text-center md:text-left">
            <div class="flex flex-col md:flex-row items-center gap-3 mb-3">
              <h1 class="text-3xl font-bold text-[#5D4037]">{{ userInfo.nickname }}</h1>
              <span class="px-4 py-1 bg-gradient-to-r from-[#F3B37A] to-[#FF8A65] text-white rounded-full text-sm font-bold">
                {{ currentLevelInfo.icon }} {{ currentLevelInfo.level_title }}
              </span>
            </div>

            <!-- 경험치 바 -->
            <div class="mb-4">
              <div class="flex justify-between text-xs text-[#8D6E63] mb-1">
                <span>EXP</span>
                <span>{{ userInfo.exp }} / {{ userInfo.next_exp }}</span>
              </div>
              <div class="w-full bg-[#EFEBE9] rounded-full h-3 overflow-hidden">
                <div
                  class="h-full bg-gradient-to-r from-[#F3B37A] to-[#FF8A65] transition-all duration-500 rounded-full"
                  :style="{ width: progressWidth }"
                ></div>
              </div>
            </div>

            <!-- 통계 -->
            <div class="flex justify-center md:justify-start gap-6 mb-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-[#5D4037]">{{ userInfo.follower_count }}</div>
                <div class="text-xs text-[#8D6E63]">팔로워</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-[#5D4037]">{{ userInfo.following_count }}</div>
                <div class="text-xs text-[#8D6E63]">팔로잉</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-[#5D4037]">{{ userInfo.review_count }}</div>
                <div class="text-xs text-[#8D6E63]">리뷰</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-[#5D4037]">{{ userInfo.post_count }}</div>
                <div class="text-xs text-[#8D6E63]">게시글</div>
              </div>
            </div>

            <!-- 팔로우 버튼 (본인이 아닌 경우에만 표시) -->
            <button
              v-if="authStore.user?.pk !== userInfo.id"
              @click="handleFollow"
              :disabled="isFollowing"
              :class="[
                'px-6 py-2.5 rounded-full font-bold transition-all shadow-md',
                isFollowed
                  ? 'bg-[#EFEBE9] text-[#5D4037] hover:bg-[#D7CCC8]'
                  : 'bg-gradient-to-r from-[#F3B37A] to-[#FF8A65] text-white hover:shadow-lg',
                isFollowing ? 'opacity-50 cursor-not-allowed' : ''
              ]"
            >
              {{ isFollowing ? '처리 중...' : (isFollowed ? '팔로잉' : '팔로우 +') }}
            </button>
          </div>
        </div>
      </div>

      <!-- 추가 콘텐츠 영역 (리뷰, 게시글 등) -->
      <div class="bg-white rounded-3xl shadow-lg p-8 border-4 border-[#F3B37A]/20">
        <p class="text-center text-[#8D6E63]">
          {{ userInfo.nickname }}님의 빵 여정을 탐험하세요! 🍞
        </p>
      </div>
    </div>

    <div v-else class="flex justify-center items-center h-96">
      <div class="text-xl text-[#8D6E63]">사용자를 찾을 수 없습니다.</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
</style>
