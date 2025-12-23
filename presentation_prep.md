# 🎯 Breadtopia (빵토피아) - 10분 발표 구성안

## 📋 발표 시간 배분 (총 10분)

| 순서 | 섹션 | 시간 | 내용 |
|------|------|------|------|
| 1 | 서비스 소개 | 1분 | 프로젝트 배경, 페르소나, 핵심 컨셉 |
| 2 | 기술 스택 & 아키텍처 | 1분 30초 | 기술 선택 이유, ERD, 시스템 구조 |
| 3 | 핵심 기능 시연 (메인) | 5분 | 페이지별 시연 + 코드 설명 |
| 4 | 추천 알고리즘 & 게이미피케이션 | 1분 30초 | AI 추천 로직, 레벨 시스템 |
| 5 | 회고 & QA | 1분 | 느낀 점, 개선점 |

---

## 📝 상세 발표 스크립트

### 1️⃣ 서비스 소개 (1분)

**화면**: HomeView 메인 페이지

```
안녕하세요. 저희는 20~30대 여성과 남성을 타겟으로 한
빵집 탐방 소셜 플랫폼 'Breadtopia(빵토피아)'를 개발했습니다.

[배경]
- 요즘 젊은 세대들 사이에서 '빵지순례'가 트렌드입니다
- 하지만 빵집 정보가 파편화되어 있고, 개인 취향 맞춤 추천이 부족했습니다

[페르소나]
- 20~30대 여성/남성 (빵덕후, SNS 활동 적극층)
- "귀엽고 포근한 느낌"을 선호하는 감성 소비자

[핵심 컨셉]
- 🐶 바구니 속 강아지 빵처럼 귀여운 UI
- 🗺️ 지도 기반 빵집 탐색
- 🎮 게이미피케이션 (레벨업, 뱃지 시스템)
```

**시연**: HomeView 스크롤 → "빵 지도 열기" 버튼 클릭

---

### 2️⃣ 기술 스택 & 아키텍처 (1분 30초)

**화면**: ERD 다이어그램 또는 기술 스택 슬라이드

```
[기술 스택]
Backend:
- Django REST Framework (RESTful API 설계)
- PostgreSQL / SQLite (개발 환경)
- Python-dotenv (API Key 보안 관리)

Frontend:
- Vue 3 (Composition API)
- Tailwind CSS (귀여운 UI 구현)
- Axios (비동기 통신)
- Kakao Map API (지도 기능)

[ERD 설명]
1. User 모델: 레벨, 경험치, 뱃지 관계
2. Store 모델: 빵집 정보, 평균 평점
3. Review 모델: 리뷰, taste_tags (취향 분석용)
4. Community 모델: 게시글, 댓글
5. Badge 모델: 뱃지 획득 시스템
```

**참고 코드 위치**:
- accounts/models.py:24-119 - User, Badge 모델
- stores/models.py:4-48 - Store, Product, Keyword 모델
- reviews/models.py:5-72 - Review, Comment 모델

---

### 3️⃣ 핵심 기능 시연 (5분) ⭐ 가장 중요

#### 3-1. 홈 화면 → 지도 페이지 (1분)

**화면**: HomeView.vue → MapPage.vue

```
[시연]
1. 메인 화면에서 "빵 지도 열기" 클릭
2. Kakao Map API로 현재 위치 기반 빵집 마커 표시
3. 좌측 리스트에서 빵집 정보 확인

[핵심 코드 설명]
📍 MapPage.vue:80-99 - Kakao Geocoder를 통한 좌표 자동 변환
📍 MapPage.vue:49-54 - 기분 기반 키워드 필터 (☁️ 우울할 땐 → "달달한")

주요 함수:
- fillMissingCoordinates(): 주소 → 좌표 변환
- getDistanceFromLatLonInKm(): 거리 계산 (Haversine 공식)
```

**코드 위치**:
- MapPage.vue:80-99 - Geocoding 로직
- MapPage.vue:49-54 - 기분 필터

---

#### 3-2. 빵집 상세 페이지 (1분 30초)

**화면**: DetailView.vue

```
[시연]
1. 지도에서 마커 클릭 → 상세 페이지 이동
2. 빵집 정보 (주소, 영업시간, 평균 평점)
3. 리뷰 작성 기능 (사진 업로드, 별점, taste_tags)
4. 즐겨찾기 버튼 (♥)

[핵심 코드 설명]
Backend:
📍 reviews/views.py:23-40 - ReviewListCreateView (리뷰 CRUD)
📍 reviews/models.py:23-25 - taste_tags 필드 (취향 분석용)

Frontend:
- Axios POST 요청으로 리뷰 생성
- FormData로 이미지 업로드
```

**코드 위치**:
- reviews/views.py:23-40 - 리뷰 생성 API
- reviews/models.py:23-25 - taste_tags 필드

---

#### 3-3. 마이페이지 - 빵 여권 & 레벨 시스템 (1분 30초)

**화면**: MyPage.vue

```
[시연]
1. 마이페이지 진입 → 캐릭터 레벨 표시 (예: Lv.3 호빵토끼)
2. 빵 여권 (Bread Passport):
   - First Bake (가입일)
   - 빵력 (경험치)
   - 스탬프 개수
3. 뱃지 핀보드 (Badge PinBoard)
4. 내가 쓴 리뷰, 즐겨찾기한 빵집

[핵심 코드 설명]
Backend - 레벨업 로직:
📍 accounts/models.py:64-87 - gain_exp(), check_level_up() 메서드
📍 accounts/models.py:47-58 - LEVEL_SYSTEM 딕셔너리 (10단계)

동작 방식:
1. 리뷰 작성 → Signal로 경험치 +20
2. check_level_up()이 자동 호출
3. 경험치가 threshold 초과 시 레벨업 + 칭호 변경
   예: 100exp → Lv.2 "식빵햄찌"

Frontend:
- get_passport_stats() API로 통계 데이터 조회
```

**코드 위치**:
- accounts/models.py:64-87 - 레벨업 로직
- accounts/models.py:47-58 - 레벨 시스템 정의
- accounts/models.py:90-108 - 빵 여권 데이터

---

#### 3-4. 커뮤니티 기능 (1분)

**화면**: Community 페이지

```
[시연]
1. 게시글 작성 (카테고리: 빵집 추천, 자유, 질문)
2. 이미지 업로드
3. 댓글 & 대댓글 기능
4. 좋아요 (♥)

[핵심 코드 설명]
Backend:
📍 community/models.py:12 - ImageField로 이미지 저장
📍 community/models.py:30 - parent 필드 (대댓글)

RESTful 원칙:
- POST /community/posts/ (게시글 생성)
- POST /community/posts/<pk>/like/ (좋아요 토글)
```

**코드 위치**:
- community/models.py:4-36 - Post, PostComment 모델

---

### 4️⃣ 추천 알고리즘 & 게이미피케이션 (1분 30초)

**화면**: 추천 로직 다이어그램 또는 코드

```
[F01 요구사항: 사용자 추천]

1. 기분 기반 추천
   - MapPage.vue:49-54 - 기분 선택 → 키워드 필터
   - 예: "☁️ 우울할 땐" → taste_tags에 "달달한" 포함된 리뷰의 빵집 추천

2. 취향 분석 추천 (개발 중)
   - 사용자가 작성한 리뷰의 taste_tags 수집
   - 예: "달달함" 80%, "바삭함" 20% → 유사 빵집 추천

3. 게이미피케이션
   - 리뷰 작성 → +20 exp
   - 레벨업 → 캐릭터 칭호 변경 (아기빵쥐 → 식빵햄찌 → ... → 황금밀 유니콘)
   - 뱃지 획득 (예: "크루아상 헌터" - 크루아상 리뷰 10개 작성)

[핵심 로직]
📍 accounts/signals.py - Signal로 경험치 자동 부여
📍 accounts/models.py:64-71 - gain_exp() 메서드
```

**코드 위치**:
- accounts/signals.py - Signal 파일
- MapPage.vue:49-54 - 기분 필터

---

### 5️⃣ 회고 & QA (1분)

