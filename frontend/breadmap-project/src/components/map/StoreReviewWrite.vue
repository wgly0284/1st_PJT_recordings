<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
    <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <!-- 헤더 -->
      <div class="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-3xl z-10">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-bold text-[#1D4E45]">가게 리뷰 작성</h2>
            <p class="text-sm text-gray-500 mt-1">{{ storeName }}</p>
          </div>
          <button
            @click="$emit('close')"
            class="w-10 h-10 rounded-full hover:bg-gray-100 flex items-center justify-center transition-colors"
          >
            <X class="w-6 h-6 text-gray-600" />
          </button>
        </div>
      </div>

      <!-- 본문 -->
      <div class="p-6 space-y-6">
        <!-- 평점 선택 -->
        <div>
          <label class="block text-sm font-bold text-gray-800 mb-3">별점</label>
          <div class="flex items-center gap-2">
            <button
              v-for="star in 5"
              :key="star"
              @click="rating = star"
              class="transition-transform hover:scale-110"
            >
              <Star
                class="w-8 h-8 transition-colors"
                :class="star <= rating ? 'fill-orange-400 text-orange-400' : 'text-gray-300'"
              />
            </button>
            <span class="ml-2 text-lg font-bold text-orange-600">{{ rating }}.0</span>
          </div>
        </div>

        <!-- 먹은 메뉴 선택 -->
        <div>
          <label class="block text-sm font-bold text-gray-800 mb-3">먹은 메뉴를 선택해주세요</label>
          <div class="flex flex-wrap gap-2 mb-3">
            <button
              v-for="menu in popularMenus"
              :key="menu"
              @click="toggleMenu(menu)"
              class="px-4 py-2 rounded-full text-sm font-bold transition-all border-2"
              :class="
                selectedMenus.includes(menu)
                  ? 'bg-amber-500 text-white border-amber-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-amber-300'
              "
            >
              {{ menu }}
            </button>
          </div>
          <!-- 직접 입력 -->
          <div class="flex gap-2">
            <input
              v-model="customMenu"
              @keyup.enter="addCustomMenu"
              placeholder="직접 입력 (엔터로 추가)"
              class="flex-1 px-4 py-2 border-2 border-gray-200 rounded-xl focus:border-amber-500 focus:outline-none text-sm"
            />
            <button
              @click="addCustomMenu"
              class="px-4 py-2 bg-amber-500 text-white rounded-xl font-bold hover:bg-amber-600 transition-colors"
            >
              추가
            </button>
          </div>
          <div v-if="selectedMenus.length > 0" class="mt-2 text-xs text-gray-500">
            선택한 메뉴: {{ selectedMenus.join(', ') }}
          </div>
        </div>

        <!-- 이런 점이 좋았어요 (키워드 선택) -->
        <div>
          <label class="block text-sm font-bold text-gray-800 mb-3">이런 점이 좋았어요</label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="keyword in tasteTags"
              :key="keyword"
              @click="toggleKeyword(keyword)"
              class="px-4 py-2 rounded-full text-sm font-bold transition-all border-2"
              :class="
                selectedKeywords.includes(keyword)
                  ? 'bg-teal-500 text-white border-teal-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-teal-300'
              "
            >
              {{ keyword }}
            </button>
          </div>
        </div>

        <!-- 리뷰 내용 -->
        <div>
          <label class="block text-sm font-bold text-gray-800 mb-3">리뷰 내용</label>
          <textarea
            v-model="content"
            placeholder="가게에 대한 솔직한 리뷰를 남겨주세요 (최소 10자)"
            class="w-full h-40 p-4 border-2 border-gray-200 rounded-2xl focus:border-teal-500 focus:outline-none resize-none text-sm"
          ></textarea>
          <p class="text-xs text-gray-500 mt-2">{{ content.length }}자 / 최소 10자</p>
        </div>

        <!-- 사진 업로드 -->
        <div>
          <label class="block text-sm font-bold text-gray-800 mb-3">사진 (선택)</label>
          <div class="flex items-center gap-4">
            <label
              class="flex-1 border-2 border-dashed border-gray-300 rounded-2xl p-6 text-center cursor-pointer hover:border-teal-400 transition-colors"
            >
              <input type="file" accept="image/*" @change="handleImageUpload" class="hidden" />
              <Camera class="w-8 h-8 text-gray-400 mx-auto mb-2" />
              <p class="text-sm text-gray-600">사진 업로드</p>
            </label>
            <div v-if="imagePreview" class="relative w-32 h-32 rounded-2xl overflow-hidden border-2 border-gray-200">
              <img :src="imagePreview" class="w-full h-full object-cover" />
              <button
                @click="removeImage"
                class="absolute top-1 right-1 w-6 h-6 bg-black/60 rounded-full flex items-center justify-center text-white hover:bg-black/80"
              >
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 하단 버튼 -->
      <div class="sticky bottom-0 bg-white border-t border-gray-200 p-6 rounded-b-3xl">
        <button
          @click="submitReview"
          :disabled="!isValid"
          class="w-full py-4 bg-teal-600 text-white rounded-xl font-bold hover:bg-teal-700 transition-all disabled:bg-gray-300 disabled:cursor-not-allowed shadow-lg"
        >
          리뷰 작성 완료
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { X, Star, Camera } from 'lucide-vue-next'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  storeId: { type: Number, required: true },
  storeName: { type: String, required: true }
})

