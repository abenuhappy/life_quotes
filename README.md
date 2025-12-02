# 생년월일 기반 매일 명언/시 제공 시스템

생년월일을 입력받아 매일 다른 명언이나 시를 제공하는 웹 애플리케이션입니다.

## 🌟 주요 기능

- **생년월일 입력**: 사용자의 생년월일을 저장
- **생년월일 분석**: 별자리, 타로 카드, 생일 특성 분석
- **매일 명언/시 제공**: 온라인에서 자동으로 수집하여 매일 다른 명언/시 제공
- **온라인 수집**: 여러 소스에서 명언/시를 자동으로 가져옴

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 실행

```bash
python app.py
```

### 3. 브라우저 접속

```
http://localhost:5003
```

## 📁 파일 구조

```
life_quotes/
├── app.py                  # Flask 백엔드
├── quote_fetcher.py        # 온라인 명언/시 수집 모듈
├── birthday_analyzer.py    # 생년월일 분석 모듈
├── requirements.txt        # 패키지 목록
├── templates/
│   └── index.html         # 메인 페이지
├── static/
│   ├── css/
│   │   └── style.css      # 스타일
│   └── js/
│       └── app.js         # 프론트엔드 로직
└── data/                   # 사용자 데이터 저장 폴더 (자동 생성)
```

## 🔧 기능 설명

### 1. 생년월일 분석

- **별자리**: 양력 기준 별자리 계산
- **타로 카드**: 생일 숫자 기반 타로 카드
- **생일 특성**: 계절, 요일, 생명수 등

### 2. 명언/시 수집

다음 소스에서 명언/시를 수집합니다:

- **Zen Quotes API**: 영어 명언
- **Quotable API**: 영어 명언
- **한국어 명언/시**: 내장 데이터베이스

### 3. 매일 다른 명언

날짜를 시드로 사용하여 같은 날짜면 같은 명언을 제공합니다.
다음 날이 되면 자동으로 다른 명언이 표시됩니다.

## 📝 API 엔드포인트

### POST `/api/birthday`
생년월일 저장

```json
{
  "user_id": "user_123",
  "birth_date": "1990-05-15"
}
```

### GET `/api/birthday/<user_id>`
저장된 생년월일 조회

### POST `/api/analyze`
생년월일 분석

```json
{
  "birth_date": "1990-05-15"
}
```

### GET `/api/quote`
명언/시 조회

```
/api/quote?user_id=user_123&date=2024-01-01
```

### GET `/api/daily`
오늘의 명언/시 (통합)

```
/api/daily?user_id=user_123
```

## 🎨 사용 방법

1. **생년월일 입력**: 메인 페이지에서 생년월일을 입력하고 저장
2. **명언 확인**: 저장 후 자동으로 오늘의 명언/시가 표시됩니다
3. **새로고침**: "🔄 오늘의 명언 새로고침" 버튼으로 다시 로드
4. **분석 정보**: 생년월일 분석 정보도 함께 표시됩니다

## 🔄 온라인 수집 개선

현재는 기본적인 명언/시 데이터를 제공합니다. 더 많은 소스를 추가하려면:

1. `quote_fetcher.py`에 새로운 수집 함수 추가
2. `fetch_quote()` 메서드의 `sources` 리스트에 추가
3. 한국어 명언 사이트 스크래핑 추가 가능

## 🚀 배포 (Render)

자세한 배포 가이드는 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고하세요.

### 빠른 배포

1. GitHub에 코드 푸시
2. Render에서 새 Web Service 생성
3. GitHub 저장소 연결
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## 📌 참고사항

- 사용자 데이터는 `data/` 폴더에 JSON 파일로 저장됩니다
- 실제 운영 환경에서는 데이터베이스를 사용하는 것을 권장합니다
- 온라인 API 호출이 실패하면 기본 명언을 제공합니다
- Render 무료 플랜은 15분 비활성화 후 슬리프 모드로 전환됩니다

## 🐛 문제 해결

### 포트가 이미 사용 중인 경우

환경 변수로 포트 변경:

```bash
PORT=5004 python app.py
```

### 패키지 설치 오류

가상 환경 사용 권장:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

