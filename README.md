# Qwen3.5 LLM 서버

Qwen3.6-35B-A3B 모델을 Windows 환경에서 고성능으로 서빙하기 위한 스크립트입니다.

## 주요 특징
- **Windows 최적화**: Windows 환경에서 CUDA 가속을 사용하는 Standalone 바이너리(`llama-server.exe`)를 실행합니다.
- **자동 모델 다운로드**: HuggingFace(`unsloth/Qwen3.6-35B-A3B-GGUF`)에서 GGUF 모델을 자동으로 다운로드합니다.
- **병렬 처리**: `--parallel` 설정을 통해 여러 요청을 동시에 처리할 수 있습니다. (기본값: cpu코어수)
- **Thinking 기능 제어**: Qwen3.6의 'thinking' 기능에 적당한 Budget을 설정하여 추론 성능과 대화 응답 속도를 조절할 수 있습니다.

## 설치 방법
**바이너리**: `./llama-server/` 폴더 내에 `llama-server.exe` 및 필요한 DLL 파일들이 있어야 합니다.  
(Claude Code 등을 이용해 설치하세요. [doc/llama_install_prompt.md](./doc/llama_install_prompt.md) 문서의 프롬프트 참고)  
이 설치 이후 아래 실행 방법의 명령어를 입력하면 됩니다.

## 실행 방법
```bash
uv run serve_qwen.py
```

## 주요 설정 (스크립트 내 수정 가능)
- `PORT`: 서버 포트 (기본값: 17722)
- `N_GPU_LAYERS`: GPU 오프로드 레이어 수 (기본값: -1, 전체 GPU 사용)
- `N_CTX`: 컨텍스트 길이 (기본값: 524288)
- `N_PARALLEL`: 동시 요청 처리 수 (기본값: cpu코어수)
- `THINKING_BUDGET`: 추론(Reasoning) 예산 (기본값: 16384)

## 테스트 실행 방법
```bash
uv run test_server.py
```

## 필수 환경 및 폴더 구조
- **OS**: Windows
- **GPU**: NVIDIA GPU VRAM 24G 이상 (예: RTX 3090, 4090 등)
- **CUDA**: 12.4 이상 버전이 설치되어 있어야 함
- **Python**: 3.10 이상 및 `uv` 패키지 매니저
- **모델**: `./models/` 폴더에 GGUF 모델 파일이 저장됩니다. (스크립트 실행 시 자동 다운로드)