```
[잘한 점]
✅ RESTful API 설계 준수 (HTTP Method, Status Code)
✅ Git 브랜치 전략 (Gitflow 사용)
✅ API Key 보안 관리 (.env, python-dotenv)
✅ 반응형 UI (Tailwind CSS)

[아쉬운 점 & 개선 방향]
- AI 추천 알고리즘 고도화 (협업 필터링, CF 적용)
- 배포 (AWS EC2, Docker)
- 성능 최적화 (이미지 lazy loading, 캐싱)

[생성형 AI 활용]
- Tailwind CSS 스타일 생성
- 더미 데이터 fixture 작성
- README 문서 자동 생성
```

---

## 🎬 발표 팁

### 1. 시연 준비물
- 로컬 서버 미리 실행 (`python manage.py runserver`, `npm run dev`)
- 테스트 계정 로그인 상태 유지
- 브라우저 탭 미리 열어두기:
  - 탭1: HomeView
  - 탭2: MapPage
  - 탭3: DetailView (특정 빵집)
  - 탭4: MyPage
  - 탭5: Community

### 2. 코드 설명 시 보여줄 파일

| 기능 | 파일 경로 | 라인 |
|------|-----------|------|
| 레벨업 로직 | accounts/models.py | 64-87 |
| 리뷰 API | reviews/views.py | 23-40 |
| 지도 좌표 변환 | MapPage.vue | 80-99 |
| taste_tags | reviews/models.py | 23-25 |

### 3. 발표 시 강조할 점

#### 명세서 필수 요구사항 충족
- ✅ F01 (사용자 추천): 기분 필터, 취향 분석
- ✅ F02 (API 활용): Kakao Map API
- ✅ NF01 (Git 활용): Gitflow 브랜치 전략
- ✅ NF02 (API Key 관리): .env + python-dotenv
- ✅ NF04 (페이지 다양성): 5개 이상 URL (Home, Map, Detail, MyPage, Community, Search, Region)
- ✅ NF05 (RESTful 원칙): HTTP Method, Status Code 활용

#### 차별화 포인트
- 🎨 귀여운 UI/UX (20~30대 타겟 명확)
- 🎮 게이미피케이션 (레벨, 뱃지)
- 🧠 취향 분석 (taste_tags)

### 4. 예상 질문 대비

**Q1. 추천 알고리즘은 어떻게 구현했나요?**
→ A: 현재는 기분 기반 키워드 필터링을 적용했고, 향후 협업 필터링(CF)으로 확장 예정입니다.

**Q2. 레벨업은 어떻게 자동으로 되나요?**
→ A: Django Signal을 활용해 리뷰 생성 시 `post_save` 시그널이 트리거되고, `gain_exp()` 메서드를 호출합니다.

**Q3. 배포는 했나요?**
→ A: 로컬 환경에서 개발 완료했으며, 향후 AWS EC2 + Docker로 배포 예정입니다.

---

## 📌 발표 슬라이드 구성 (선택사항)

1. **표지**: 프로젝트명, 팀원, 날짜
2. **서비스 소개**: 배경, 페르소나, 컨셉
3. **기술 스택**: 로고 이미지
4. **ERD**: 모델 관계도
5. **화면 구성**: 각 페이지 스크린샷
6. **핵심 코드**: 레벨업 로직, 리뷰 API
7. **회고**: 잘한 점, 아쉬운 점

---

## 📂 프로젝트 구조

```
final-pjt/
├── backend/
│   ├── accounts/        # 사용자, 레벨, 뱃지 관리
│   ├── stores/          # 빵집 정보
│   ├── reviews/         # 리뷰, 댓글
│   ├── community/       # 커뮤니티 게시판
│   └── core/            # 프로젝트 설정
└── frontend/
    └── breadmap-project/
        ├── src/
        │   ├── Views/          # 페이지 컴포넌트
        │   ├── components/     # 재사용 컴포넌트
        │   ├── stores/         # Pinia 상태관리
        │   └── api/            # Axios 설정
        └── public/
```

---

## 🚀 실행 방법

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/*.json
python manage.py runserver
```

### Frontend
```bash
cd frontend/breadmap-project
npm install
npm run dev
```

---

이 문서를 바탕으로 발표 준비를 진행하시면 됩니다! 발표 화이팅! 🎉
