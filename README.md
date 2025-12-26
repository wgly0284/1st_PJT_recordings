# 🍞 Breadtopia (빵토피아)

> **빵지순례의 새로운 시작, 당신만의 빵 여행을 시작하세요**

AI 기반 빵집 추천 플랫폼 | SSAFY 12기 최종 프로젝트

[![Django](https://img.shields.io/badge/Django-5.2.9-092E20?logo=django)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.5.25-4FC08D?logo=vue.js)](https://vuejs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai)](https://openai.com/)

---

## 📌 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [핵심 기능](#-핵심-기능)
3. [기술 스택](#-기술-스택)
4. [시스템 아키텍처](#-시스템-아키텍처)
5. [ERD](#-erd)
6. [프로젝트 구조](#-프로젝트-구조)
7. [설치 및 실행](#-설치-및-실행)
8. [API 명세](#-api-명세)
9. [주요 화면](#-주요-화면)
10. [팀원 소개](#-팀원-소개)

---

## 🎯 프로젝트 소개

### 개요

**Breadtopia(빵토피아)**는 빵지순례를 즐기는 사용자들을 위한 **AI 기반 빵집 추천 플랫폼**입니다.
지도 기반 탐색, 게이미피케이션, 커뮤니티 기능을 통해 빵집 탐방을 더욱 재미있고 편리하게 만들어줍니다.

### 핵심 가치

- 🤖 **AI 기반 3대 서비스**: 오늘의 빵집 추천, 웰시코기 챗봇, 리뷰 요약
- 🗺️ **지도 기반 탐색**: Kakao Map API를 활용한 직관적인 빵집 찾기
- 🎮 **게이미피케이션**: 레벨, 뱃지, 빵 여권으로 탐방 기록을 재미있게
- 🤝 **소셜 커뮤니티**: 빵덕후들의 정보 공유 및 소통 공간
- 🐶 **귀여운 UI/UX**: 바구니 속 강아지 빵 컨셉의 따뜻한 디자인

### 타겟 사용자

- 20~30대 빵지순례 애호가
- SNS 활동이 활발한 감성 소비자
- 새로운 빵집을 탐방하고 기록하는 것을 즐기는 사용자
- 귀엽고 포근한 느낌을 선호하는 사용자

---

## 🚀 핵심 기능

### 1. 🤖 AI 기반 3대 서비스

#### 1-1. 오늘의 빵집 추천
- 사용자의 **빵 취향 선호 키워드** 기반 추천
- **하루 한 개씩** 개인 맞춤형 빵집 추천
- HomeView에서 카드 형태로 표시
- 매일 자정(00:00)에 추천 갱신

**주요 코드**: [`frontend/src/Views/HomeView.vue`](frontend/breadmap-project/src/Views/HomeView.vue)

#### 1-2. 웰시코기 챗봇
- 우측 하단에 **플로팅 버튼** 형태로 배치
- 빵집 관련 질문에 **실시간 AI 응답**
- OpenAI API 활용
- 빵집 영업시간, 추천 메뉴, 위치 안내 등 제공

**주요 코드**: [`frontend/src/components/BakeryChatbot.vue`](frontend/breadmap-project/src/components/BakeryChatbot.vue)

#### 1-3. AI 리뷰 요약
- 빵집 상세 페이지에서 **수십 개 리뷰를 AI가 요약**
- 핵심 키워드, 장점/단점, 추천 메뉴 등을 3-5줄로 정리
- LangChain + OpenAI API 활용

**주요 코드**: [`backend/stores/views.py`](backend/stores/views.py) - `ReviewSummaryView`

---

### 2. 🗺️ 지도 기반 빵집 탐색

- **Kakao Map API** 기반 실시간 지도
- 현재 위치 중심 빵집 마커 표시
- **기분 필터**: "우울할 땐", "행복할 땐" 등 감정 기반 추천
- 거리순 정렬
- 마커 클릭 시 빵집 상세 페이지 이동

**주요 코드**: [`frontend/src/Views/MapPage.vue`](frontend/breadmap-project/src/Views/MapPage.vue)

---

### 3. 🎮 게이미피케이션 시스템

#### 3-1. 레벨 시스템 (10단계)
| 레벨 | 칭호 | 필요 경험치 |
|------|------|------------|
| 1 | 아기빵쥐 | 0 |
| 2 | 식빵햄찌 | 100 |
| 3 | 호빵토끼 | 300 |
| 4 | 모닝코기 | 600 |
| 5 | 크루아상여우 | 1000 |
| 6 | 브리오슈곰 | 1500 |
| 7 | 사워도우울프 | 2200 |
| 8 | 초코표범 | 3000 |
| 9 | 바게트호크 | 4000 |
| 10 | 황금밀 유니콘 | 5500 |

#### 3-2. 경험치 획득 방법
- 리뷰 작성: **+20 EXP**
- 커뮤니티 게시글 작성: **+10 EXP**
- 즐겨찾기 추가: **+5 EXP**

#### 3-3. 뱃지 시스템
- **행동 기반**: 크루아상 헌터, 인증샷 마스터, 빵지순례왕
- **지역 기반**: 서울 빵지순례자, 부산 빵 탐험가
- **이벤트**: 새벽빵 요정, 황금 바게트

#### 3-4. 빵 여권 (Bread Passport)
- **First Bake**: 가입일
- **빵력**: 현재 경험치
- **스탬프**: 방문 인증 개수
- **획득 뱃지**: 뱃지 핀보드

**주요 코드**: [`backend/accounts/models.py`](backend/accounts/models.py) - `User.gain_exp()`, `User.check_level_up()`

---

### 4. 💬 커뮤니티 기능

- **게시글 작성**: 빵집 추천, 자유, 질문 카테고리
- **이미지 업로드**: 빵집 인증샷, 빵 사진 공유
- **댓글 & 대댓글**: 계층형 댓글 시스템
- **좋아요**: 게시글 및 댓글 좋아요
- **핫 게시글**: 좋아요 많은 인기 게시글 표시

**주요 코드**:
- [`backend/community/models.py`](backend/community/models.py)
- [`frontend/src/components/community/CommunityMain.vue`](frontend/breadmap-project/src/components/community/CommunityMain.vue)

---

### 5. 📝 리뷰 시스템

- **별점**: 1~5점
- **맛 태그**: 달달함, 바삭함, 촉촉함, 고소함 등
- **메뉴 태그**: 소금빵, 크루아상, 바게트 등
- **사진 업로드**: 다중 이미지 지원
- **댓글**: 리뷰에 대한 의견 공유

**주요 코드**: [`backend/reviews/models.py`](backend/reviews/models.py)

---

### 6. 🔍 검색 및 필터

- **빵집 이름 검색**
- **지역별 필터**: 서울, 경기, 부산, 대구 등
- **카테고리 필터**: 베이커리, 디저트 카페, 프랜차이즈
- **태그 검색**: #데이트 #분위기좋은 #뷰맛집

**주요 코드**: [`frontend/src/Views/SearchResultView.vue`](frontend/breadmap-project/src/Views/SearchResultView.vue)

---

## 🛠 기술 스택

### Backend

| 기술 | 버전 | 사용 목적 |
|------|------|-----------|
| **Python** | 3.11+ | 백엔드 언어 |
| **Django** | 5.2.9 | RESTful API 서버 |
| **Django REST Framework** | 3.16.1 | API 직렬화, 인증 |
| **django-allauth** | 65.13.1 | 소셜 로그인 (확장 가능) |
| **django-cors-headers** | 4.9.0 | CORS 처리 |
| **Pillow** | 12.0.0 | 이미지 처리 |
| **python-dotenv** | 1.2.1 | 환경 변수 관리 |
| **SQLite** | - | 개발 환경 DB |

#### AI/LLM
| 기술 | 버전 | 사용 목적 |
|------|------|-----------|
| **OpenAI API** | 2.14.0 | AI 챗봇, 리뷰 요약 |
| **LangChain** | 1.2.0 | LLM 파이프라인 |
| **LangGraph** | 1.0.5 | AI 에이전트 워크플로우 |

### Frontend

| 기술 | 버전 | 사용 목적 |
|------|------|-----------|
| **Vue.js** | 3.5.25 | Composition API, 반응형 UI |
| **Vue Router** | 4.6.4 | SPA 라우팅 |
| **Pinia** | 3.0.4 | 상태 관리 |
| **Axios** | 1.13.2 | HTTP 통신 |
| **Bootstrap** | 5.3.8 | UI 컴포넌트 |
| **Lucide Vue** | 0.562.0 | 아이콘 라이브러리 |
| **Vite** | 7.2.4 | 빌드 도구 |

### API

| API | 사용 목적 |
|-----|-----------|
| **Kakao Map API** | 지도 표시, 마커, Geocoding |
| **공공데이터포털 API** | 전국 제과점 정보 수집 |
| **OpenAI API** | AI 챗봇, 리뷰 요약 |

### 개발 도구

- **Git**: 버전 관리 (Gitflow 전략)
- **VS Code**: 통합 개발 환경
- **Postman**: API 테스트

---

## 🏗 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        Client (Browser)                      │
│                     Vue 3 + Vite + Pinia                     │
└────────────────────────┬────────────────────────────────────┘
                         │ Axios HTTP Request
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Django REST API Server                    │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Accounts │  │  Stores  │  │ Reviews  │  │Community │   │
│  │   App    │  │   App    │  │   App    │  │   App    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
└────────────┬────────────────────────────────┬───────────────┘
             │                                 │
             ↓                                 ↓
┌─────────────────────┐              ┌─────────────────────┐
│   SQLite Database   │              │   External APIs     │
│                     │              │                     │
│  - User             │              │  - Kakao Map API    │
│  - Store            │              │  - OpenAI API       │
│  - Review           │              │  - 공공데이터포털    │
│  - Post             │              │                     │
│  - Badge            │              └─────────────────────┘
└─────────────────────┘
```

---

## 📊 ERD

### 핵심 모델 관계

```
┌──────────────┐
│     User     │
│ (계정 정보)   │
│──────────────│
│ id           │◄──────┐
│ email        │       │
│ nickname     │       │ 1:N
│ level        │       │
│ exp          │       │
│ level_title  │       │
│ badges       │◄──┐   │
└──────────────┘   │   │
        │          │   │
        │ N:M      │   │
        │          │   │
┌───────▼──────┐   │   │
│    Badge     │   │   │
│  (뱃지 정보)  │   │   │
│──────────────│   │   │
│ id           │   │   │
│ name         │   │   │
│ category     │   │   │
└──────────────┘   │   │
                   │   │
        ┌──────────┘   │
        │              │
┌───────▼──────┐       │
│  UserBadge   │       │
│  (획득 기록)  │       │
│──────────────│       │
│ user_id      │       │
│ badge_id     │       │
│ acquired_at  │       │
└──────────────┘       │
                       │
┌──────────────┐       │
│    Store     │       │
│  (빵집 정보)  │       │
│──────────────│       │
│ id           │◄──────┤
│ name         │       │
│ address      │       │ 1:N
│ latitude     │       │
│ longitude    │       │
│ avg_rating   │       │
└──────────────┘       │
        │              │
        │ 1:N          │
        │              │
┌───────▼──────┐       │
│   Product    │       │
│  (빵 상품)    │       │
│──────────────│       │
│ id           │       │
│ store_id     │       │
│ name         │       │
│ price        │       │
└──────────────┘       │
                       │
┌──────────────┐       │
│    Review    │◄──────┤
│  (리뷰 정보)  │       │
│──────────────│       │
│ id           │       │
│ user_id      │       │ 1:N
│ store_id     │       │
│ rating       │       │
│ content      │       │
│ taste_tags   │       │
│ menu_items   │       │
└──────────────┘       │
        │              │
        │ 1:N          │
        │              │
┌───────▼──────┐       │
│   Comment    │       │
│ (리뷰 댓글)   │       │
│──────────────│       │
│ id           │       │
│ review_id    │       │
│ user_id      │       │
│ content      │       │
│ parent_id    │       │
└──────────────┘       │
                       │
┌──────────────┐       │
│     Post     │◄──────┘
│ (커뮤니티)    │
│──────────────│
│ id           │
│ author_id    │
│ title        │
│ content      │
│ category     │
│ image        │
└──────────────┘
        │
        │ 1:N
        │
┌───────▼──────┐
│ PostComment  │
│ (게시글 댓글) │
│──────────────│
│ id           │
│ post_id      │
│ user_id      │
│ content      │
│ parent_id    │
└──────────────┘
```

### 주요 모델 설명

#### 1. User (사용자)
```python
# backend/accounts/models.py
- email: 이메일 (로그인 ID)
- nickname: 닉네임
- level: 현재 레벨 (1~10)
- exp: 경험치
- level_title: 레벨 칭호 (예: 아기빵쥐, 황금밀 유니콘)
- badges: 획득 뱃지 (Many-to-Many)
- follows: 팔로우 관계 (자기 참조)
```

#### 2. Store (빵집)
```python
# backend/stores/models.py
- name: 빵집 이름
- address: 주소
- latitude, longitude: 위도, 경도 (Kakao Map)
- category: 카테고리 (베이커리, 카페 등)
- avg_rating: 평균 평점
- popular_menu_items: 대표 메뉴 (콤마 구분)
```

#### 3. Review (리뷰)
```python
# backend/reviews/models.py
- user: 작성자
- store: 빵집
- rating: 평점 (1~5)
- content: 내용
- taste_tags: 맛 태그 (예: "달달함,바삭함")
- menu_items: 먹은 메뉴 (예: "소금빵,크루아상")
- photo_urls: 사진 URL
- like_users: 좋아요 누른 사용자 (Many-to-Many)
```

#### 4. Badge (뱃지)
```python
# backend/accounts/models.py
- name: 뱃지 이름 (예: 크루아상 헌터)
- description: 설명
- category: 카테고리 (ACTION, REGION, EVENT)
- condition_threshold: 획득 조건 수치
```

#### 5. Post (커뮤니티 게시글)
```python
# backend/community/models.py
- author: 작성자
- title: 제목
- content: 내용
- category: 카테고리 (빵집 추천, 자유, 질문)
- image: 이미지 (ImageField)
- like_users: 좋아요 누른 사용자 (Many-to-Many)
```

---

## 📁 프로젝트 구조

```
final-pjt/
├── backend/                          # Django 백엔드
│   ├── accounts/                     # 사용자 계정 앱
│   │   ├── models.py                # User, Badge, UserBadge 모델
│   │   ├── views.py                 # 회원가입, 로그인, 프로필 API
│   │   ├── serializers.py           # User 직렬화
│   │   ├── signals.py               # 경험치 부여 Signal
│   │   └── urls.py                  # 계정 관련 URL
│   ├── stores/                       # 빵집 앱
│   │   ├── models.py                # Store, Product, Keyword 모델
│   │   ├── views.py                 # 빵집 CRUD, AI 요약 API
│   │   ├── serializers.py           # Store 직렬화
│   │   └── urls.py                  # 빵집 관련 URL
│   ├── reviews/                      # 리뷰 앱
│   │   ├── models.py                # Review, Comment 모델
│   │   ├── views.py                 # 리뷰 작성, 댓글 API
│   │   ├── serializers.py           # Review 직렬화
│   │   └── urls.py                  # 리뷰 관련 URL
│   ├── community/                    # 커뮤니티 앱
│   │   ├── models.py                # Post, PostComment 모델
│   │   ├── views.py                 # 게시글, 댓글 API
│   │   ├── serializers.py           # Post 직렬화
│   │   └── urls.py                  # 커뮤니티 관련 URL
│   ├── core/                         # Django 설정
│   │   ├── settings.py              # 환경 설정
│   │   ├── urls.py                  # 메인 URL 라우팅
│   │   └── wsgi.py                  # WSGI 설정
│   ├── data/                         # 공공데이터 JSON
│   ├── create_data.py               # 데이터 생성 스크립트
│   ├── manage.py                    # Django 관리 명령
│   ├── requirements.txt             # Python 패키지
│   └── db.sqlite3                   # SQLite 데이터베이스
│
├── frontend/                         # Vue 프론트엔드
│   └── breadmap-project/
│       ├── src/
│       │   ├── Views/               # 페이지 컴포넌트
│       │   │   ├── HomeView.vue    # 홈 (오늘의 빵집 추천)
│       │   │   ├── MapPage.vue     # 지도 페이지
│       │   │   ├── DetailView.vue  # 빵집 상세 (AI 리뷰 요약)
│       │   │   ├── UserProfile.vue # 마이페이지 (빵 여권)
│       │   │   ├── SearchResultView.vue  # 검색 결과
│       │   │   ├── RegionBakeryView.vue  # 지역별 빵집
│       │   │   └── BreadRoulette.vue     # 빵 룰렛
│       │   ├── AccountsViews/       # 계정 관련 뷰
│       │   │   ├── Login.vue       # 로그인
│       │   │   ├── SignUp.vue      # 회원가입
│       │   │   └── DailyBakeryCard.vue  # 오늘의 빵집 카드
│       │   ├── components/          # 재사용 컴포넌트
│       │   │   ├── BakeryChatbot.vue    # 웰시코기 챗봇
│       │   │   ├── community/      # 커뮤니티 컴포넌트
│       │   │   │   ├── CommunityMain.vue
│       │   │   │   ├── ChatterList.vue
│       │   │   │   ├── HotList.vue
│       │   │   │   └── NewChatter.vue
│       │   │   └── common/         # 공통 컴포넌트
│       │   │       ├── BakeryGrid.vue
│       │   │       └── BakeryChatbot.vue
│       │   ├── bakery/             # 빵집 관련 컴포넌트
│       │   │   ├── BakeryCard.vue
│       │   │   └── BakeryList.vue
│       │   ├── router/             # Vue Router 설정
│       │   │   └── index.js
│       │   ├── stores/             # Pinia Store
│       │   │   ├── auth.js        # 인증 상태
│       │   │   ├── bakery.js      # 빵집 상태
│       │   │   └── user.js        # 사용자 상태
│       │   ├── assets/             # 정적 파일
│       │   │   ├── images/        # 이미지
│       │   │   │   ├── logo.png
│       │   │   │   ├── 메인화면.png
│       │   │   │   ├── 바게트코기.png
│       │   │   │   ├── 식빵쥐.png
│       │   │   │   ├── 진열대.png
│       │   │   │   └── 진열대2.png
│       │   │   └── mascot/        # 마스코트 캐릭터
│       │   │       ├── 캐릭터 (1).png
│       │   │       ├── 캐릭터 (2).png
│       │   │       └── ... (9개)
│       │   ├── App.vue             # 루트 컴포넌트
│       │   └── main.js             # 앱 진입점
│       ├── public/                 # 정적 리소스
│       ├── index.html              # HTML 템플릿
│       ├── vite.config.js          # Vite 설정
│       ├── package.json            # npm 패키지
│       └── .env                    # 환경 변수
│
├── 명세서/                          # 프로젝트 명세서
├── GIT.md                           # Git 사용 가이드
└── README.md                        # 프로젝트 문서 (현재 파일)
```

---

## 🚀 설치 및 실행

### 사전 요구사항

- **Python**: 3.11 이상
- **Node.js**: 20.19.0 또는 22.12.0 이상
- **Git**

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd final-pjt
```

### 2. Backend 설정

#### 2-1. 가상환경 생성 및 활성화

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2-2. 패키지 설치

```bash
pip install -r requirements.txt
```

#### 2-3. 환경 변수 설정

`backend/.env` 파일 생성:

```bash
# Django Secret Key
SECRET_KEY=your-django-secret-key-here

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here

# Kakao API Key (선택)
KAKAO_API_KEY=your-kakao-api-key-here
```

#### 2-4. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2-5. 초기 데이터 로드 (선택)

```bash
# 공공데이터 기반 빵집 데이터 생성
python create_data.py

# 또는 Fixture 로드
python manage.py loaddata data/fixtures/*.json
```

#### 2-6. 슈퍼유저 생성

```bash
python manage.py createsuperuser
```

#### 2-7. 서버 실행

```bash
python manage.py runserver
```

**Backend URL**: `http://localhost:8000`

---

### 3. Frontend 설정

#### 3-1. 패키지 설치

```bash
cd frontend/breadmap-project
npm install
```

#### 3-2. 환경 변수 설정

`frontend/breadmap-project/.env` 파일 생성:

```bash
# Kakao Map API Key
VITE_KAKAO_MAP_API_KEY=your-kakao-map-api-key-here

# Backend API URL
VITE_API_BASE_URL=http://localhost:8000
```

#### 3-3. 개발 서버 실행

```bash
npm run dev
```

**Frontend URL**: `http://localhost:5173`

---

### 4. 빌드 (배포용)

#### Backend
```bash
python manage.py collectstatic
```

#### Frontend
```bash
npm run build
```

빌드된 파일은 `frontend/breadmap-project/dist/` 폴더에 생성됩니다.

---

## 📡 API 명세

### 인증 (Authentication)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| POST | `/api/accounts/signup/` | 회원가입 | ❌ |
| POST | `/api/accounts/login/` | 로그인 | ❌ |
| POST | `/api/accounts/logout/` | 로그아웃 | ✅ |
| GET | `/api/accounts/profile/` | 프로필 조회 | ✅ |
| PUT | `/api/accounts/profile/` | 프로필 수정 | ✅ |

### 빵집 (Stores)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/api/stores/` | 빵집 목록 조회 | ❌ |
| GET | `/api/stores/:id/` | 빵집 상세 조회 | ❌ |
| POST | `/api/stores/` | 빵집 생성 (관리자) | ✅ |
| PUT | `/api/stores/:id/` | 빵집 수정 | ✅ |
| DELETE | `/api/stores/:id/` | 빵집 삭제 | ✅ |
| POST | `/api/stores/:id/bookmark/` | 즐겨찾기 토글 | ✅ |
| POST | `/api/stores/:id/review-summary/` | AI 리뷰 요약 생성 | ✅ |

### 리뷰 (Reviews)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/api/stores/:id/reviews/` | 빵집 리뷰 목록 | ❌ |
| POST | `/api/stores/:id/reviews/` | 리뷰 작성 | ✅ |
| PUT | `/api/reviews/:id/` | 리뷰 수정 | ✅ |
| DELETE | `/api/reviews/:id/` | 리뷰 삭제 | ✅ |
| POST | `/api/reviews/:id/like/` | 리뷰 좋아요 토글 | ✅ |
| POST | `/api/reviews/:id/comments/` | 댓글 작성 | ✅ |

### 커뮤니티 (Community)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/api/community/posts/` | 게시글 목록 | ❌ |
| GET | `/api/community/posts/:id/` | 게시글 상세 | ❌ |
| POST | `/api/community/posts/` | 게시글 작성 | ✅ |
| PUT | `/api/community/posts/:id/` | 게시글 수정 | ✅ |
| DELETE | `/api/community/posts/:id/` | 게시글 삭제 | ✅ |
| POST | `/api/community/posts/:id/like/` | 게시글 좋아요 | ✅ |
| POST | `/api/community/posts/:id/comments/` | 댓글 작성 | ✅ |

### AI 기능 (AI Features)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/api/ai/daily-recommendation/` | 오늘의 빵집 추천 | ✅ |
| POST | `/api/ai/chatbot/` | 챗봇 대화 | ✅ |
| POST | `/api/stores/:id/ai-summary/` | AI 리뷰 요약 | ✅ |

### 게이미피케이션 (Gamification)

| Method | Endpoint | 설명 | 인증 필요 |
|--------|----------|------|-----------|
| GET | `/api/accounts/passport/` | 빵 여권 조회 | ✅ |
| GET | `/api/accounts/badges/` | 획득 뱃지 목록 | ✅ |
| GET | `/api/accounts/level/` | 레벨 정보 조회 | ✅ |

---

## 🎨 주요 화면

### 1. 홈 화면 (HomeView)
- 서비스 소개
- **오늘의 빵집 추천** (AI 기능)
- 빵 지도 진입 CTA

### 2. 지도 페이지 (MapPage)
- Kakao Map 기반 빵집 마커
- 기분 필터 (우울할 땐, 행복할 땐 등)
- 거리순 정렬
- 현재 위치 중심

### 3. 빵집 상세 (DetailView)
- 빵집 정보 (주소, 영업시간, 연락처)
- **AI 리뷰 요약** (핵심 키워드, 장단점)
- 평균 평점
- 리뷰 목록
- 리뷰 작성 폼 (별점, 맛 태그, 사진)
- 즐겨찾기 버튼

### 4. 마이페이지 (UserProfile)
- **빵 여권 (Bread Passport)**
  - First Bake (가입일)
  - 레벨 & 칭호
  - 경험치 바
  - 스탬프 개수
- **뱃지 핀보드**
- 내 리뷰 목록
- 즐겨찾기 빵집

### 5. 커뮤니티 (CommunityMain)
- 게시글 목록 (빵집 추천, 자유, 질문)
- 핫 게시글 (좋아요 많은 글)
- 게시글 작성 버튼
- 카테고리 필터

### 6. 검색 결과 (SearchResultView)
- 빵집 이름 검색
- 지역별 필터
- 카테고리 필터
- 검색 결과 그리드

### 7. 웰시코기 챗봇 (플로팅)
- 우측 하단 플로팅 버튼
- 채팅 창 (열림/닫힘)
- AI 실시간 응답
- 빵집 정보 안내

---

## 📈 데이터베이스 구축 전략

### 1. 공공데이터포털 활용

- **출처**: 공공데이터포털 (data.go.kr) - 전국 제과점 정보
- **수집 방법**: Open API를 통해 전국 제과점 데이터 조회 및 병합
- **데이터 규모**: 전국 단위 빵집 정보 (서울, 경기, 부산, 대구 등)

### 2. 경위도 필수 모델 설계

```python
class Store(models.Model):
    latitude = models.FloatField(null=True, blank=True)   # 필수 (지도 표시용)
    longitude = models.FloatField(null=True, blank=True)  # 필수
```

### 3. 데이터 정제 과정

```python
# create_data.py 핵심 로직
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

### 4. 지역별 데이터 보완

- **경위도 제공 지역**: 서울, 경기 중심 데이터는 공공데이터에서 직접 제공
- **경위도 누락 지역**: 지방 도시(부산, 대구, 광주 등)는 도로명 주소 기반 Geocoding
- **Geocoding 성공률**: 약 95% (유효한 도로명 주소 기준)

---

## 🎯 프로젝트 특징

### 1. AI 기반 차별화

- **LangChain + OpenAI API** 활용
- 3가지 AI 서비스로 사용자 경험 향상
- 실시간 챗봇 응답
- 리뷰 요약으로 정보 접근성 개선

### 2. 게이미피케이션

- 10단계 레벨 시스템
- 다양한 뱃지 획득
- 빵 여권으로 탐방 기록
- 경험치 획득으로 동기 부여

### 3. 지도 기반 UX

- Kakao Map API 실시간 연동
- Geocoding으로 주소 → 좌표 자동 변환
- 기분 필터로 감성 기반 추천
- 현재 위치 중심 탐색

### 4. 귀여운 디자인

- 빵토피아 전용 마스코트 캐릭터 (9개)
- 따뜻한 빵색 컬러 팔레트
- 바구니 속 강아지 빵 컨셉
- 직관적이고 친근한 UI

---

## 📝 주요 개발 내용

### Backend

#### 1. Django Signal을 활용한 경험치 자동 부여
```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from reviews.models import Review

@receiver(post_save, sender=Review)
def reward_review_exp(sender, instance, created, **kwargs):
    if created:
        instance.user.gain_exp(20)  # 리뷰 작성 시 20 EXP
```

#### 2. LangChain을 활용한 AI 리뷰 요약
```python
# stores/views.py
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class ReviewSummaryView(APIView):
    def post(self, request, store_id):
        reviews = Review.objects.filter(store_id=store_id)

        # 리뷰 텍스트 결합
        review_texts = "\n".join([r.content for r in reviews])

        # LangChain 프롬프트
        prompt = ChatPromptTemplate.from_template("""
        다음 리뷰들을 분석하여 핵심 키워드, 장점, 단점을 요약하세요:
        {reviews}
        """)

        # OpenAI API 호출
        llm = ChatOpenAI(model="gpt-4")
        summary = llm.invoke(prompt.format(reviews=review_texts))

        return Response({"summary": summary})
```

#### 3. Kakao Geocoding API 연동
```python
# create_data.py
import requests

def geocode_address(address):
    """도로명 주소를 경위도로 변환"""
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}

    response = requests.get(url, headers=headers, params=params)
    result = response.json()

    if result['documents']:
        return {
            'lat': float(result['documents'][0]['y']),
            'lng': float(result['documents'][0]['x'])
        }
    return None
```

### Frontend

#### 1. Pinia Store를 활용한 상태 관리
```javascript
// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),

  actions: {
    async login(email, password) {
      const response = await axios.post('/api/accounts/login/', {
        email, password
      })
      this.token = response.data.token
      this.user = response.data.user
      this.isAuthenticated = true
    }
  }
})
```

#### 2. Kakao Map API 초기화
```javascript
// Views/MapPage.vue
import { onMounted, ref } from 'vue'

const map = ref(null)

onMounted(() => {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.5665, 126.9780),
    level: 5
  }

  map.value = new kakao.maps.Map(container, options)

  // 현재 위치 가져오기
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude
      const locPosition = new kakao.maps.LatLng(lat, lng)

      map.value.setCenter(locPosition)
    })
  }
})
```

#### 3. AI 챗봇 컴포넌트
```vue
<!-- components/BakeryChatbot.vue -->
<template>
  <div class="chatbot-container">
    <button class="chatbot-trigger" @click="toggleChat">
      <img src="@/assets/images/바게트코기.png" alt="챗봇">
    </button>

    <div class="chat-window" v-if="isOpen">
      <div class="chat-messages">
        <div v-for="msg in messages" :key="msg.id" :class="msg.sender">
          {{ msg.text }}
        </div>
      </div>

      <input v-model="userInput" @keyup.enter="sendMessage">
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const messages = ref([])
const userInput = ref('')

const sendMessage = async () => {
  messages.value.push({ id: Date.now(), sender: 'user', text: userInput.value })

  const response = await axios.post('/api/ai/chatbot/', {
    message: userInput.value
  })

  messages.value.push({ id: Date.now() + 1, sender: 'bot', text: response.data.reply })
  userInput.value = ''
}
</script>
```

---

## 👥 팀원 소개

| 이름 | 역할 | 담당 업무 |
|------|------|-----------|
| **팀원 1** | Backend | User, Store 모델 설계, AI API 연동 |
| **팀원 2** | Frontend | 지도 페이지, 챗봇 컴포넌트 개발 |

---

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

---

## 🙏 감사의 말

이 프로젝트를 통해 Django REST Framework, Vue 3, LangChain, Kakao API 연동 등 실무에 가까운 기술 스택을 경험할 수 있었습니다.

특히 **RESTful API 설계 원칙**, **Git 협업 전략**, **AI/LLM 통합**은 향후 모든 프로젝트에서 활용할 수 있는 핵심 역량이 되었습니다.

---

**Last Updated**: 2025.12.26
**SSAFY 14기 최종 프로젝트**
**Breadtopia (빵토피아)** 🍞✨
