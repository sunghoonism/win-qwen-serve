"""
llama-cpp-python 서버를 이용한 Qwen3.6-35B-A3B 서빙 스크립트
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

# Avoid Xet-backed download issues on some Windows setups.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")


# ── 설정 ──────────────────────────────────────────────
MODEL_REPO = "unsloth/Qwen3.6-35B-A3B-GGUF"
MODEL_FILE = "Qwen3.6-35B-A3B-UD-Q4_K_M.gguf"
MODEL_DIR = Path("./models")

HOST = "0.0.0.0"
PORT = 17722
N_GPU_LAYERS = -1       # -1 = 전체 GPU 오프로드
N_CTX = 524288           # 컨텍스트 길이
N_PARALLEL = os.cpu_count() or 10  # 동시 요청 처리 수 (CPU 코어 수 기반)
CHAT_FORMAT = "chatml"  # Qwen 채팅 포맷
THINKING_BUDGET = 16384
# ─────────────────────────────────────────────────────


def download_model() -> Path:
    """HuggingFace에서 GGUF 모델 다운로드"""
    model_path = MODEL_DIR / MODEL_FILE
    if model_path.exists():
        return model_path

    print(f"[DOWNLOAD] Downloading model: {MODEL_REPO}/{MODEL_FILE}")
    print("  (first run only, about 22GB)")
    downloaded = hf_hub_download(
        repo_id=MODEL_REPO,
        filename=MODEL_FILE,
        local_dir=str(MODEL_DIR),
    )
    print(f"[DONE] Download complete: {downloaded}")
    return Path(downloaded)


def serve(model_path: Path):
    """llama-server.exe 바이너리를 직접 실행"""
    server_dir = Path("./llama-server").absolute()
    server_exe = server_dir / "llama-server.exe"

    # DLL 경로 설정 (CUDA 및 ggml DLL을 찾기 위함)
    os.environ["PATH"] = f"{server_dir};{os.environ.get('PATH', '')}"

    print("=" * 60)
    print("  llama-server starting (Standalone Binary)")
    print(f"  model: {MODEL_FILE}")
    print(f"  parallel requests: {N_PARALLEL}")
    print(f"  API: http://{HOST}:{PORT}")
    print("=" * 60)
    print()
    print("Example request (curl):")
    print(f'  curl http://localhost:{PORT}/v1/chat/completions \\')
    print('    -H "Content-Type: application/json" \\')
    print(f'    -d \'{{"model": "qwen3.6-35b-a3b-ud-q4_k_m",')
    print('          "messages": [{"role": "user", "content": "Hello"}],')
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