const emit = defineEmits(['close', 'review-created'])

const authStore = useAuthStore()

// 폼 데이터
const rating = ref(5)
const content = ref('')
const imageFile = ref(null)
const imagePreview = ref(null)
const selectedKeywords = ref([])
const selectedMenus = ref([])
const customMenu = ref('')
const popularMenus = ref([])

// 키워드 옵션 (네이버 지도 스타일)
const tasteTags = [
  '맛있어요',
  '친절해요',
  '깨끗해요',
  '분위기 좋아요',
  '재방문 의사 있어요',
  '가성비 좋아요',
  '신선해요',
  '특별해요'
]

// 가게 정보 불러오기 (대표 메뉴 포함)
const fetchStoreInfo = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/stores/${props.storeId}/`)
    const store = response.data

    // popular_menu_items가 있으면 파싱
    if (store.popular_menu_items) {
      popularMenus.value = store.popular_menu_items.split(',').map(item => item.trim()).filter(item => item)
    }

    // 기본 메뉴가 없으면 일반적인 빵 메뉴 제공
    if (popularMenus.value.length === 0) {
      popularMenus.value = ['소금빵', '크루아상', '바게트', '식빵', '단팥빵', '카스테라']
    }
  } catch (error) {
    console.error('가게 정보 로드 실패:', error)
    // 실패 시 기본 메뉴
    popularMenus.value = ['소금빵', '크루아상', '바게트', '식빵', '단팥빵', '카스테라']
  }
}

onMounted(() => {
  fetchStoreInfo()
})

// 유효성 검사
const isValid = computed(() => {
  return content.value.trim().length >= 10
})

// 키워드 토글
const toggleKeyword = (keyword) => {
  const index = selectedKeywords.value.indexOf(keyword)
  if (index > -1) {
    selectedKeywords.value.splice(index, 1)
  } else {
    selectedKeywords.value.push(keyword)
  }
}

// 메뉴 토글
const toggleMenu = (menu) => {
  const index = selectedMenus.value.indexOf(menu)
  if (index > -1) {
    selectedMenus.value.splice(index, 1)
  } else {
    selectedMenus.value.push(menu)
  }
}

// 커스텀 메뉴 추가
const addCustomMenu = () => {
  const menu = customMenu.value.trim()
  if (menu && !selectedMenus.value.includes(menu)) {
    selectedMenus.value.push(menu)
    customMenu.value = ''
  }
}

// 이미지 업로드
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 이미지 제거
const removeImage = () => {
  imageFile.value = null
  imagePreview.value = null
}

// 리뷰 제출
const submitReview = async () => {
  if (!isValid.value) return

  try {
    const formData = new FormData()
    formData.append('rating', rating.value)
    formData.append('content', content.value)
    formData.append('taste_tags', selectedKeywords.value.join(','))
    formData.append('menu_items', selectedMenus.value.join(','))

    if (imageFile.value) {
      formData.append('image', imageFile.value)
    }

    const response = await axios.post(
      `http://127.0.0.1:8000/stores/${props.storeId}/reviews/`,
      formData,
      {
        headers: {
          Authorization: `Token ${authStore.token}`,
          'Content-Type': 'multipart/form-data'
        }
      }
    )

    emit('review-created', response.data)
    emit('close')
  } catch (error) {
    console.error('리뷰 작성 실패:', error)
    alert('리뷰 작성에 실패했습니다.')
  }
}
</script>
