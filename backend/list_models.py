import os
import httpx

key = os.getenv("GEMINI_API_KEY", "your-gemini-api-key-here")
try:
    res = httpx.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}")
    print(res.status_code)
    import json
    models = res.json().get("models", [])
    for m in models:
        print(f"Name: {m.get('name')}, Supported Methods: {m.get('supportedGenerationMethods')}")
except Exception as e:
    print(f"Error: {e}")
