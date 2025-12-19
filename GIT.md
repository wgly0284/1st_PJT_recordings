# ✅ 브랜치 운영 원칙 (master + feature만)

## 1) 브랜치 종류

* **master**

  * 항상 실행 가능한 상태 유지
  * 제출/배포 가능한 최종본만 존재

* **feature/<기능-요약>**

  * 기능 개발 전용 브랜치
  * 예시:

    * `feature/auth-login`
    * `feature/todo-crud`
    * `feature/ui-navbar`

---

## 2) 작업 흐름 (무조건 이 순서)

1. `master` 최신화
2. `feature/*` 브랜치 생성 후 개발
3. 커밋은 규칙에 맞게 작은 단위로 작성
4. PR(MR) 생성 → **상대 1명 리뷰 필수**
5. PR 체크 통과 후 `master`로 머지
6. 머지 완료 후 해당 `feature/*` 브랜치 삭제

---

## 3) 절대 금지

* 🚫 `master`에 직접 작업 / 직접 커밋 / 직접 push 금지
* 🚫 PR 없이 `master`에 merge 금지

---

## ✅ 커밋 메시지 규칙 (Conventional Commits)

### 형식

```text
<type>(<scope>): <subject>
```

### type

* `feat` : 기능 추가
* `fix` : 버그 수정
* `refactor` : 리팩터링(동작 동일)
* `docs` : 문서 수정
* `style` : 포맷 변경(로직 변경 없음)
* `test` : 테스트 코드
* `chore` : 설정/환경/기타 작업

### scope

* 선택 사항
* 예: `auth`, `api`, `ui`, `router`, `store`

### subject 규칙

* 한 줄 요약, 명령형 사용
* 마침표(`.`) 사용 금지

### 예시

```text
feat(auth): 로그인 API 연결
fix(ui): 카드 정렬 깨짐 수정
refactor(api): axios 인스턴스 분리
docs(readme): 실행 방법 추가
chore(env): .env.example 추가
```

---

## ✅ PR(MR) 규칙 (2인 팀 기준)

* PR 제목은 커밋 메시지 형식과 동일하게 작성 권장

  * 예: `feat(search): 유튜브 검색 결과 렌더링`

### PR 체크리스트 (머지 전 필수)

* 로컬 실행 OK
* 핵심 기능 1회 이상 수동 테스트
* 충돌 해결 후 재실행 OK

### 머지 방식

* **Squash merge 권장** (히스토리 관리 용이)

---

## 🧩 Git 명령어 템플릿 (`switch` 버전)

### 1) 기능 시작

```bash
git switch master
git pull origin master

git switch -c feature/auth-login
```

### 2) 개발하면서 커밋

```bash
git add .
git commit -m "feat(auth): 로그인 폼 UI 추가"

git add .
git commit -m "feat(auth): 로그인 API 연결"
```

### 3) 원격에 푸시 (PR 생성)

```bash
git push -u origin feature/auth-login
```

### 4) 리뷰 반영 중 master 최신 반영 (충돌 최소화)

```bash
git switch master
git pull origin master

git switch feature/auth-login
git merge master
# 충돌 발생 시 해결 후
git add .
git commit -m "chore(merge): resolve conflicts with master"
git push
```

### 5) PR 머지 후 브랜치 정리

```bash
git switch master
git pull origin master

git branch -d feature/auth-login
git push origin --delete feature/auth-login
```

---

## 🔥 자주 쓰는 `switch` 치트키

### 원격 브랜치 받아서 바로 이동

```bash
git fetch
git switch feature/auth-login
```

### 브랜치 목록 확인

```bash
git branch
```