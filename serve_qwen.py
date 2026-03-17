"""
llama-cpp-python 서버를 이용한 Qwen3.5-35B-A3B 서빙 스크립트
- Windows 지원
- 동시 요청 처리 (--n-parallel)
- OpenAI 호환 API

실행:
  uv run serve_qwen.py
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "huggingface-hub",
# ]
# [tool.uv]
# find-links = ["https://abetlen.github.io/llama-cpp-python/whl/cu124"]
# ///

import os
import subprocess
from pathlib import Path
from huggingface_hub import hf_hub_download


# ── 설정 ──────────────────────────────────────────────
MODEL_REPO = "unsloth/Qwen3.5-35B-A3B-GGUF"
MODEL_FILE = "Qwen3.5-35B-A3B-Q4_K_M.gguf"
MODEL_DIR = Path("./models")

HOST = "0.0.0.0"
PORT = 17722
N_GPU_LAYERS = -1       # -1 = 전체 GPU 오프로드
N_CTX = 65536            # 컨텍스트 길이
N_PARALLEL = 10          # 동시 요청 처리 수
CHAT_FORMAT = "chatml"  # Qwen 채팅 포맷
THINKING_BUDGET = 16384
# ─────────────────────────────────────────────────────


def download_model() -> Path:
    """HuggingFace에서 GGUF 모델 다운로드"""
    model_path = MODEL_DIR / MODEL_FILE
    if model_path.exists():
        print(f"✓ 모델 파일이 이미 존재합니다: {model_path}")
        return model_path

    print(f"⬇ 모델 다운로드 중: {MODEL_REPO}/{MODEL_FILE}")
    print("  (최초 1회만 실행됩니다. 약 20GB)")
    downloaded = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=str(MODEL_DIR),
    )
    print(f"✓ 다운로드 완료: {downloaded}")
    return Path(downloaded)


def serve(model_path: Path):
    """llama-server.exe 바이너리를 직접 실행"""
    server_dir = Path("./llama-server").absolute()
    server_exe = server_dir / "llama-server.exe"

    # DLL 경로 설정 (CUDA 및 ggml DLL을 찾기 위함)
    os.environ["PATH"] = f"{server_dir};{os.environ.get('PATH', '')}"

    print("=" * 60)
    print(f"  llama-server 시작 (Standalone Binary)")
    print(f"  모델: {MODEL_FILE}")
    print(f"  동시 요청 수: {N_PARALLEL}")
    print(f"  API: http://{HOST}:{PORT}")
    print("=" * 60)
    print()
    print("사용 예시 (curl):")
    print(f'  curl http://localhost:{PORT}/v1/chat/completions \\')
    print('    -H "Content-Type: application/json" \\')
    print(f'    -d \'{{"model": "qwen",')
    print('          "messages": [{"role": "user", "content": "안녕하세요"}],')
    print('          "max_tokens": 512}\'')
    print("=" * 60)

    # llama-server.exe 인자 구성
    cmd = [
        str(server_exe),
        "--model", str(model_path.absolute()),
        "--host", HOST,
        "--port", str(PORT),
        "--n-gpu-layers", str(N_GPU_LAYERS),
        "--ctx-size", str(N_CTX),
        "--parallel", str(N_PARALLEL),
        # "--chat-template", CHAT_FORMAT, # llama-server는 파일이나 문자열 템플릿을 선호함
    ]

    # 'thinking' 기능 조절을 위한 인자들
    cmd.extend([
        "--reasoning-budget", f"{THINKING_BUDGET}",
        "--chat-template-kwargs", '{"enable_thinking": false}'
    ])

    subprocess.run(cmd)


if __name__ == "__main__":
    model_path = download_model()
    serve(model_path)
