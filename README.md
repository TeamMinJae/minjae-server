# Video Caption Server

FastAPI 기반의 비디오 캡션 오버레이 서버입니다. POST 요청으로 이름 목록을 받아 미리 정의된 위치와 시간에 캡션을 추가한 비디오를 반환합니다.

## 프로젝트 구조

```
video-caption-server/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱과 /generate 엔드포인트
│   ├── utils/
│   │   ├── __init__.py
│   │   └── overlay.py       # ffmpeg를 사용한 비디오 오버레이 함수
│   ├── assets/
│   │   └── base_video.mp4   # 기본 비디오 파일 (30초 파란색 배경)
│   └── temp/                # 임시 출력 비디오 파일 저장소
├── requirements.txt         # 필요한 패키지들
├── run.sh                   # 서버 실행 스크립트
└── README.md               # 이 파일
```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd video-caption-server
   ```

2. 서버 실행:
   ```bash
   ./run.sh
   ```

   이 스크립트는 다음을 자동으로 처리합니다:
   - 가상환경 생성 (없는 경우)
   - 의존성 설치
   - FastAPI 서버 시작 (http://localhost:8080)

## API 사용법

### POST /generate

이름 목록을 받아 캡션이 추가된 비디오를 생성합니다.

**요청 예시:**
```bash
curl -X POST "http://localhost:8080/generate" \
     -H "Content-Type: application/json" \
     -d '{"names": ["김철수", "이영희", "박민수"]}' \
     --output output_video.mp4
```

**요청 바디:**
```json
{
  "names": ["이름1", "이름2", "이름3"]
}
```

**응답:** MP4 비디오 파일

### 기타 엔드포인트

- `GET /` : 서버 상태 확인
- `GET /health` : 헬스 체크 (비디오 파일 및 디렉토리 상태 확인)

## 캡션 위치 및 타이밍

현재 미리 정의된 캡션 위치:
1. (100, 100) - 2초에 시작, 3초 지속
2. (400, 200) - 6초에 시작, 3초 지속  
3. (700, 300) - 10초에 시작, 3초 지속
4. (200, 400) - 14초에 시작, 3초 지속
5. (500, 150) - 18초에 시작, 3초 지속

최대 5개의 이름까지 지원됩니다.

## 개발 상태

현재는 기본적인 구조와 더미 응답이 구현되어 있습니다. 실제 ffmpeg 로직은 `app/utils/overlay.py`에 주석으로 계획이 작성되어 있으며, 향후 구현될 예정입니다.

## 요구사항

- Python 3.8+
- ffmpeg (비디오 처리용)
- FastAPI 및 관련 의존성 (requirements.txt 참조) # video-caption-server
