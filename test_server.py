import requests
import json
import sys

# Windows 콘솔에서 UTF-8 출력을 지원하도록 설정
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:17722/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "qwen3.6-35b-a3b-ud-q4_k_m",
    "messages": [
        {"role": "user", "content": "안녕하세요. 반갑습니다. 간단하게 인사해줘."}
    ],
    "max_tokens": 100
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection failed: {e}")
