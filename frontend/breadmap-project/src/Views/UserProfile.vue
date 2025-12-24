<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'

const route = useRoute()
const authStore = useAuthStore()

// 라우트에 있는 userId (다른 사람 프로필용)
const routeUserId = computed(() =>
  route.params.userId ? Number(route.params.userId) : null
)
// 로그인한 내 유저 ID
const myUserId = computed(() => authStore.user?.pk ?? null)

const userInfo = ref(null)
const isLoading = ref(true)
const isFollowed = ref(false)
const isFollowing = ref(false)

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

const characterImages = {
  hamster: 'https://cdn-icons-png.flaticon.com/512/235/235394.png',
  bear: 'https://cdn-icons-png.flaticon.com/512/235/235388.png',
  lion: 'https://cdn-icons-png.flaticon.com/512/235/235352.png',
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

// 본인 페이지인지 여부
const isMyPage = computed(() => {
  // 라우트에 userId가 없으면 내 마이페이지
  if (routeUserId.value === null) return true
  // 라우트 userId와 내 ID가 같으면 내 페이지
  return myUserId.value !== null && routeUserId.value === myUserId.value
})

// 팔로우 버튼 노출 조건: 로그인 + 타 유저 프로필일 때만
const shouldShowFollowButton = computed(() => {
  return authStore.isAuthenticated &&
         !isMyPage.value &&
         routeUserId.value !== null
})

// 프로필 데이터 가져오기
const fetchUserProfile = async () => {
  try {
    let response

    console.log('routeUserId =', routeUserId.value, 'myUserId =', myUserId.value, 'isMyPage =', isMyPage.value)

    if (!isMyPage.value && routeUserId.value !== null) {
      const url = `http://127.0.0.1:8000/accounts/user/${routeUserId.value}/`
      console.log('🔵 타 유저 프로필 요청:', url)
      response = await axios.get(url, {
        headers: authStore.token ? { Authorization: `Token ${authStore.token}` } : {},
      })
    } else {
      const url = 'http://127.0.0.1:8000/accounts/profile/'
      console.log('🟠 내 프로필 요청:', url)
      response = await axios.get(url, {
        headers: authStore.token ? { Authorization: `Token ${authStore.token}` } : {},
      })
    }

    console.log('프로필 응답 data =', response.data)

    const data = response.data
    userInfo.value = {
      id: data.id || data.user_id,
      nickname: data.nickname || data.username,
      level: data.level || 1,
      level_title: LEVEL_CONFIG[data.level || 1]?.name || '아기빵쥐',
      exp: data.exp || 0,
      next_exp: data.max_exp || data.next_exp || 100,
      profile_image_url: data.profile_image_url
        ? `http://127.0.0.1:8000${data.profile_image_url}`
        : null,
      character_type: data.character_type || 'hamster',
      follower_count: Number(data.follower_count || 0),
      following_count: Number(data.following_count || 0),
      review_count: Number(data.review_count || 0),
      post_count: Number(data.post_count || 0),
      date_joined: data.date_joined || new Date().toISOString().split('T')[0],
    }
    isLoading.value = false
  } catch (error) {
    console.error('프로필 로드 실패:', error)
    isLoading.value = false
  }
}

// 팔로우 상태 확인
const checkFollowStatus = async () => {
  if (!authStore.isAuthenticated || !shouldShowFollowButton.value) return
  try {
    const response = await apiClient.get('/accounts/following/')
    const followingIds = response.data.following?.map((u) => u.id) || []
    isFollowed.value = followingIds.includes(routeUserId.value)
  } catch (error) {
    console.error('팔로우 상태 확인 실패:', error)
  }
}

// 팔로우/언팔로우 토글
const handleFollow = async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요합니다.')
    return
  }
  if (isFollowing.value) return

  try {
    isFollowing.value = true
    const response = await apiClient.post(`/accounts/follow/${routeUserId.value || postData.value.author_id}/`)
    const data = response.data

    // status로 팔로우 여부 결정
    isFollowed.value = data.status === 'followed'

    // ✅ follower_count는 서버 값으로 덮어쓴다 (있을 때만)
    if (userInfo.value && typeof data.follower_count === 'number') {
      userInfo.value.follower_count = data.follower_count
    } else if (userInfo.value) {
      // 서버에서 카운트 안 내려주면 최소 0 아래로는 안 떨어지게 방어
      const delta = isFollowed.value ? 1 : -1
      userInfo.value.follower_count = Math.max(0, (userInfo.value.follower_count || 0) + delta)
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
    <!-- 로딩 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center h-screen">
      <div class="animate-spin rounded-full h-12 w-12 border-4 border-[#AED581] border-t-transparent"></div>
      <p class="mt-4 text-[#5D4037] font-bold animate-pulse font-serif">빵 굽는 중... 🥐</p>
    </div>

    <!-- 프로필 -->
    <div v-else-if="userInfo">
      <!-- 프로필 헤더 -->
      <div class="relative pt-12 pb-20 px-6 rounded-b-[50px] shadow-xl overflow-hidden z-10 bg-gradient-to-b from-[#F1F8E9] to-[#DCEDC8]">

        <!-- ☁️ 몽글몽글 배경 효과 (Blobs - 연두빛) -->
        <div class="absolute top-[-20%] left-[-10%] w-72 h-72 bg-lime-200/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob"></div>
        <div class="absolute top-[-20%] right-[-10%] w-72 h-72 bg-green-200/40 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000"></div>
        <div class="absolute bottom-[-20%] left-[20%] w-72 h-72 bg-yellow-100/60 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000"></div>
        <div class="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/cream-paper.png')]"></div>

        <div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8 relative z-10">

          <!-- 캐릭터/프로필 이미지 -->
          <div class="relative group cursor-pointer transition-transform hover:scale-105 duration-300 shrink-0">
            <div class="w-36 h-36 bg-white rounded-full border-[6px] border-white shadow-xl flex items-center justify-center overflow-hidden relative z-10">
              <img :src="getProfileImage" :class="userInfo.profile_image_url ? 'w-full h-full object-cover' : 'w-24 h-24 object-contain drop-shadow-lg'" @error="handleImageError">
            </div>
            <!-- 레벨 뱃지 (연두색 포인트) -->
            <div class="absolute -bottom-3 left-1/2 -translate-x-1/2 bg-[#8BC34A] text-white font-bold px-4 py-1.5 rounded-full shadow-lg whitespace-nowrap z-20 flex items-center gap-1 text-sm font-serif border border-white/50">
              <span class="text-xs opacity-90">Lv.{{ userInfo.level }}</span>
              <span>{{ currentLevelInfo.name }}</span>
            </div>
          </div>

          <!-- 정보 (오른쪽) -->
          <div class="flex-1 text-center md:text-left w-full">
            <div class="flex flex-col md:flex-row md:items-end gap-3 mb-3 justify-center md:justify-start">
              <h2 class="text-3xl font-extrabold tracking-tight text-[#4E342E] font-serif">{{ userInfo.nickname }}</h2>
              <span class="text-2xl animate-bounce">{{ currentLevelInfo.icon }}</span>
            </div>

            <!-- 경험치 바 (라임 & 그린 그라데이션) -->
            <div class="relative mb-2 group max-w-md mx-auto md:mx-0">
              <div class="w-full bg-white/60 h-5 rounded-full overflow-hidden backdrop-blur-sm border border-white/40 shadow-inner">
                <div class="bg-gradient-to-r from-[#DCE775] to-[#8BC34A] h-full rounded-full transition-all duration-1000 relative bg-[length:200%_100%] animate-[shimmer_2s_infinite]"
                     :style="{ width: progressWidth }">
                </div>
              </div>
              <div class="absolute top-0 w-full text-center text-[10px] font-bold text-[#558B2F] leading-5 drop-shadow-sm">
                {{ userInfo.exp }} / {{ userInfo.next_exp }} EXP
              </div>
            </div>

            <p class="text-xs text-[#795548] text-center md:text-left mb-5">
              "{{ currentLevelInfo.name }}" 단계입니다. 맛있는 빵을 찾아 떠나보세요! 🚀
            </p>

            <!-- 스탯 요약 (글라스모피즘 스타일) -->
            <div class="flex justify-center md:justify-start gap-4 p-3 bg-white/40 rounded-2xl backdrop-blur-md border border-white/50 shadow-sm inline-flex flex-wrap mb-5">
              <div class="text-center px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.follower_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Followers</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div class="text-center px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.following_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Following</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div class="text-center px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.review_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Reviews</p>
              </div>
              <div class="border-r border-[#8D6E63]/20"></div>
              <div class="text-center px-2">
                <p class="text-lg font-bold text-[#4E342E]">{{ userInfo.post_count }}</p>
                <p class="text-[9px] text-[#8D6E63] uppercase tracking-wider font-bold">Posts</p>
              </div>
            </div>

            <!-- 팔로우 버튼 (본인 X & 로그인 O & 타유저일 때만) -->
            <div v-if="shouldShowFollowButton">
              <button
                @click="handleFollow"
                :disabled="isFollowing"
                :class="[
                  'px-6 py-2.5 rounded-full font-bold text-sm transition-all shadow-lg duration-300',
                  isFollowed
                    ? 'bg-white/60 text-[#558B2F] hover:bg-white/80 border border-white/40'
                    : 'bg-[#8BC34A] text-white hover:bg-[#7CB342]',
                  isFollowing ? 'opacity-60 cursor-not-allowed' : '',
                ]"
              >
                <span v-if="isFollowing" class="animate-spin">⏳</span>
                <span v-else>{{ isFollowed ? '팔로잉' : '팔로우 +' }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 추가 콘텐츠 -->
      <div class="max-w-5xl mx-auto px-4 sm:px-6 pt-8 pb-20">
        <div class="bg-white rounded-3xl p-6 md:p-10 shadow-xl border border-[#F0EBE0]">
          <p class="text-center text-[#8D6E63] text-lg font-medium">
            {{ userInfo.nickname }}님의 빵 여정을 탐험하세요! 🍞
          </p>
        </div>
      </div>
    </div>

    <!-- 에러/없음 -->
    <div v-else class="flex flex-col items-center justify-center h-screen">
      <p class="text-4xl mb-4">🥐</p>
      <div class="text-xl text-[#8D6E63] font-medium">사용자를 찾을 수 없습니다.</div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&family=Gaegu:wght@400;700&display=swap');

div {
  font-family: 'Noto Sans KR', sans-serif;
}

h2, .font-serif {
  font-family: 'Gaegu', cursive;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* 몽글몽글 구름 효과 애니메이션 */
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
