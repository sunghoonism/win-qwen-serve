# llama-server 자동 설치 프롬프트

이 프로젝트는 동작 시 `llama-server/` 폴더 하위에 `llama-server.exe`와 관련 DLL 파일들이 필요합니다. 
Claude Code 안에서 구동 중이라면, 아래의 프롬프트를 입력하여 번거로운 설치 과정을 자동으로 처리할 수 있습니다.

---

### 📋 프롬프트 복사하기

```text
현재 디렉토리 기준으로 아래 작업을 순서대로 진행해줘:

1. 인터넷 검색을 통해 최신 `llama.cpp`의 Windows용 릴리즈(CUDA 지원 버전, 예: llama-bXXXX-bin-win-cuda-cu12.X-x64.zip)의 다운로드 URL을 획득해. 공식 GitHub 릴리즈 페이지(https://github.com/ggerganov/llama.cpp/releases)를 참고하면 돼.
2. 획득한 URL에서 zip 파일을 로컬 스토리지에 다운로드 받아줘. 파워쉘 명령어 등을 직접 이용해도 좋아.
3. 다운로드한 zip 파일의 압축을 로컬 임시 폴더에 해제해.
4. 압축 해제된 파일들 중에서 `llama-server.exe`와 확장자가 `.dll`인 모든 파일들을 찾아줘.
5. 현재 프로젝트 루트 위치에 `llama-server/` 라는 디렉토리를 생성해.
6. 찾은 `llama-server.exe`와 모든 `.dll` 파일들을 방금 만든 `llama-server/` 디렉토리 안으로 복사(또는 이동)해줘.
7. 작업이 완전히 끝난 후에는 다운로드했던 원본 zip 파일과 압축을 풀었던 임시 폴더 흔적을 삭제해줘.
```

---
**팁:** 다운로드 실패 등의 문제가 발생하는 경우, 에이전트에게 **자신의 PC에 맞는 특정 빌드(예: vulkan, cu117, cu122 등)**를 자세히 명시해주면 더 정확히 동작합니다.
