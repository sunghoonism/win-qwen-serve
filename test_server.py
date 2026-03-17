import requests
import json

url = "http://localhost:17722/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "qwen",
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
