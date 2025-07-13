"""
ffmpeg를 사용하여 비디오에 자막을 추가하는 오버레이 유틸리티 (비동기 버전)
"""

import os
import uuid
import asyncio # 비동기 처리를 위해 추가
from pathlib import Path # Path 객체 사용을 위해 추가
from typing import List, Dict, Any

# FFmpeg 실행 파일 경로 (시스템 환경에 맞게 조정 필요)
# Render와 같은 클라우드 환경에서는 'ffmpeg'만으로 PATH에서 찾을 수 있는 경우가 많습니다.
# 만약 PATH에 없다면 Dockerfile 등에서 설치 경로를 지정해야 합니다.
FFMPEG_EXEC_PATH = "ffmpeg"

# 사용할 한글 폰트 경로 (Render에 배포 시 이 파일도 같이 업로드할 것)
# 이 경로는 'your_project/app/assets/NanumGothic.ttf' 와 같이 상대 경로로 지정하거나
# 배포 환경에서 폰트가 설치된 실제 절대 경로로 지정해야 합니다.
# 예시: FONT_PATH = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf" (리눅스)
# 현재 프로젝트 구조에 맞게 'app' 디렉토리 내부로 경로를 설정했습니다.
FONT_PATH_FOR_FFMPEG = str(Path(__file__).parent / "assets" / "NanumGothic.ttf") # Path 객체로 경로 구성

# create_captions_from_names는 이제 main.py에서 동적으로 로드된 캡션 템플릿을 사용할 것이므로,
# 여기서 캡션 템플릿 매핑을 제거하고 단순 메시지 처리만 담당합니다.
# (이 함수는 main.py의 동적 로딩과 함께 사용되지 않을 가능성이 높습니다.
# 필요하다면 main.py의 generate_video에서 직접 캡션 데이터를 구성하세요.)
# 여기서는 단순히 예시로 남겨둡니다.
def create_captions_from_names(messages: List[str], template: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """메시지 리스트로부터 캡션 데이터를 생성합니다. (템플릿 기반)"""
    _validate_messages(messages)

    captions = []

    for i, message in enumerate(messages):
        if i >= len(template):
            # 템플릿보다 메시지가 많으면 마지막 템플릿의 위치를 기반으로 생성
            # (이 부분은 템플릿의 내용에 따라 매우 유동적으로 변해야 합니다. 일반화하기 어려움)
            # 여기서는 예시로 남겨두지만, 실제 사용 시에는 명확한 템플릿 규칙이 필요합니다.
            if template:
                last_template = template[-1]
                caption = {
                    "text": message,
                    "x": last_template["x"], # x는 고정
                    "y": last_template["y"] + (i - len(template) + 1) * 40, # y는 메시지 개수에 따라 아래로 이동
                    "start": last_template["start"] + (i - len(template) + 1) * 2.0,
                    "duration": 2.0
                }
            else: # 템플릿이 없는 경우
                caption = {
                    "text": message, "x": 100, "y": 100 + i * 40, "start": i * 2.0, "duration": 2.0
                }
        else:
            # 템플릿을 복사하고 메시지만 교체
            caption = template[i].copy()
            caption["text"] = message
            # "message" 키가 있으면 "text"로 통일 (FFmpeg 필터는 'text'를 사용)
            if "message" in caption:
                caption["text"] = caption.pop("message") # 'message'를 'text'로 변경하고 기존 'message' 키 제거

        captions.append(caption)

    return captions

# 이 함수는 main.py에서 직접 캡션 템플릿 모듈의 함수를 호출하도록 변경했으므로,
# 여기서는 더 이상 사용되지 않을 수 있습니다.
# def create_captions_from_template(video_id: str = "video1") -> List[Dict[str, Any]]:
#     """템플릿에서 직접 캡션 데이터를 가져옵니다."""
#     if video_id in VIDEO_CAPTION_TEMPLATES:
#         template = VIDEO_CAPTION_TEMPLATES[video_id]
#     else:
#         raise ValueError(f"영상 ID {video_id}에 대한 캡션 템플릿을 찾을 수 없습니다.")

#     captions = []
#     for caption_template in template:
#         caption = caption_template.copy()
#         captions.append(caption)

#     return captions


async def add_captions_to_video(video_path: str, captions: List[Dict[str, Any]], output_dir: str) -> str:
    """비디오에 자막을 추가하고 결과 파일 경로를 반환합니다. (비동기)"""
    _validate_inputs(video_path, captions)

    output_filename = f"video_with_captions_{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    try:
        await _render_with_ffmpeg(video_path, captions, output_path) # await 추가
        return output_path
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path) # 실패 시 임시 파일 삭제
        raise RuntimeError(f"[오류] 비디오 자막 렌더링 실패: {e}")

