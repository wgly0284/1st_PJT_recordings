<template>
  <!-- mypage와 동일한 외부 레이아웃 -->
  <div class="min-h-screen bg-cream-100 flex items-center justify-center p-24">
    <div class="w-full max-w-6xl bg-white rounded-[2.5rem] shadow-soft p-8 md:p-16 border border-gray-100">
      <div class="flex flex-col md:flex-row gap-12 items-start">
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
            <div
              v-else
              class="w-full h-full rounded-full border-4 border-[#F9F7F2] shadow-lg bg-gray-200 flex items-center justify-center text-5xl"
            >
              🥖
            </div>

            <!-- 숨겨진 파일 입력 -->
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleImageUpload"
            />

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

          <!-- 프로필 이미지 저장 -->
          <button
            @click="saveProfile"
            :disabled="isSaving"
            class="w-full py-4 bg-teal-900 text-white font-bold rounded-2xl 
                   hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed
                   transition-all duration-200 flex items-center justify-center gap-2 mb-4"
          >
            <span v-if="isSaving">저장 중...</span>
            <span v-else>이미지 저장</span>
          </button>
        </div>

        <!-- 오른쪽: 빵 선호도 + 계정 정보 수정 -->
        <div class="flex-1 w-full space-y-8">
          <!-- 빵 선호도 -->
          <div class="bg-[#F9F7F2] p-8 rounded-[2rem]">
            <div class="flex justify-between items-center mb-4">
              <p class="text-xs font-bold text-orange-600 uppercase tracking-widest">
                My Bread Preferences
              </p>
              <button
                @click="openPreferencesModal"
                class="px-4 py-1 bg-teal-900 text-white text-xs font-bold rounded-full hover:bg-teal-800"
              >
                수정하기
              </button>
            </div>

            <div v-if="currentPreferences.length" class="flex flex-wrap gap-2">
              <span
                v-for="pref in currentPreferences"
                :key="pref"
                class="px-3 py-1 bg-teal-800 text-white text-sm rounded-full"
              >
                {{ pref }}
              </span>
            </div>
            <p v-else class="text-sm text-gray-500">선호하는 빵 종류가 없습니다.</p>
          </div>

          <!-- 닉네임 수정 + 중복체크 -->
          <div class="bg-[#F9F7F2] p-8 rounded-[2rem]">
            <h3 class="text-sm font-bold text-orange-600 uppercase tracking-widest mb-4">
              Profile Info
            </h3>
            <form @submit.prevent="updateNickname" class="space-y-3">
              <div class="text-left">
                <label class="block text-xs font-semibold text-gray-500 mb-1">
                  Nickname
                </label>
                <input
                  v-model="nickname"
                  type="text"
                  class="w-full px-4 py-2 border rounded-lg bg-white border-cream-200 focus:ring-teal-800 focus:border-teal-800 text-sm"
                  placeholder="닉네임을 입력하세요"
                  @input="checkNickname"
                />
              </div>

              <!-- 닉네임 중복 / 사용 가능 메시지 -->
              <p v-if="nicknameMessage" :class="['text-xs', nicknameMessageType === 'error' ? 'text-red-500' : 'text-green-600']">
                {{ nicknameMessage }}
              </p>

              <button
                type="submit"
                :disabled="isUpdatingNickname || nicknameMessageType === 'error'"
                class="w-full py-2.5 bg-teal-900 text-white text-sm font-bold rounded-xl hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ isUpdatingNickname ? '저장 중...' : '닉네임 저장' }}
              </button>
            </form>
          </div>

          <!-- 비밀번호 변경 -->
          <div class="bg-[#F9F7F2] p-8 rounded-[2rem]">
            <h3 class="text-sm font-bold text-orange-600 uppercase tracking-widest mb-3">
              Change Password
            </h3>

            <!-- 비밀번호 규칙 안내 -->
            <ul class="mb-4 text-xs text-gray-600 list-disc list-inside space-y-1">
              <li>비밀번호는 최소 8자 이상이어야 합니다.</li>
              <li>숫자만으로 구성할 수 없습니다.</li>
              <li>영문자와 숫자를 함께 사용하는 것을 권장합니다.</li>
            </ul>

            <form @submit.prevent="changePassword" class="space-y-3">
              <div class="text-left">
                <label class="block text-xs font-semibold text-gray-500 mb-1">
                  현재 비밀번호
                </label>
                <input
                  v-model="oldPassword"
                  type="password"
                  class="w-full px-4 py-2 border rounded-lg bg-white border-cream-200 focus:ring-teal-800 focus:border-teal-800 text-sm"
                  placeholder="현재 비밀번호"
                />
              </div>
              <div class="text-left">
                <label class="block text-xs font-semibold text-gray-500 mb-1">
                  새 비밀번호
                </label>
                <input
                  v-model="newPassword1"
                  type="password"
                  class="w-full px-4 py-2 border rounded-lg bg-white border-cream-200 focus:ring-teal-800 focus:border-teal-800 text-sm"
                  placeholder="새 비밀번호"
                />
                <!-- 새 비밀번호 규칙/동일 여부 메시지 -->
                <p v-if="passwordSameError" class="mt-1 text-xs text-red-500">
                  기존과 동일한 비밀번호입니다. 다른 비밀번호를 입력해주세요.
                </p>
                <p v-else-if="passwordRuleMessage" :class="['mt-1 text-xs', isPasswordValid ? 'text-green-600' : 'text-red-500']">
                  {{ passwordRuleMessage }}
                </p>
              </div>
              <div class="text-left">
                <label class="block text-xs font-semibold text-gray-500 mb-1">
                  새 비밀번호 확인
                </label>
                <input
                  v-model="newPassword2"
                  type="password"
                  class="w-full px-4 py-2 border rounded-lg bg-white border-cream-200 focus:ring-teal-800 focus:border-teal-800 text-sm"
                  placeholder="새 비밀번호 확인"
                />
              </div>

              <button
                type="submit"
                :disabled="isChangingPassword || !canSubmitPassword"
                class="w-full py-2.5 bg-teal-900 text-white text-sm font-bold rounded-xl hover:bg-teal-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {{ isChangingPassword ? '변경 중...' : '비밀번호 변경' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- 빵 선호도 모달 -->
    <div
      v-if="showPreferencesModal"
      class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-lg shadow-xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-bold text-teal-900">
            {{ authStore.currentUser?.nickname || 'USER' }}님의 빵 취향
          </h3>
          <button
            class="text-gray-400 hover:text-gray-600"
            @click="showPreferencesModal = false"
          >
            ✕
          </button>
        </div>

        <p class="text-gray-600 mb-4 text-sm">
          좋아하는 종류를 모두 선택해주세요.
        </p>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
          <button
            v-for="pref in preferences"
            :key="pref.name"
            @click="togglePreference(pref.name)"
            :class="[
              'p-4 border rounded-lg flex flex-col items-center justify-center transition-all',
              selectedPreferences.includes(pref.name)
                ? 'bg-teal-800 text-white border-teal-800'
                : 'bg-cream-50 border-cream-200 hover:border-teal-800'
            ]"
          >
            <span class="text-3xl mb-2">{{ pref.emoji }}</span>
            <span class="font-semibold">{{ pref.name }}</span>
          </button>
        </div>

        <div class="flex justify-end gap-2">
          <button
            class="px-4 py-2 rounded-xl text-sm text-gray-600 hover:bg-gray-100"
            @click="showPreferencesModal = false"
          >
            취소
          </button>
          <button
            class="px-4 py-2 rounded-xl text-sm bg-teal-800 text-white hover:bg-teal-700"
            @click="savePreferences"
          >
            저장
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/axios'

