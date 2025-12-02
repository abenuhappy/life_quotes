#!/bin/bash

# 생년월일 기반 명언/시 시스템 실행 스크립트

echo "생년월일 기반 명언/시 시스템을 시작합니다..."

# 현재 디렉토리 확인
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3가 설치되어 있지 않습니다."
    echo "Python 3.7 이상을 설치해주세요."
    exit 1
fi

# 가상 환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 가상 환경을 생성합니다..."
    python3 -m venv venv
fi

# 가상 환경 활성화
echo "🔧 가상 환경을 활성화합니다..."
source venv/bin/activate

# 패키지 설치
echo "📥 필요한 패키지를 설치합니다..."
pip install --upgrade pip
pip install -r requirements.txt

# data 폴더 생성
mkdir -p data

# Flask 앱 실행
echo "🚀 서버를 시작합니다..."
echo "브라우저에서 http://localhost:5003 접속하세요."
echo ""
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

python app.py

