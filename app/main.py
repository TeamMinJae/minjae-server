# main.py
import mimetypes
import os
import importlib.util  # 모듈을 동적으로 로드하기 위함
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

# app 모듈에서 필요한 함수를 임포트합니다.
from app.overlay import add_captions_to_video
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME", "videos")

app = FastAPI(title="비디오 서버", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "https://127.0.0.1:3000", "http://localhost:3000", "https://localhost:3000", "https://v0-min-jae.vercel.app"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    roomId: str = Field(..., description="방 ID")
    winner: str = Field(..., description="승자 이름")
    others: List[str] = Field(..., description="패자들 이름 목록")
    base_video_id: int = Field(..., description="사용할 기본 비디오의 ID (예: 1, 2 등)")


class VideoResponse(BaseModel):
    video_url: str = Field(..., description="생성된 비디오의 URL")


# 디렉토리 경로 설정
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
RESULT_VIDEO_DIR = BASE_DIR / "temp"
CAPTIONS_DIR = BASE_DIR / "captions"  # 캡션 템플릿 디렉토리

# 필요한 디렉토리가 없으면 생성 (서버 시작 시 한 번만 실행되도록 보장)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(RESULT_VIDEO_DIR, exist_ok=True)
os.makedirs(CAPTIONS_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "비디오 자막 서버가 실행 중입니다"}


@app.get("/videos/{filename}")
async def get_result_video(filename: str):
    """
    생성된 비디오 파일을 클라이언트에 제공합니다.
    """
    file_path = RESULT_VIDEO_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="비디오 파일을 찾을 수 없습니다.")

    return FileResponse(file_path, media_type="video/mp4", filename=filename)


@app.post("/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def generate_video(request: VideoRequest):
    """
    승자, 패자 목록, 방 ID, 기본 비디오 ID를 기반으로 비디오를 생성하고 해당 URL을 반환합니다.
    """
    await _validate_request(request)

    # 1. 기본 비디오 선택
    base_video_filename = f"{request.base_video_id}.mp4"
    current_base_video_path = ASSETS_DIR / base_video_filename

    if not current_base_video_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"기본 비디오 '{base_video_filename}'을(를) 찾을 수 없습니다. assets 폴더에 해당 ID의 MP4 파일이 있는지 확인하세요."
        )

    # 2. base_video_id에 해당하는 캡션 템플릿 동적 로드
    caption_template_filename = f"video_template_{request.base_video_id}.py"
    caption_template_path = CAPTIONS_DIR / caption_template_filename

    if not caption_template_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"캡션 템플릿 '{caption_template_filename}'을(를) 찾을 수 없습니다. app/captions 폴더에 해당 파일이 있는지 확인하세요."
        )

    try:
        # 동적으로 모듈 로드
        spec = importlib.util.spec_from_file_location(
            f"video_template_{request.base_video_id}",
            str(caption_template_path)
        )
        caption_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(caption_module)

        # 로드된 모듈에서 generate_captions_for_videoX 함수 가져오기
        # 함수 이름 규칙을 'generate_captions_for_video{id}' 로 가정
        generate_captions_func_name = f"generate_captions_for_video{request.base_video_id}"
        generate_captions_func = getattr(caption_module, generate_captions_func_name, None)

        if not generate_captions_func or not callable(generate_captions_func):
            raise AttributeError(
                f"캡션 템플릿 '{caption_template_filename}'에서 '{generate_captions_func_name}' 함수를 찾을 수 없거나 호출할 수 없습니다."
            )

        # 캡션 생성 함수 호출
        captions = generate_captions_func(winner=request.winner, others=request.others)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"캡션 템플릿 로드 또는 캡션 생성 중 오류가 발생했습니다: {str(e)}"
        )

    # 3. 비디오에 캡션 추가 및 렌더링
    try:
        output_path = await add_captions_to_video(
            video_path=str(current_base_video_path),
            captions=captions,
            output_dir=str(RESULT_VIDEO_DIR)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"비디오 생성 중 오류가 발생했습니다: {str(e)}"
        )

    # 4. 생성된 비디오를 CDN에 업로드하고 URL을 받음
    cdn_video_url = await _upload_to_cdn(Path(output_path))

    # 5. (선택 사항) 로컬에 임시 저장된 파일 삭제
    os.remove(output_path)

    return VideoResponse(video_url=cdn_video_url)


async def _upload_to_cdn(file_path: Path) -> str:
    """
    Supabase Storage에 비디오 파일을 업로드하고 CDN URL 반환
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase 설정이 누락되었습니다.")

    filename = file_path.name
    upload_path = f"{SUPABASE_BUCKET_NAME}/{filename}"
    mime_type, _ = mimetypes.guess_type(str(file_path))

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": mime_type or "application/octet-stream",
    }

    upload_url = f"{SUPABASE_URL}/storage/v1/object/{upload_path}"

    async with httpx.AsyncClient() as client:
        with open(file_path, "rb") as f:
            response = await client.post(upload_url, content=f.read(), headers=headers)

    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=500, detail=f"Supabase 업로드 실패: {response.text}")

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET_NAME}/{filename}"
    return public_url


async def _validate_request(request: VideoRequest):
    """
    들어오는 요청의 유효성을 검사합니다.
    """
    if not request.winner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="승자 이름이 필요합니다.")
    if not request.others:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="다른 사람들의 이름 목록이 비어있을 수 없습니다.")