def _validate_messages(messages: List[str]) -> None:
    if not messages or not all(message.strip() for message in messages):
        raise ValueError("메시지가 유효하지 않습니다.")

def _validate_inputs(video_path: str, captions: List[Dict[str, Any]]) -> None:
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"입력 비디오가 존재하지 않습니다: {video_path}")
    if not captions:
        raise ValueError("캡션 데이터가 비어 있습니다.")

    # 캡션 데이터 유효성 검사 (X, Y, start, duration 필수)
    required_keys = {"text", "x", "y", "start", "duration"}
    for i, caption in enumerate(captions):
        # 'message' 키가 있으면 'text'로 변환되었음을 가정
        if "message" in caption and "text" not in caption:
            caption["text"] = caption["message"]

        missing_keys = required_keys - set(caption.keys())
        if missing_keys:
            raise ValueError(f"캡션 {i}에 필수 키가 누락되었습니다: {missing_keys}. (필수: {required_keys})")

async def _render_with_ffmpeg(input_path: str, captions: List[Dict[str, Any]], output_path: str) -> None:
    """FFmpeg를 비동기적으로 실행하여 비디오를 렌더링합니다."""
    filter_str = _build_drawtext_filters(captions)

    cmd = [
        FFMPEG_EXEC_PATH, # FFmpeg 실행 경로
        "-i", input_path,
        "-vf", filter_str, # 비디오 필터 적용
        "-c:a", "copy", # 오디오는 원본과 동일하게 복사
        "-y", # 출력 파일이 이미 존재하면 덮어쓰기
        output_path
    ]

    print(f"FFmpeg 명령어 실행: {' '.join(cmd)}") # 디버깅을 위한 명령어 출력

    # 비동기적으로 subprocess 실행
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_message = f"FFmpeg 에러:\nSTDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}"
        print(error_message) # 콘솔에 에러 출력
        raise RuntimeError(error_message)

def _build_drawtext_filters(captions: List[Dict[str, Any]]) -> str:
    """drawtext 필터 문자열 생성"""
    filters = []

    for caption in captions:
        text = caption["text"]
        start = float(caption["start"])
        end = start + float(caption["duration"])

        # drawtext 필터 조합
        # fontfile 경로가 올바른지 다시 한번 확인하세요.
        filter_ = (
            f"drawtext=fontfile='{FONT_PATH_FOR_FFMPEG}':"
            f"text='{_escape(text)}':"
            f"x={caption['x']}-text_w/2:y={caption['y']}-text_h/2:"
            f"fontsize=48:fontcolor=white:borderw=3:bordercolor=black:"
            f"box=1:boxcolor=black@0.6:boxborderw=8:"
            f"enable='between(t,{start},{end})'"
        )
        filters.append(filter_)

    return ",".join(filters)

def _escape(text: str) -> str:
    """ffmpeg용 텍스트 이스케이프 처리"""
    # 콜론(:)과 작은따옴표(')는 FFmpeg 필터에서 특수 문자로 사용되므로 이스케이프 필요
    return text.replace(":", "\\:").replace("'", "\\'")