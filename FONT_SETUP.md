# 한글 폰트 설정 가이드

OG 이미지에서 한글이 깨지지 않도록 하려면 한글 폰트 파일을 추가해야 합니다.

## 방법 1: 프로젝트에 폰트 파일 추가 (권장)

1. **Noto Sans KR 폰트 다운로드**
   - Google Fonts에서 다운로드: https://fonts.google.com/noto/specimen/Noto+Sans+KR
   - 또는 직접 다운로드: https://github.com/google/fonts/tree/main/ofl/notosanskr

2. **폰트 파일을 프로젝트에 추가**
   ```
   static/fonts/NotoSansKR-Bold.otf
   static/fonts/NotoSansKR-Regular.otf
   ```

3. **또는 Nanum Gothic 사용**
   - 나눔고딕 다운로드: https://hangeul.naver.com/2017/nanum
   - 폰트 파일을 `static/fonts/` 폴더에 추가:
     ```
     static/fonts/NanumGothic-Bold.ttf
     static/fonts/NanumGothic-Regular.ttf
     ```

## 방법 2: Render에서 시스템 폰트 사용

Render는 Linux 환경이므로, 다음 경로의 폰트를 자동으로 찾습니다:
- `/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc`
- `/usr/share/fonts/truetype/nanum/NanumGothic-Regular.ttf`

Render에서 한글 폰트를 설치하려면 `render.yaml` 또는 Build Command에 다음을 추가:
```bash
sudo apt-get update && sudo apt-get install -y fonts-nanum fonts-noto-cjk
```

## 확인 방법

폰트가 제대로 로드되었는지 확인:
1. `/og-image` 엔드포인트 접속
2. 생성된 이미지에서 한글이 깨지지 않고 표시되는지 확인

## 참고

- 폰트 파일이 없어도 앱은 정상 작동하지만, OG 이미지의 한글이 깨질 수 있습니다
- 프로젝트에 폰트를 포함시키는 것이 가장 안정적입니다

