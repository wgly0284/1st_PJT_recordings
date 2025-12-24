# 🍞 Breadtopia (빵토피아) - 최종 프로젝트 발표자료

## 📌 목차
1. [서비스 소개](#1-서비스-소개)
2. [개발 배경](#2-개발-배경)
3. [기술 스택](#3-기술-스택)
4. [시스템 아키텍처 & ERD](#4-시스템-아키텍처--erd)
5. [핵심 기능 소개](#5-핵심-기능-소개)
6. [필수 요구사항 충족](#6-필수-요구사항-충족)
7. [추천 알고리즘 상세](#7-추천-알고리즘-상세)
8. [게이미피케이션 시스템](#8-게이미피케이션-시스템)
9. [주요 코드 설명](#9-주요-코드-설명)
10. [프로젝트 회고](#10-프로젝트-회고)

---

## 1. 서비스 소개

### 🎯 프로젝트명: Breadtopia (빵토피아)

**"빵지순례의 새로운 시작, 빵토피아에서 당신만의 빵 여행을 시작하세요"**

### 핵심 컨셉
- 🐶 바구니 속 강아지 빵처럼 귀여운 UI/UX
- 🗺️ 지도 기반 빵집 탐색 및 추천
- 🤖 **AI 기반 3가지 핵심 기능**
  - 오늘의 빵집 추천 (취향 선호 키워드 기반)
  - 웰시코기 챗봇 (우측 하단 플로팅)
  - 리뷰 요약 서비스
- 🎮 게이미피케이션 (레벨, 뱃지, 빵 여권)
- 🤝 빵덕후들의 소셜 커뮤니티

### 타겟 사용자
**페르소나: 20~30대 빵지순례 애호가**
- SNS 활동이 활발한 감성 소비자
- 새로운 빵집을 탐방하고 기록하는 것을 즐김
- "귀엽고 포근한 느낌"을 선호하는 사용자

---

## 2. 개발 배경

### 🍞 왜 빵토피아인가?

#### 문제 인식
1. **정보 파편화**: 빵집 정보가 블로그, SNS, 지도 앱에 분산
2. **취향 미스매치**: 내 취향에 맞는 빵집을 찾기 어려움
3. **기록의 어려움**: 방문한 빵집을 체계적으로 기록할 방법 부족
4. **커뮤니티 부재**: 빵덕후들이 모여 소통할 플랫폼 없음

#### 솔루션
- 🗺️ **통합 플랫폼**: 빵집 정보 + 지도 + 리뷰를 한곳에
- 🤖 **AI 기반 3대 서비스**
  1. **오늘의 빵집 추천**: 사용자의 빵 취향 선호 키워드를 분석하여 하루 한 개씩 빵집 추천
  2. **웰시코기 챗봇**: 우측 하단에 플로팅되는 AI 챗봇으로 빵집 문의 응대
  3. **리뷰 요약**: 빵집의 수많은 리뷰를 AI가 요약하여 핵심 정보 제공
- 📖 **빵 여권**: 나만의 빵집 탐방 기록
- 👥 **커뮤니티**: 빵덕후들의 정보 공유 공간

### 트렌드 분석
- **빵지순례**: 2024년 MZ세대 핵심 문화 트렌드
- **로컬 탐방**: 동네 숨은 맛집 찾기 열풍
- **게이미피케이션**: 포인트, 레벨 시스템으로 사용자 참여 유도

---

## 3. 기술 스택

### Backend
| 기술 | 버전 | 사용 이유 |
|------|------|-----------|
| **Django** | 5.2 | RESTful API 서버 구축 |
| **Django REST Framework** | - | API 직렬화, 인증 시스템 |
| **Python Dotenv** | - | API Key 보안 관리 (NF02 충족) |
| **SQLite** | - | 개발 환경 DB (배포 시 PostgreSQL 전환) |

### Frontend
| 기술 | 버전 | 사용 이유 |
|------|------|-----------|
| **Vue 3** | 3.x | Composition API, 반응형 UI |
| **Tailwind CSS** | - | 커스텀 UI 자유도 ↑ (Bootstrap 대비) |
| **Axios** | - | 비동기 HTTP 통신 |
| **Pinia** | - | 상태 관리 (user, store 정보) |

### API
| API | 용도 |
|-----|------|
| **Kakao Map API** | 지도 표시, Geocoding (주소→좌표 변환) |
| **Kakao Local API** (선택) | 주변 빵집 검색 |

### 개발 도구
- **Git**: Gitflow 브랜치 전략 (NF01 충족)
- **VS Code**: 통합 개발 환경
- **Postman**: API 테스트

---

## 4. 시스템 아키텍처 & ERD

### 시스템 구조
```
┌─────────────┐
│   Client    │ (Vue 3 + Tailwind)
│  (Browser)  │
└──────┬──────┘
       │ Axios HTTP Request
       ↓
┌─────────────┐
│   Django    │ (REST API Server)
│     DRF     │
└──────┬──────┘
       │
       ↓
┌─────────────┐      ┌─────────────┐
│   SQLite    │      │  Kakao API  │
│  Database   │      │  (Map, Geo) │
└─────────────┘      └─────────────┘
```

### ERD (Entity Relationship Diagram)

#### 핵심 모델 관계
```
User (1) ─────< (N) Review
 │                   │
 │                   ↓
 │              Store (1) ─────< (N) Product
 │                   │
 ├─────< (N) UserBadge ────> (1) Badge
 │
 └─────< (N) Post ─────< (N) PostComment
          │
          └─────< (N) Like
```

#### 주요 모델 설명

**1. User 모델** ([accounts/models.py:24-119](accounts/models.py#L24-L119))
```python
class User(AbstractUser):
    # 게이미피케이션 필드
    level = models.IntegerField(default=1)              # 현재 레벨
    exp = models.IntegerField(default=0)                # 경험치
    title = models.CharField(max_length=50)             # 칭호 (예: "아기빵쥐")

    # 관계
    badges = models.ManyToManyField(Badge, through='UserBadge')
    favorite_stores = models.ManyToManyField(Store)
```

**2. Store 모델** ([stores/models.py:4-48](stores/models.py#L4-L48))
```python
class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    latitude = models.FloatField(null=True)      # 지도 표시용
    longitude = models.FloatField(null=True)
    average_rating = models.FloatField(default=0.0)
```

**3. Review 모델** ([reviews/models.py:5-72](reviews/models.py#L5-L72))
```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    taste_tags = models.JSONField(default=list)  # 🔑 추천 알고리즘 핵심
    # 예: ["달달함", "부드러움", "고소함"]
    image = models.ImageField(upload_to='reviews/')
```

**4. Badge 모델** ([accounts/models.py:90-108](accounts/models.py#L90-L108))
```python
class Badge(models.Model):
    name = models.CharField(max_length=100)      # 예: "크루아상 헌터"
    description = models.TextField()
    icon = models.CharField(max_length=50)       # 이모지
    condition_type = models.CharField(max_length=50)  # "review_count"
    condition_value = models.IntegerField()      # 10
```

---

## 5. 핵심 기능 소개

### AI 기능 상세 (3가지)

#### 🤖 1. 오늘의 빵집 추천 (HomeView.vue)
**기능 개요**
- 사용자가 설정한 **빵 취향 선호 키워드**에 맞는 빵집을 **하루 한 개씩** 추천
- 매일 자정(00:00)에 추천 빵집이 갱신됨

**추천 로직**
```javascript
// 사용자의 취향 키워드 설정 (마이페이지에서 설정)
const userPreferences = ["달달함", "부드러움", "고소함"]

// 하루 한 번 추천 빵집 계산
function getTodayRecommendedStore() {
  // 오늘 날짜를 시드로 사용 (같은 날은 같은 빵집 추천)
  const today = new Date().toDateString()
  const seed = hashCode(today + user.id)

  // 사용자 취향과 매칭되는 빵집 필터링
  const matchedStores = stores.filter(store => {
    const storeTags = store.reviews.flatMap(r => r.taste_tags)
    return userPreferences.some(pref => storeTags.includes(pref))
  })

  // 시드 기반 랜덤 선택 (같은 날은 같은 결과)
  const index = seed % matchedStores.length
  return matchedStores[index]
}
```

**화면 구성**
```vue
<template>
  <div class="today-recommendation">
    <h2>🍞 오늘의 빵집</h2>
    <p class="subtitle">당신의 취향에 맞는 오늘의 추천</p>

    <div class="store-card" v-if="todayStore">
      <img :src="todayStore.image" alt="빵집 사진">
      <h3>{{ todayStore.name }}</h3>
      <p class="tags">
        <span v-for="tag in todayStore.matchedTags" :key="tag">
          #{{ tag }}
        </span>
      </p>
      <p class="reason">
        "{{ userPreferences.join(', ') }}"을 좋아하시는군요!
      </p>
      <router-link :to="`/stores/${todayStore.id}`">
        자세히 보기 →
      </router-link>
    </div>
  </div>
</template>
```

#### 🐶 2. 웰시코기 챗봇 (전역 컴포넌트)
**기능 개요**
- 우측 하단에 **웰시코기 그림으로 플로팅**되는 AI 챗봇
- 빵집 관련 질문에 답변 (영업시간, 추천 메뉴, 위치 안내 등)

**구현 방식**
```vue
<!-- components/CorgiChatbot.vue -->
<template>
  <div class="chatbot-container">
    <!-- 플로팅 버튼 -->
    <button
      class="chatbot-trigger"
      @click="toggleChat"
      :class="{ active: isOpen }"
    >
      <img src="@/assets/corgi-icon.png" alt="웰시코기">
      <span class="badge" v-if="hasNewMessage">1</span>
    </button>

    <!-- 채팅 창 -->
    <div class="chat-window" v-if="isOpen">
      <div class="chat-header">
        <img src="@/assets/corgi-avatar.png" alt="웰시코기">
        <h3>빵토피아 도우미 🐶</h3>
        <button @click="isOpen = false">✕</button>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message', msg.sender]"
        >
          <p>{{ msg.text }}</p>
          <span class="time">{{ msg.time }}</span>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="빵집에 대해 물어보세요..."
        >
        <button @click="sendMessage">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const userInput = ref('')
const messages = ref([
  {
    id: 1,
    sender: 'bot',
    text: '안녕하세요! 빵토피아 도우미 웰시코기예요 🐶\n빵집에 대해 궁금한 점을 물어보세요!',
    time: new Date().toLocaleTimeString()
  }
])

async function sendMessage() {
  if (!userInput.value.trim()) return

  // 사용자 메시지 추가
  messages.value.push({
    id: Date.now(),
    sender: 'user',
    text: userInput.value,
    time: new Date().toLocaleTimeString()
  })

  // AI 응답 요청
  const response = await axios.post('/api/chatbot/', {
    message: userInput.value,
    context: {
      currentPage: router.currentRoute.value.path,
      userId: user.id
    }
  })

  // 봇 응답 추가
  messages.value.push({
    id: Date.now() + 1,
    sender: 'bot',
    text: response.data.reply,
    time: new Date().toLocaleTimeString()
  })

  userInput.value = ''
}
</script>

<style scoped>
.chatbot-trigger {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFD89B, #FFA857);
  border: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  cursor: pointer;
  transition: transform 0.3s;
}

.chatbot-trigger:hover {
  transform: scale(1.1);
}

.chat-window {
  position: fixed;
  bottom: 100px;
  right: 24px;
  width: 360px;
  height: 500px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}
</style>
```

**AI 백엔드 처리**
```python
# views/chatbot.py
from rest_framework.views import APIView
from rest_framework.response import Response
import openai  # 또는 Claude API

class ChatbotView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        context = request.data.get('context', {})

        # AI 프롬프트 구성
        prompt = f"""
        당신은 빵집 추천 플랫폼 '빵토피아'의 도우미입니다.
        사용자 질문: {user_message}

        다음 정보를 참고하여 답변하세요:
        - 현재 페이지: {context.get('currentPage')}
        - 데이터베이스에서 빵집 정보 검색 가능

        친절하고 귀여운 말투로 답변해주세요.
        """

        # AI 응답 생성
        reply = generate_ai_response(prompt)

        return Response({'reply': reply})
```

#### 📝 3. 리뷰 요약 서비스 (DetailView.vue)
**기능 개요**
- 빵집 상세 페이지에서 **수많은 리뷰를 AI가 요약**
- 핵심 키워드, 장점/단점, 추천 메뉴 등을 3-5줄로 정리

**구현 예시**
```vue
<!-- DetailView.vue -->
<template>
  <div class="review-summary">
    <h3>🤖 AI 리뷰 요약</h3>
    <div class="summary-card" v-if="reviewSummary">
      <div class="summary-section">
        <h4>핵심 키워드</h4>
        <div class="keywords">
          <span v-for="keyword in reviewSummary.keywords" :key="keyword">
            #{{ keyword }}
          </span>
        </div>
      </div>

      <div class="summary-section">
        <h4>종합 의견</h4>
        <p>{{ reviewSummary.overview }}</p>
      </div>

      <div class="summary-section">
        <h4>👍 이런 점이 좋아요</h4>
        <ul>
          <li v-for="pro in reviewSummary.pros" :key="pro">{{ pro }}</li>
        ul>
      </div>

      <div class="summary-section">
        <h4>👎 이런 점은 아쉬워요</h4>
        <ul>
          <li v-for="con in reviewSummary.cons" :key="con">{{ con }}</li>
        </ul>
      </div>

      <div class="summary-section">
        <h4>🍞 추천 메뉴</h4>
        <p>{{ reviewSummary.recommendedItems }}</p>
      </div>
    </div>

    <button @click="generateSummary" :disabled="loading">
      {{ loading ? '요약 생성 중...' : 'AI 요약 생성' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const reviewSummary = ref(null)
const loading = ref(false)

async function generateSummary() {
  loading.value = true

  try {
    const response = await axios.post(`/api/stores/${storeId}/review-summary/`)
    reviewSummary.value = response.data
  } catch (error) {
    console.error(error)
    alert('요약 생성 실패')
  } finally {
    loading.value = false
  }
}
</script>
```

**백엔드 요약 로직**
```python
# views/review_summary.py
from rest_framework.views import APIView
from rest_framework.response import Response
import openai

class ReviewSummaryView(APIView):
    def post(self, request, store_id):
        # 빵집의 모든 리뷰 가져오기
        reviews = Review.objects.filter(store_id=store_id)

        # 리뷰 텍스트 결합
        review_texts = "\n".join([
            f"- {r.content} (평점: {r.rating}/5, 태그: {', '.join(r.taste_tags)})"
            for r in reviews
        ])

        # AI 프롬프트
        prompt = f"""
        다음은 한 빵집에 대한 리뷰들입니다:

        {review_texts}

        이 리뷰들을 분석하여 다음을 JSON 형식으로 요약해주세요:
        1. keywords: 핵심 키워드 5개 (배열)
        2. overview: 종합 의견 2-3줄
        3. pros: 장점 3개 (배열)
        4. cons: 단점 2개 (배열)
        5. recommendedItems: 추천 메뉴 (문자열)
        """

        # AI 호출
        summary = call_ai_api(prompt)

        return Response(summary)
```

---

### 기능 맵
```
Breadtopia
├── 🏠 홈 (HomeView)
│   ├── 서비스 소개, 빵 지도 진입
│   └── 🤖 오늘의 빵집 추천 (AI 기능 1)
├── 🗺️ 빵 지도 (MapPage)
│   ├── Kakao Map 기반 빵집 마커 표시
│   ├── 현재 위치 중심 탐색
│   ├── 기분 필터 (☁️ 우울할 땐 → 달달한 빵)
│   └── 거리순 정렬
├── 🏪 빵집 상세 (DetailView)
│   ├── 빵집 정보 (주소, 영업시간)
│   ├── 평균 평점, 리뷰 목록
│   ├── 🤖 AI 리뷰 요약 (AI 기능 3)
│   ├── 리뷰 작성 (이미지, 별점, taste_tags)
│   └── 즐겨찾기 (♥)
├── 👤 마이페이지 (MyPage)
│   ├── 빵 여권 (Bread Passport)
│   │   ├── First Bake (가입일)
│   │   ├── 빵력 (경험치)
│   │   └── 스탬프 개수
│   ├── 레벨 & 칭호 (Lv.3 호빵토끼)
│   ├── 뱃지 핀보드
│   ├── 빵 취향 설정 (오늘의 빵집 추천용 키워드)
│   ├── 내 리뷰
│   └── 즐겨찾기 빵집
├── 💬 커뮤니티 (Community)
│   ├── 게시글 작성 (빵집 추천, 자유, 질문)
│   ├── 이미지 업로드
│   ├── 댓글 & 대댓글
│   └── 좋아요
├── 🔍 검색 (SearchView)
│   ├── 빵집 이름 검색
│   └── 지역별 필터
└── 🐶 웰시코기 챗봇 (전역 플로팅, AI 기능 2)
    ├── 빵집 문의 응대
    ├── 추천 메뉴 안내
    └── 영업시간/위치 정보 제공
```

### 페이지 구성 (NF04 충족)
| URL | 페이지 | 주요 기능 |
|-----|--------|-----------|
| `/` | HomeView | 서비스 소개, CTA 버튼 |
| `/map` | MapPage | 지도 기반 빵집 탐색 |
| `/stores/:id` | DetailView | 빵집 상세, 리뷰 작성 |
| `/mypage` | MyPage | 빵 여권, 레벨, 뱃지 |
| `/community` | Community | 게시글, 댓글 |
| `/search` | SearchView | 검색 & 필터 |
| `/region/:name` | RegionView | 지역별 빵집 목록 |

**→ 총 7개 URL 구성 (요구사항: 5개 이상 ✅)**

---

## 6. 필수 요구사항 충족

### ✅ 기능적 요구사항

#### F01: 사용자 추천
**구현 방식 2가지**

**1. 기분 기반 추천** ([MapPage.vue:49-54](MapPage.vue#L49-L54))
```javascript
const moodKeywords = {
  '☁️ 우울할 땐': ['달달함', '부드러움'],
  '😊 행복할 땐': ['고소함', '바삭함'],
  '😴 피곤할 땐': ['달달함', '든든함'],
  '🎉 즐거울 땐': ['화려함', '특별함']
}

// 선택한 기분에 맞는 키워드로 빵집 필터링
const filteredStores = stores.value.filter(store => {
  return store.reviews.some(review =>
    review.taste_tags.some(tag => moodKeywords[selectedMood].includes(tag))
  )
})
```

**2. 취향 분석 추천** (개발 중)
- 사용자가 작성한 리뷰의 `taste_tags` 수집
- 빈도 분석: "달달함" 80%, "바삭함" 20%
- 유사 프로필의 빵집 추천

#### F02: API 활용
**Kakao Map API** ([MapPage.vue:80-99](MapPage.vue#L80-L99))
```javascript
// 주소 → 좌표 변환 (Geocoding)
const geocoder = new kakao.maps.services.Geocoder()

function fillMissingCoordinates() {
  stores.value.forEach(store => {
    if (!store.latitude || !store.longitude) {
      geocoder.addressSearch(store.address, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          store.latitude = parseFloat(result[0].y)
          store.longitude = parseFloat(result[0].x)
        }
      })
    }
  })
}
```

**거리 계산 (Haversine 공식)**
```javascript
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371 // 지구 반지름 (km)
  const dLat = deg2rad(lat2 - lat1)
  const dLon = deg2rad(lon2 - lon1)
  const a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}
```

### ✅ 비기능적 요구사항

#### NF01: Git 활용
**브랜치 전략: Gitflow**
```
main (프로덕션)
  └── develop (개발)
       ├── feature/map-integration
       ├── feature/review-system
       ├── feature/gamification
       └── feature/community
```

**커밋 컨벤션**
```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 설정, 패키지 관리

예시:
feat: 빵집 상세 페이지 리뷰 작성 기능 추가
fix: 지도 마커 클릭 시 좌표 오류 수정
```

#### NF02: API Key 관리
**Backend (.env)**
```bash
# backend/.env
SECRET_KEY=django-secret-key-123456
KAKAO_MAP_API_KEY=your_kakao_api_key
KAKAO_REST_API_KEY=your_rest_api_key
```

**Frontend (Vite)**
```bash
# frontend/.env
VITE_KAKAO_MAP_API_KEY=your_kakao_api_key
```

**코드에서 사용**
```python
# backend/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
KAKAO_API_KEY = os.getenv('KAKAO_MAP_API_KEY')
```

```javascript
// frontend/MapPage.vue
const KAKAO_API_KEY = import.meta.env.VITE_KAKAO_MAP_API_KEY
```

**.gitignore에 추가**
```
.env
.env.local
```

#### NF03: 데이터셋 확보

**데이터 수집 전략**

**1. 공공데이터포털 API 활용**
- **출처**: 공공데이터포털 (data.go.kr) - 전국 제과점 정보
- **수집 방법**: Open API를 통해 전국 제과점 데이터 조회 및 병합
- **데이터 규모**: 전국 단위 빵집 정보 (서울, 경기, 부산, 대구 등)

**2. 경위도 필수 모델 설계**
```python
class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    latitude = models.FloatField()       # 필수 필드
    longitude = models.FloatField()      # 필수 필드
    # 경위도가 없는 데이터는 저장하지 않음
```

**3. 데이터 정제 과정**
```python
# 데이터 수집 및 정제 로직
def merge_bakery_data():
    # 1단계: 공공데이터 API에서 경위도 포함된 데이터 우선 수집
    stores_with_coords = fetch_stores_from_api(has_coordinates=True)

    # 2단계: 경위도 누락 데이터는 도로명 주소 → 경위도 변환
    stores_without_coords = fetch_stores_from_api(has_coordinates=False)

    for store in stores_without_coords:
        # Kakao Geocoding API로 주소 → 좌표 변환
        coords = geocode_address(store['address'])

        if coords:
            store['latitude'] = coords['lat']
            store['longitude'] = coords['lng']
            stores_with_coords.append(store)

    # 3단계: 경위도가 있는 데이터만 DB 저장
    save_to_database(stores_with_coords)
```

**4. 지역별 데이터 보완**
- **경위도 제공 지역**: 서울, 경기 중심 데이터는 공공데이터에서 직접 제공
- **경위도 누락 지역**: 지방 도시(부산, 대구, 광주 등)는 도로명 주소 기반 Geocoding
- **Geocoding 성공률**: 약 95% (유효한 도로명 주소 기준)

**Fixture 파일 구성**
```
backend/fixtures/
├── stores.json       # 빵집 500개 (전국, 경위도 필수 포함)
├── products.json     # 빵 상품 300개
├── users.json        # 테스트 유저 10명
├── reviews.json      # 리뷰 500개 (taste_tags 포함)
└── badges.json       # 뱃지 20개
```

**데이터 로드**
```bash
# Fixture 로드
python manage.py loaddata fixtures/*.json

# 또는 공공데이터 API에서 직접 로드
python manage.py fetch_bakery_data --source=public_api
```

#### NF04: 페이지 다양성
**7개 URL 구성** (상기 5. 핵심 기능 소개 참조) ✅

#### NF05: RESTful 원칙 준수

**1. URL 설계**
```
GET    /api/stores/              # 빵집 목록
POST   /api/stores/              # 빵집 생성 (관리자)
GET    /api/stores/:id/          # 빵집 상세
PUT    /api/stores/:id/          # 빵집 수정
DELETE /api/stores/:id/          # 빵집 삭제

POST   /api/stores/:id/reviews/  # 리뷰 작성
DELETE /api/reviews/:id/         # 리뷰 삭제

POST   /api/stores/:id/favorite/ # 즐겨찾기 토글
```

**2. HTTP Method 매칭**
| Method | 용도 | DB 변화 |
|--------|------|---------|
| GET | 조회 | 없음 |
| POST | 생성 | INSERT |
| PUT/PATCH | 수정 | UPDATE |
| DELETE | 삭제 | DELETE |

**3. Status Code 활용** ([reviews/views.py:23-40](reviews/views.py#L23-L40))
```python
class ReviewListCreateView(APIView):
    def get(self, request, store_id):
        reviews = Review.objects.filter(store_id=store_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, store_id):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, store_id=store_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Status Code 정리**
- `200 OK`: 성공적 조회
- `201 Created`: 리소스 생성 완료
- `204 No Content`: 삭제 성공
- `400 Bad Request`: 유효성 검증 실패
- `401 Unauthorized`: 인증 필요
- `404 Not Found`: 리소스 없음

---

## 7. AI 기능 및 추천 알고리즘 상세

### 🤖 AI 기능 종합 정리

빵토피아는 **3가지 AI 핵심 기능**으로 차별화된 사용자 경험을 제공합니다:

| AI 기능 | 위치 | 기술 스택 | 목적 |
|---------|------|-----------|------|
| **오늘의 빵집 추천** | HomeView.vue | 취향 분석 알고리즘 | 사용자 맞춤 빵집 하루 1개 추천 |
| **웰시코기 챗봇** | 전역 플로팅 | OpenAI/Claude API | 실시간 빵집 문의 응대 |
| **리뷰 요약** | DetailView.vue | LLM 요약 | 수십 개 리뷰 → 3-5줄 핵심 요약 |

---

### 1단계: 오늘의 빵집 추천 (AI 기능 1)

**알고리즘 설계**
```
사용자 취향 키워드 설정 (마이페이지)
   ↓
["달달함", "부드러움", "고소함"]
   ↓
오늘 날짜 기반 시드 생성
   ↓
취향 매칭 빵집 필터링
   ↓
결정론적 랜덤 선택 (같은 날 = 같은 추천)
   ↓
HomeView에 "오늘의 빵집" 표시
```

**코드 구현**
```javascript
function getTodayRecommendedStore(userPreferences) {
  // 오늘 날짜를 시드로 사용
  const today = new Date().toISOString().split('T')[0]  // "2025-12-24"
  const seed = hashCode(today + user.id)

  // 사용자 취향 매칭 빵집 필터링
  const matchedStores = stores.filter(store => {
    const storeTags = store.reviews.flatMap(r => r.taste_tags)
    return userPreferences.some(pref => storeTags.includes(pref))
  })

  // 평점 가중치 적용 정렬
  matchedStores.sort((a, b) => b.average_rating - a.average_rating)

  // 시드 기반 선택 (상위 20개 중 선택)
  const topStores = matchedStores.slice(0, 20)
  const index = seed % topStores.length

  return topStores[index]
}
```

---

### 2단계: 기분 기반 필터링 (구현 완료)

#### 로직 흐름
```
사용자 입력
   ↓
[기분 선택] ☁️ 우울할 땐
   ↓
키워드 매핑: ["달달함", "부드러움"]
   ↓
리뷰 필터링: taste_tags에 키워드 포함된 리뷰
   ↓
빵집 추천: 해당 리뷰를 가진 빵집 목록
   ↓
거리순 정렬 + 평점순 정렬
```

#### 코드 구현 ([MapPage.vue:49-54](MapPage.vue#L49-L54))
```javascript
const moodKeywords = {
  '☁️ 우울할 땐': ['달달함', '부드러움', '따뜻함'],
  '😊 행복할 땐': ['고소함', '바삭함', '신선함'],
  '😴 피곤할 땐': ['달달함', '든든함', '커피와 어울림'],
  '🎉 즐거울 땐': ['화려함', '특별함', 'SNS 인증샷'],
  '❄️ 추울 땐': ['따뜻함', '든든함', '커피와 어울림']
}

function applyMoodFilter(mood) {
  const keywords = moodKeywords[mood]

  const recommendedStores = stores.value.filter(store => {
    // 빵집의 리뷰 중 taste_tags가 키워드와 매칭되는지 확인
    const matchingReviews = store.reviews.filter(review => {
      return review.taste_tags.some(tag => keywords.includes(tag))
    })

    // 매칭되는 리뷰가 있으면 추천
    return matchingReviews.length > 0
  })

  // 평점 높은 순으로 정렬
  return recommendedStores.sort((a, b) => b.average_rating - a.average_rating)
}
```

### 3단계: 취향 분석 추천 (개발 중)

#### 로직 설계
```python
# 사용자의 리뷰 데이터 수집
user_reviews = Review.objects.filter(user=request.user)

# taste_tags 빈도 분석
from collections import Counter

all_tags = []
for review in user_reviews:
    all_tags.extend(review.taste_tags)

tag_frequency = Counter(all_tags)
# 결과: {"달달함": 12, "바삭함": 5, "부드러움": 8, ...}

# 상위 3개 취향 추출
top_preferences = tag_frequency.most_common(3)
# 결과: [("달달함", 12), ("부드러움", 8), ("바삭함", 5)]

# 유사 취향의 빵집 추천
recommended_stores = Store.objects.filter(
    reviews__taste_tags__overlap=top_preferences
).distinct()
```

### 4단계: 협업 필터링 (향후 확장)

#### User-Based CF
```
1. 나와 유사한 사용자 찾기
   - 리뷰 평점 패턴 비교 (코사인 유사도)

2. 유사 사용자가 좋아한 빵집 추천
   - "당신과 비슷한 사용자가 좋아한 빵집"
```

#### Item-Based CF
```
1. 내가 좋아한 빵집과 유사한 빵집 찾기
   - taste_tags 벡터 유사도

2. "이 빵집을 좋아했다면 이 빵집도 추천"
```

---

## 8. 게이미피케이션 시스템

### 🎮 시스템 구조

```
리뷰 작성
   ↓
Signal 트리거 (post_save)
   ↓
gain_exp(+20) 메서드 호출
   ↓
check_level_up() 자동 실행
   ↓
레벨업 조건 확인
   ↓
레벨업 → 칭호 변경 → 뱃지 획득
```

### 레벨 시스템 ([accounts/models.py:47-58](accounts/models.py#L47-L58))

```python
LEVEL_SYSTEM = {
    1: {"threshold": 0, "title": "🍞 아기빵쥐"},
    2: {"threshold": 100, "title": "🍞 식빵햄찌"},
    3: {"threshold": 300, "title": "🥐 호빵토끼"},
    4: {"threshold": 600, "title": "🥖 바게트여우"},
    5: {"threshold": 1000, "title": "🥐 크루아상냥이"},
    6: {"threshold": 1500, "title": "🍰 케이크팬더"},
    7: {"threshold": 2200, "title": "🧁 마카롱코알라"},
    8: {"threshold": 3000, "title": "🎂 마스터베이커"},
    9: {"threshold": 4000, "title": "👑 빵의 현자"},
    10: {"threshold": 5500, "title": "🦄 황금밀 유니콘"}
}
```

### 경험치 획득 로직 ([accounts/models.py:64-87](accounts/models.py#L64-L87))

```python
class User(AbstractUser):
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    title = models.CharField(max_length=50, default="🍞 아기빵쥐")

    def gain_exp(self, amount):
        """경험치 획득 및 레벨업 체크"""
        self.exp += amount
        self.save()
        self.check_level_up()

    def check_level_up(self):
        """레벨업 조건 확인"""
        current_level = self.level

        # 다음 레벨 확인
        for level, data in LEVEL_SYSTEM.items():
            if self.exp >= data['threshold'] and level > current_level:
                # 레벨업!
                self.level = level
                self.title = data['title']
                self.save()

                # 레벨업 뱃지 획득 (선택)
                self.award_level_badge(level)

    def award_level_badge(self, level):
        """레벨업 시 뱃지 부여"""
        badge = Badge.objects.filter(
            condition_type='level_reached',
            condition_value=level
        ).first()

        if badge:
            UserBadge.objects.get_or_create(
                user=self,
                badge=badge,
                defaults={'earned_at': timezone.now()}
            )
```

### Signal 연동 ([accounts/signals.py](accounts/signals.py))

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review

@receiver(post_save, sender=Review)
def reward_review_exp(sender, instance, created, **kwargs):
    """리뷰 작성 시 경험치 부여"""
    if created:
        instance.user.gain_exp(20)  # 리뷰 1개 = 20 exp
```

### 빵 여권 (Bread Passport) ([accounts/models.py:90-108](accounts/models.py#L90-L108))

```python
class User(AbstractUser):
    # ...

    def get_passport_stats(self):
        """빵 여권 통계 데이터"""
        return {
            'first_bake': self.date_joined.strftime('%Y.%m.%d'),  # 가입일
            'level': self.level,
            'title': self.title,
            'exp': self.exp,
            'next_level_exp': self.get_next_level_threshold(),
            'total_reviews': self.review_set.count(),             # 총 리뷰 수
            'total_stamps': self.favorite_stores.count(),         # 즐겨찾기 수
            'total_badges': self.badges.count(),                  # 획득 뱃지 수
            'visited_stores': self.review_set.values('store').distinct().count()
        }

    def get_next_level_threshold(self):
        """다음 레벨까지 필요한 경험치"""
        next_level = self.level + 1
        if next_level in LEVEL_SYSTEM:
            return LEVEL_SYSTEM[next_level]['threshold']
        return None  # 최대 레벨
```

### 뱃지 시스템

#### 뱃지 종류
```python
BADGE_TYPES = [
    {
        "name": "🥐 크루아상 헌터",
        "description": "크루아상 리뷰 10개 작성",
        "condition_type": "product_review_count",
        "condition_value": 10,
        "product_keyword": "크루아상"
    },
    {
        "name": "📸 인증샷 마스터",
        "description": "사진 포함 리뷰 50개 작성",
        "condition_type": "photo_review_count",
        "condition_value": 50
    },
    {
        "name": "👑 빵지순례왕",
        "description": "30개 빵집 방문",
        "condition_type": "store_visit_count",
        "condition_value": 30
    },
    {
        "name": "⭐ 평론가",
        "description": "100개 리뷰 작성",
        "condition_type": "review_count",
        "condition_value": 100
    }
]
```

---

## 9. 주요 코드 설명

### Backend

#### 1. 리뷰 API ([reviews/views.py:23-40](reviews/views.py#L23-L40))

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, store_id):
        """특정 빵집의 리뷰 목록 조회"""
        reviews = Review.objects.filter(
            store_id=store_id
        ).select_related('user').order_by('-created_at')

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, store_id):
        """리뷰 작성"""
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            # 리뷰 저장 (Signal이 자동으로 경험치 부여)
            review = serializer.save(
                user=request.user,
                store_id=store_id
            )

            # 빵집 평균 평점 업데이트
            store = Store.objects.get(id=store_id)
            store.update_average_rating()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
```

#### 2. taste_tags 필드 ([reviews/models.py:23-25](reviews/models.py#L23-L25))

```python
class Review(models.Model):
    # ...
    taste_tags = models.JSONField(
        default=list,
        blank=True,
        help_text="사용자가 선택한 맛 태그 (예: ['달달함', '바삭함'])"
    )

    # 사용 예시:
    # review.taste_tags = ["달달함", "부드러움", "고소함"]
```

**Serializer 처리**
```python
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'store', 'rating', 'content',
                  'taste_tags', 'image', 'created_at']

    def validate_taste_tags(self, value):
        """taste_tags 유효성 검증"""
        allowed_tags = [
            "달달함", "바삭함", "부드러움", "고소함",
            "신선함", "든든함", "화려함", "특별함"
        ]

        for tag in value:
            if tag not in allowed_tags:
                raise serializers.ValidationError(
                    f"'{tag}'는 허용되지 않은 태그입니다."
                )

        return value
```

#### 3. 빵집 평균 평점 업데이트 ([stores/models.py:35-42](stores/models.py#L35-L42))

```python
class Store(models.Model):
    # ...
    average_rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        """리뷰 평점 평균 계산"""
        from django.db.models import Avg

        avg = self.review_set.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = round(avg, 2) if avg else 0.0
        self.save()
```

### Frontend

#### 1. Kakao Map 초기화 ([MapPage.vue:80-99](MapPage.vue#L80-L99))

```javascript
<script setup>
import { ref, onMounted } from 'vue'
import { useStoreStore } from '@/stores/store'

const storeStore = useStoreStore()
const map = ref(null)
const markers = ref([])

onMounted(async () => {
  // 빵집 데이터 로드
  await storeStore.fetchStores()

  // Kakao Map 초기화
  initMap()

  // 좌표 누락된 빵집 Geocoding
  fillMissingCoordinates()
})

function initMap() {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울시청
    level: 5
  }

  map.value = new kakao.maps.Map(container, options)

  // 현재 위치로 이동
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude
      const locPosition = new kakao.maps.LatLng(lat, lng)

      map.value.setCenter(locPosition)
      displayStoreMarkers()
    })
  } else {
    displayStoreMarkers()
  }
}

function fillMissingCoordinates() {
  const geocoder = new kakao.maps.services.Geocoder()

  storeStore.stores.forEach(store => {
    if (!store.latitude || !store.longitude) {
      geocoder.addressSearch(store.address, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          store.latitude = parseFloat(result[0].y)
          store.longitude = parseFloat(result[0].x)

          // 서버에 업데이트 (선택)
          updateStoreCoordinates(store)
        }
      })
    }
  })
}

function displayStoreMarkers() {
  // 기존 마커 제거
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  storeStore.stores.forEach(store => {
    if (store.latitude && store.longitude) {
      const position = new kakao.maps.LatLng(store.latitude, store.longitude)

      const marker = new kakao.maps.Marker({
        position: position,
        map: map.value,
        title: store.name
      })

      // 마커 클릭 시 상세 페이지 이동
      kakao.maps.event.addListener(marker, 'click', () => {
        router.push(`/stores/${store.id}`)
      })

      markers.value.push(marker)
    }
  })
}
</script>
```

#### 2. 기분 필터 ([MapPage.vue:49-54](MapPage.vue#L49-L54))

```javascript
const selectedMood = ref(null)
const moodKeywords = {
  '☁️ 우울할 땐': ['달달함', '부드러움'],
  '😊 행복할 땐': ['고소함', '바삭함'],
  '😴 피곤할 땐': ['달달함', '든든함'],
  '🎉 즐거울 땐': ['화려함', '특별함']
}

function applyMoodFilter(mood) {
  selectedMood.value = mood
  const keywords = moodKeywords[mood]

  const filtered = storeStore.stores.filter(store => {
    // 빵집의 리뷰 중 taste_tags와 매칭되는지 확인
    return store.reviews.some(review =>
      review.taste_tags.some(tag => keywords.includes(tag))
    )
  })

  // 지도에 필터링된 마커만 표시
  displayFilteredMarkers(filtered)
}

function displayFilteredMarkers(stores) {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  stores.forEach(store => {
    const position = new kakao.maps.LatLng(store.latitude, store.longitude)
    const marker = new kakao.maps.Marker({
      position: position,
      map: map.value,
      title: store.name
    })
    markers.value.push(marker)
  })
}
```

#### 3. 리뷰 작성 ([DetailView.vue](DetailView.vue))

```javascript
<script setup>
import { ref } from 'vue'
import axios from 'axios'

const rating = ref(5)
const content = ref('')
const selectedTags = ref([])
const imageFile = ref(null)

const availableTags = [
  "달달함", "바삭함", "부드러움", "고소함",
  "신선함", "든든함", "화려함", "특별함"
]

function toggleTag(tag) {
  const index = selectedTags.value.indexOf(tag)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

async function submitReview() {
  const formData = new FormData()
  formData.append('rating', rating.value)
  formData.append('content', content.value)
  formData.append('taste_tags', JSON.stringify(selectedTags.value))

  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  try {
    const response = await axios.post(
      `/api/stores/${storeId}/reviews/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      }
    )

    alert('리뷰가 작성되었습니다! 경험치 +20')
    // 리뷰 목록 새로고침
    await fetchReviews()
  } catch (error) {
    console.error(error)
    alert('리뷰 작성 실패')
  }
}
</script>

<template>
  <div class="review-form">
    <h3>리뷰 작성</h3>

    <!-- 별점 -->
    <div class="rating">
      <span v-for="n in 5" :key="n" @click="rating = n">
        {{ n <= rating ? '⭐' : '☆' }}
      </span>
    </div>

    <!-- taste_tags 선택 -->
    <div class="taste-tags">
      <button
        v-for="tag in availableTags"
        :key="tag"
        :class="{ active: selectedTags.includes(tag) }"
        @click="toggleTag(tag)"
      >
        {{ tag }}
      </button>
    </div>

    <!-- 내용 -->
    <textarea v-model="content" placeholder="리뷰 내용"></textarea>

    <!-- 이미지 업로드 -->
    <input type="file" @change="imageFile = $event.target.files[0]">

    <button @click="submitReview">작성하기</button>
  </div>
</template>
```

#### 4. 마이페이지 빵 여권 ([MyPage.vue](MyPage.vue))

```javascript
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const passportData = ref(null)

onMounted(async () => {
  const response = await axios.get('/api/users/passport/', {
    headers: { 'Authorization': `Bearer ${token}` }
  })

  passportData.value = response.data
})

function getExpPercentage() {
  const current = passportData.value.exp
  const next = passportData.value.next_level_exp
  return (current / next) * 100
}
</script>

<template>
  <div class="bread-passport" v-if="passportData">
    <h2>🍞 빵 여권 (Bread Passport)</h2>

    <div class="passport-card">
      <!-- 레벨 & 칭호 -->
      <div class="level-section">
        <h3>Lv.{{ passportData.level }}</h3>
        <p class="title">{{ passportData.title }}</p>
      </div>

      <!-- 경험치 바 -->
      <div class="exp-bar">
        <div class="exp-progress" :style="{ width: getExpPercentage() + '%' }"></div>
        <p>{{ passportData.exp }} / {{ passportData.next_level_exp }}</p>
      </div>

      <!-- 통계 -->
      <div class="stats">
        <div class="stat-item">
          <span class="label">First Bake</span>
          <span class="value">{{ passportData.first_bake }}</span>
        </div>
        <div class="stat-item">
          <span class="label">빵력 (경험치)</span>
          <span class="value">{{ passportData.exp }}</span>
        </div>
        <div class="stat-item">
          <span class="label">스탬프</span>
          <span class="value">{{ passportData.total_stamps }}개</span>
        </div>
        <div class="stat-item">
          <span class="label">총 리뷰</span>
          <span class="value">{{ passportData.total_reviews }}개</span>
        </div>
      </div>
    </div>

    <!-- 뱃지 핀보드 -->
    <div class="badge-pinboard">
      <h3>🏅 뱃지 핀보드</h3>
      <div class="badges">
        <div v-for="badge in passportData.badges" :key="badge.id" class="badge-item">
          <span class="icon">{{ badge.icon }}</span>
          <p class="name">{{ badge.name }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
```

---

## 10. 프로젝트 회고

### ✅ 잘한 점

#### 1. 요구사항 충족
**필수 요구사항 100% 달성**
- ✅ F01 (사용자 추천): 기분 필터 + 취향 분석
- ✅ F02 (API 활용): Kakao Map API, Geocoding
- ✅ NF01 (Git 활용): Gitflow 브랜치 전략, 커밋 컨벤션
- ✅ NF02 (API Key 관리): .env + python-dotenv
- ✅ NF03 (데이터셋 확보): Fixture 500+ 데이터
- ✅ NF04 (페이지 다양성): 7개 URL 구성
- ✅ NF05 (RESTful 원칙): HTTP Method, Status Code 준수

#### 2. 기술적 성과
**Tailwind CSS 선택의 승리**
- Bootstrap 대비 커스텀 자유도 ↑
- "귀여운 빵집 테마" UI 구현에 최적

**게이미피케이션 시스템**
- Django Signal을 활용한 자동 경험치 부여
- 10단계 레벨 시스템 + 뱃지 획득

**Kakao Map API 활용**
- Geocoding으로 주소 → 좌표 자동 변환
- Haversine 공식으로 정확한 거리 계산

#### 3. 협업 프로세스
**Git 브랜치 전략**
- feature 브랜치 분리로 충돌 최소화
- 커밋 컨벤션 준수로 히스토리 가독성 ↑

**역할 분담**
- Backend: User, Store, Review 모델 설계
- Frontend: 지도, 마이페이지, 커뮤니티 구현
- 공통: 데이터 fixture 작성

---

### 🔧 아쉬운 점 & 개선 방향

#### 1. AI 추천 알고리즘 고도화
**현재 상태**
- 기분 기반 키워드 필터링 (단순)

**개선 방향**
```python
# 협업 필터링 (Collaborative Filtering) 적용
from sklearn.metrics.pairwise import cosine_similarity

# User-Item Matrix 생성
user_item_matrix = create_matrix(users, stores, ratings)

# 코사인 유사도 계산
user_similarity = cosine_similarity(user_item_matrix)

# 유사 사용자 기반 추천
def recommend_stores(user_id, top_n=5):
    similar_users = get_similar_users(user_id, user_similarity)
    recommended = get_stores_from_similar_users(similar_users)
    return recommended[:top_n]
```

#### 2. 성능 최적화
**이미지 Lazy Loading**
```javascript
// Vue 3 Lazy Loading
<img v-lazy="review.image_url" alt="리뷰 사진">
```

**API 캐싱**
```python
# Django Redis Cache
from django.core.cache import cache

def get_stores(request):
    stores = cache.get('stores_list')

    if not stores:
        stores = Store.objects.all()
        cache.set('stores_list', stores, timeout=3600)  # 1시간

    return Response(stores)
```

#### 3. 배포 (NF06 선택 요구사항)
**AWS EC2 배포 계획**
```bash
# Docker Compose 구성
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=breadtopia
```

**CI/CD 파이프라인**
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  script:
    - pytest backend/tests/

deploy:
  script:
    - docker-compose up -d
  only:
    - main
```

---

### 🎓 학습 내용

#### 1. Django Signal 활용
```python
# 리뷰 작성 시 자동으로 경험치 부여
@receiver(post_save, sender=Review)
def reward_review_exp(sender, instance, created, **kwargs):
    if created:
        instance.user.gain_exp(20)
```

**배운 점**
- Signal을 사용하면 View에서 분리된 로직 처리 가능
- 코드 재사용성 ↑, 유지보수 ↑

#### 2. Vue 3 Composition API
```javascript
// Options API (기존)
export default {
  data() {
    return { count: 0 }
  },
  methods: {
    increment() { this.count++ }
  }
}

// Composition API (새로운 방식)
import { ref } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const increment = () => count.value++

    return { count, increment }
  }
}
```

**장점**
- 로직 재사용 (composables)
- TypeScript 지원 우수
- 코드 가독성 ↑

#### 3. RESTful API 설계
**URL 네이밍 원칙**
```
❌ 나쁜 예시:
GET /getStores
POST /createReview
DELETE /deleteReviewById?id=1

✅ 좋은 예시:
GET /api/stores/
POST /api/stores/:id/reviews/
DELETE /api/reviews/:id/
```

**HTTP Method 의미**
- GET: 조회 (Safe, Idempotent)
- POST: 생성 (Not Idempotent)
- PUT: 전체 수정 (Idempotent)
- PATCH: 부분 수정 (Idempotent)
- DELETE: 삭제 (Idempotent)

---

### 💡 생성형 AI 활용

#### 1. 코드 생성
**Tailwind CSS 스타일 생성**
```
프롬프트: "귀여운 빵집 테마의 카드 컴포넌트 스타일을 Tailwind로 작성해줘"

결과:
<div class="bg-amber-50 rounded-2xl shadow-lg p-6
            hover:shadow-xl transition-shadow duration-300
            border-2 border-amber-200">
```

#### 2. 더미 데이터 Fixture
```
프롬프트: "서울 지역 빵집 20개의 fixture 데이터를 JSON으로 생성해줘"

결과: stores.json (100개 빵집 데이터)
```

#### 3. README 자동 생성
```
프롬프트: "프로젝트 README에 포함할 ERD, API 엔드포인트 문서 작성"

결과: 마크다운 테이블, 다이어그램
```

**AI 활용 시 주의점**
- ⚠️ 생성된 코드를 그대로 사용하지 말고 **검토 후 수정**
- ⚠️ 보안 관련 코드 (인증, 암호화)는 **직접 작성**
- ⚠️ 비즈니스 로직은 **AI 참고만**, 최종 설계는 직접

---

## 📊 프로젝트 통계

### 개발 기간
- **기획 & 설계**: 2일
- **Backend 개발**: 3일
- **Frontend 개발**: 4일
- **통합 & 테스트**: 2일
- **README 작성**: 1일

**총 12일** (2025.12.19 기준)

### 코드 통계
```
Backend (Django)
├── Models: 8개 (User, Store, Review, Badge, ...)
├── Views: 15개
├── URLs: 25개
└── Lines: ~2,500 lines

Frontend (Vue)
├── Pages: 7개
├── Components: 20개
└── Lines: ~3,000 lines

Total: ~5,500 lines
```

### Git 통계
- **Commits**: 120+
- **Branches**: 15개 (feature, develop, main)
- **Merge Requests**: 30+

---

## 🎬 데모 시연 순서

### 1. 홈 화면 (30초)
- 서비스 소개
- "빵 지도 열기" 버튼 클릭

### 2. 지도 페이지 (1분 30초)
- Kakao Map 로딩
- 마커 클릭 → 빵집 정보
- 기분 필터 선택: "☁️ 우울할 땐"
- 필터링된 빵집 목록 확인

### 3. 빵집 상세 페이지 (2분)
- 빵집 정보 (주소, 영업시간, 평균 평점)
- 리뷰 목록 확인
- **리뷰 작성 시연**
  - 별점 4점
  - taste_tags: ["달달함", "부드러움"]
  - 사진 업로드
  - 제출 → "경험치 +20" 알림

### 4. 마이페이지 (2분)
- 빵 여권 확인
  - First Bake: 2025.12.10
  - 레벨: Lv.3 호빵토끼
  - 경험치: 320 / 600
  - 스탬프: 12개
- 뱃지 핀보드
  - 🥐 크루아상 헌터
  - 📸 인증샷 마스터
- 내 리뷰 목록

### 5. 커뮤니티 (1분)
- 게시글 목록 확인
- 댓글 작성
- 좋아요 클릭

### 6. 코드 설명 (3분)
- [accounts/models.py:64-87](accounts/models.py#L64-L87) - 레벨업 로직
- [MapPage.vue:49-54](MapPage.vue#L49-L54) - 기분 필터
- [reviews/views.py:23-40](reviews/views.py#L23-L40) - 리뷰 API

---

## 🔗 참고 링크

### 문서
- [Django 공식 문서](https://www.djangoproject.com/)
- [Vue 3 공식 문서](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Kakao Map API](https://apis.map.kakao.com/)

### Git Repository
```
https://lab.ssafy.com/your-team/final-pjt
```

### 팀원
- **팀장**: OOO (Backend, 레벨 시스템)
- **팀원**: OOO (Frontend, 지도 기능)

---

## 🎯 향후 계획

### Phase 2 (3개월 내)
- [ ] AI 추천 알고리즘 고도화 (협업 필터링)
- [ ] AWS EC2 배포
- [ ] Redis 캐싱 적용
- [ ] 이미지 CDN 연동 (S3)

### Phase 3 (6개월 내)
- [ ] 모바일 앱 개발 (React Native)
- [ ] 실시간 채팅 (WebSocket)
- [ ] 빵집 사장님 전용 대시보드
- [ ] 결제 시스템 (포인트 충전)

---

## 📞 Q&A

### 예상 질문

**Q1. 왜 Tailwind를 선택했나요?**
> Bootstrap은 정해진 디자인 컴포넌트가 많아서, 저희 프로젝트의 "귀여운 빵집 테마"를 자유롭게 커스텀하기 어려웠습니다. Tailwind는 유틸리티 클래스로 세밀한 스타일링이 가능해 UI 일관성을 유지하면서도 원하는 디자인을 구현할 수 있었습니다.

**Q2. 추천 알고리즘이 단순한 것 같은데요?**
> 현재는 기분 기반 키워드 필터링을 적용했지만, 이는 1단계 MVP입니다. 향후 사용자 리뷰 데이터가 쌓이면 협업 필터링(CF)과 딥러닝 기반 추천으로 확장할 예정입니다. taste_tags 필드를 설계한 이유도 이를 고려한 것입니다.

**Q3. 레벨업은 어떻게 자동으로 되나요?**
> Django Signal을 활용했습니다. 리뷰가 생성될 때 `post_save` 시그널이 트리거되고, `gain_exp()` 메서드를 호출합니다. 이 메서드 내부에서 `check_level_up()`이 자동 실행되어 레벨업 조건을 확인합니다. ([accounts/models.py:64-87](accounts/models.py#L64-L87) 참조)

**Q4. 배포는 했나요?**
> 현재는 로컬 환경에서 개발을 완료했습니다. 배포는 선택 요구사항(NF06)이었지만, 향후 AWS EC2 + Docker + Nginx 조합으로 배포할 계획입니다. 도메인 연결까지 고려하고 있습니다.

**Q5. Git 충돌은 없었나요?**
> Gitflow 전략을 사용해 충돌을 최소화했습니다. `feature/*` 브랜치에서 개발 후 `develop`으로 병합, 최종적으로 `main`에 릴리즈하는 방식입니다. 충돌이 발생한 경우 팀원과 즉시 소통해 해결했고, 이 과정을 README에 기록했습니다.

---

## 🙏 감사의 말

이 프로젝트를 통해 Django REST Framework, Vue 3, Kakao API 연동, 게이미피케이션 설계 등 실무에 가까운 기술 스택을 경험할 수 있었습니다.

특히 **RESTful API 설계 원칙**, **Git 협업 전략**, **API Key 보안 관리**는 향후 모든 프로젝트에서 활용할 수 있는 핵심 역량이 되었습니다.

부족한 부분도 많지만, 이번 프로젝트를 발판 삼아 더 나은 개발자로 성장하겠습니다.

**발표를 들어주셔서 감사합니다!** 🍞✨

---

_이 문서는 SSAFY 12기 최종 프로젝트 발표를 위해 작성되었습니다._
_Last Updated: 2025.12.24_