const authStore = useAuthStore()

const fileInput = ref(null)
const showPreferencesModal = ref(false)
const localProfileImageUrl = ref(null)
const isSaving = ref(false)

// 닉네임
const nickname = ref(authStore.currentUser?.nickname || '')
const isUpdatingNickname = ref(false)
const nicknameMessage = ref('')
const nicknameMessageType = ref(null) // 'error' | 'success' | null

// 비밀번호
const oldPassword = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')
const isChangingPassword = ref(false)

const passwordSameError = ref(false)
const passwordRuleMessage = ref('')
const isPasswordValid = ref(false)

// --- 빵 취향 부분 ---
const preferences = ref([
  { name: '담백/고소', emoji: '🥖' },
  { name: '달콤한', emoji: '🥐' },
  { name: '부드러운', emoji: '🍞' },
  { name: '바삭/하드', emoji: '🥨' },
  { name: '디저트류', emoji: '🍰' },
  { name: '조리빵', emoji: '🌭' },
])

const currentPreferences = computed(() => {
  return authStore.currentUser?.bread_preferences
    ? authStore.currentUser.bread_preferences.split(',')
    : []
})

const selectedPreferences = ref([])

onMounted(() => {
  selectedPreferences.value = [...currentPreferences.value]
})

// 이미지 업로드 관련
const openFileDialog = () => fileInput.value?.click()

const handleImageUpload = (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  localProfileImageUrl.value = URL.createObjectURL(file)
}

const saveProfile = async () => {
  isSaving.value = true
  try {
    const file = fileInput.value?.files?.[0]
    if (file) {
      const formData = new FormData()
      formData.append('profile_image', file)

      const res = await apiClient.patch('/accounts/profile-image/', formData)
      const url = `http://127.0.0.1:8000${res.data.profile_image_url}`
      localProfileImageUrl.value = url
    }

    await authStore.fetchUser()
    alert('프로필 이미지가 저장되었습니다!')
  } catch (e) {
    console.error('저장 실패:', e.response?.status, e.response?.data)
    alert('이미지 저장 중 오류가 발생했습니다.')
  } finally {
    isSaving.value = false
  }
}

