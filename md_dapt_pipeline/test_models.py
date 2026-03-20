import httpx
key = "api_key_here"
url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
for m in ["mistralai/mistral-small-4-119b-2603", "moonshotai/kimi-k2.5", "moonshotai/kimi-k2-thinking"]:
    resp = httpx.post(url, headers=headers, json={"model": m, "messages": [{"role": "user", "content": "hi"}]})
    print(m, resp.status_code)
