#!/bin/bash

# 비디오 자막 서버 시작 스크립트
echo "비디오 자막 서버를 시작합니다..."

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo "가상환경을 생성하고 있습니다..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "가상환경을 활성화하고 있습니다..."
source venv/bin/activate

# 의존성 설치
echo "의존성을 설치하고 있습니다..."
pip install -r requirements.txt

# temp 디렉토리가 없으면 생성
mkdir -p app/temp

# 서버 시작
echo "FastAPI 서버를 http://localhost:8080 에서 시작합니다"
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload 