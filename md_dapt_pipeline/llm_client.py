import httpx
from config import BASE_URL, get_api_key_for_model

async def call_llm(model: str, prompt: str, temperature: float, **kwargs):
    api_key = get_api_key_for_model(model)
    if not api_key:
        raise ValueError(f"No API key found for model '{model}'. Check your .env file.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    payload.update(kwargs)

    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