// --- 빵 선호도 모달 ---
const openPreferencesModal = () => {
  selectedPreferences.value = [...currentPreferences.value]
  showPreferencesModal.value = true
}

const togglePreference = (prefName) => {
  const index = selectedPreferences.value.indexOf(prefName)
  if (index > -1) {
    selectedPreferences.value.splice(index, 1)
  } else {
    selectedPreferences.value.push(prefName)
  }
}

const savePreferences = async () => {
  try {
    const preferencesString = selectedPreferences.value.join(',')

    await apiClient.patch('/accounts/preferences/', {
      bread_preferences: preferencesString,
    })

    await authStore.fetchUser()
    showPreferencesModal.value = false
    alert('빵 선호도가 저장되었습니다!')
  } catch (e) {
    console.error('빵 선호도 저장 실패:', e.response?.status, e.response?.data)
    alert('빵 선호도 저장 중 오류가 발생했습니다.')
  }
}

// --- 닉네임 중복 검사 ---
// 예시: GET /accounts/check-nickname/?nickname=xxx  -> { available: true/false }
const checkNickname = async () => {
  nicknameMessage.value = ''
  nicknameMessageType.value = null

  const value = nickname.value.trim()
  if (!value || value === authStore.currentUser?.nickname) {
    // 비워졌거나 기존 닉네임이면 메시지 X
    return
  }

  try {
    const res = await apiClient.get('/accounts/check-nickname/', {
      params: { nickname: value },
    })
    if (res.data.available) {
      nicknameMessage.value = '사용 가능한 이름입니다.'
      nicknameMessageType.value = 'success'
    } else {
      nicknameMessage.value = '이미 존재하는 이름입니다. 다른 이름을 사용해주세요.'
      nicknameMessageType.value = 'error'
    }
  } catch (e) {
    console.error('닉네임 중복 검사 실패:', e.response?.status, e.response?.data)
    nicknameMessage.value = '닉네임 확인 중 오류가 발생했습니다.'
    nicknameMessageType.value = 'error'
  }
}

const updateNickname = async () => {
  const value = nickname.value.trim()
  if (!value) {
    alert('닉네임을 입력해주세요.')
    return
  }
  if (nicknameMessageType.value === 'error') {
    alert('사용 불가능한 닉네임입니다.')
    return
  }

  isUpdatingNickname.value = true
  try {
    await apiClient.patch('/accounts/user/', {
      nickname: value,
    })
    await authStore.fetchUser()
    alert('닉네임이 변경되었습니다!')
    nicknameMessage.value = ''
    nicknameMessageType.value = null
  } catch (e) {
    console.error('닉네임 변경 실패:', e.response?.status, e.response?.data)
    alert('닉네임 변경 중 오류가 발생했습니다.')
  } finally {
    isUpdatingNickname.value = false
  }
}

// --- 비밀번호 규칙 / 동일 여부 체크 ---
const validatePasswordRules = () => {
  passwordSameError.value = false
  passwordRuleMessage.value = ''
  isPasswordValid.value = false

  const pw = newPassword1.value

  if (!pw) return

  // 1) 기존 비밀번호와 동일한지
  if (pw === oldPassword.value) {
    passwordSameError.value = true
    return
  }

  // 2) 규칙: 8자 이상, 숫자만은 불가
  if (pw.length < 8) {
    passwordRuleMessage.value = '8자 이상이어야 합니다.'
    return
  }
  const onlyDigits = /^\d+$/ // 숫자만
  if (onlyDigits.test(pw)) {
    passwordRuleMessage.value = '숫자만으로는 사용할 수 없습니다.'
    return
  }

  // 통과
  isPasswordValid.value = true
  passwordRuleMessage.value = '사용 가능한 비밀번호입니다.'
}

watch([oldPassword, newPassword1], validatePasswordRules)

const canSubmitPassword = computed(() => {
  return (
    oldPassword.value &&
    newPassword1.value &&
    newPassword2.value &&
    !passwordSameError.value &&
    isPasswordValid.value
  )
})

const changePassword = async () => {
  if (!canSubmitPassword.value) {
    alert('비밀번호 조건을 다시 확인해주세요.')
    return
  }
  if (newPassword1.value !== newPassword2.value) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  isChangingPassword.value = true
  try {
    await apiClient.post('/accounts/password/change/', {
      old_password: oldPassword.value,
      new_password1: newPassword1.value,
      new_password2: newPassword2.value,
    })

    oldPassword.value = ''
    newPassword1.value = ''
    newPassword2.value = ''
    passwordSameError.value = false
    passwordRuleMessage.value = ''
    isPasswordValid.value = false

    alert('비밀번호가 변경되었습니다!')
  } catch (e) {
    console.error('비밀번호 변경 실패:', e.response?.status, e.response?.data)
    alert('비밀번호 변경 중 오류가 발생했습니다.')
  } finally {
    isChangingPassword.value = false
  }
}
</script>
