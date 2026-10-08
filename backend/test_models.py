import os
import httpx

key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-3.5-flash"]
for m in models:
    try:
        res = httpx.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}", json={"contents": [{"parts":[{"text":"Hello"}]}]})
        print(f"{m}: {res.status_code}")
        if res.status_code != 200:
            print(f"  {res.text}")
    except Exception as e:
        print(f"{m}: Error {e}")
