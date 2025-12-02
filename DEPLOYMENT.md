# life_quotes GitHub & Render 배포 가이드

이 가이드는 `life_quotes` 프로젝트를 GitHub에 올리고 Render로 배포하는 방법을 설명합니다.

## 📋 사전 준비

1. **GitHub 계정** 생성 (없는 경우)
2. **Render 계정** 생성 (https://render.com)
3. **Git 설치** 확인

## 🚀 1단계: GitHub에 코드 업로드

### 1.1 Git 저장소 초기화

```bash
cd /Users/abenu/Downloads/Forecast/LearningData/life_quotes
git init
```

### 1.2 파일 추가 및 커밋

```bash
# 모든 파일 추가
git add .

# 첫 커밋
git commit -m "Initial commit: life_quotes project"
```

### 1.3 GitHub 저장소 생성

1. GitHub 웹사이트 접속: https://github.com
2. 우측 상단 **"+"** → **"New repository"** 클릭
3. 저장소 정보 입력:
   - **Repository name**: `life_quotes` (또는 원하는 이름)
   - **Description**: "생년월일 기반 매일 명언/시 제공 시스템"
   - **Visibility**: Public 또는 Private 선택
   - **Initialize this repository with**: 체크하지 않음 (이미 로컬에 파일이 있음)
4. **"Create repository"** 클릭

### 1.4 로컬 저장소와 GitHub 연결

GitHub에서 생성된 저장소의 URL을 복사한 후:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 본인의 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/life_quotes.git

# 또는 SSH 사용 (SSH 키가 설정된 경우)
git remote add origin git@github.com:YOUR_USERNAME/life_quotes.git
```

### 1.5 코드 푸시

```bash
# 기본 브랜치를 main으로 설정 (GitHub 기본 브랜치)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 🌐 2단계: Render에 배포

### 2.1 Render 대시보드 접속

1. https://render.com 접속
2. **"Sign Up"** 또는 **"Log In"** 클릭
3. GitHub 계정으로 로그인 (권장)

### 2.2 새 Web Service 생성

1. Render 대시보드에서 **"New +"** → **"Web Service"** 클릭
2. **"Connect account"** 또는 **"Connect GitHub"** 클릭하여 GitHub 연결
3. 저장소 선택: `life_quotes` 저장소 선택
4. **"Connect"** 클릭

### 2.3 서비스 설정

다음 정보를 입력:

- **Name**: `life-quotes` (또는 원하는 이름)
- **Environment**: `Python 3`
- **Region**: 원하는 지역 선택 (예: `Singapore`)
- **Branch**: `main` (또는 기본 브랜치)
- **Root Directory**: 비워두기 (루트 디렉토리 사용)
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```
- **Plan**: 
  - **Free**: 무료 플랜 (15분 비활성화 후 슬리프 모드)
  - **Starter**: 유료 플랜 (항상 실행)

### 2.4 환경 변수 설정 (선택사항)

**Environment** 탭에서 환경 변수 추가:

- `FLASK_DEBUG=0` (프로덕션 모드)
- `PORT` (자동 설정됨, 수동 설정 불필요)

### 2.5 서비스 생성 및 배포

1. **"Create Web Service"** 클릭
2. Render가 자동으로 빌드 및 배포 시작
3. **"Logs"** 탭에서 빌드 진행 상황 확인
4. 배포 완료 후 서비스 URL 확인:
   - 예: `https://life-quotes-xxxx.onrender.com`

## ✅ 3단계: 배포 확인

### 3.1 서비스 접속

브라우저에서 Render에서 제공한 URL로 접속:
```
https://your-service-name.onrender.com
```

### 3.2 기능 테스트

1. 생년월일 입력
2. 오늘의 명언/시 확인
3. 오늘의 컬러 확인
4. 오늘의 한잔 확인
5. 공유 기능 테스트

## 🔄 4단계: 코드 업데이트 및 재배포

### 4.1 로컬에서 코드 수정

```bash
# 파일 수정 후
git add .
git commit -m "Update: 설명"
git push origin main
```

### 4.2 자동 재배포

- Render는 GitHub에 푸시하면 자동으로 재배포합니다
- **"Events"** 탭에서 배포 상태 확인 가능

### 4.3 수동 재배포

1. Render 대시보드에서 서비스 선택
2. **"Manual Deploy"** → **"Deploy latest commit"** 클릭

## 🔧 문제 해결

### 빌드 실패

1. **Logs 탭 확인**: 빌드 로그에서 오류 메시지 확인
2. **requirements.txt 확인**: 모든 패키지가 올바른지 확인
3. **Python 버전 확인**: `runtime.txt`에 올바른 버전이 있는지 확인

### 서비스 시작 실패

1. **Logs 탭 확인**: 런타임 로그 확인
2. **Start Command 확인**: `gunicorn app:app --bind 0.0.0.0:$PORT` 올바른지 확인
3. **포트 확인**: `app.py`에서 `PORT` 환경 변수를 사용하는지 확인

### 404 오류

- 경로 확인: `/api/daily`, `/api/birthday` 등 API 경로 확인
- JavaScript의 API 호출 경로 확인

### 데이터 저장 문제

- `data/` 폴더가 `.gitignore`에 포함되어 있어 GitHub에 업로드되지 않습니다
- Render에서는 런타임에 자동으로 생성됩니다
- 데이터는 서비스 재시작 시 초기화될 수 있습니다 (무료 플랜)

## 📝 체크리스트

배포 전 확인사항:

- [ ] `.gitignore`에 `venv/`, `__pycache__/`, `data/` 포함
- [ ] `requirements.txt`에 `gunicorn` 포함
- [ ] `Procfile` 생성 및 올바른 명령어 포함
- [ ] `runtime.txt`에 Python 버전 지정
- [ ] `app.py`에서 `PORT` 환경 변수 사용
- [ ] GitHub에 코드 푸시 완료
- [ ] Render 서비스 생성 완료
- [ ] 배포 후 기능 테스트 완료

## 🌐 커스텀 도메인 설정

커스텀 도메인을 사용하려면:

1. Render 대시보드 → 서비스 선택
2. **Settings** → **Custom Domains**
3. 도메인 추가 및 DNS 설정
4. 자세한 내용은 [RENDER_DOMAIN.md](RENDER_DOMAIN.md) 참고

## 📚 추가 리소스

- [Render 공식 문서](https://render.com/docs)
- [Gunicorn 문서](https://gunicorn.org/)
- [Flask 배포 가이드](https://flask.palletsprojects.com/en/latest/deploying/)

