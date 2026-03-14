# import time
# import requests
# from app.config import LM_STUDIO_URL

# # -------------------------------
# # Tunable parameters (safe defaults)
# # -------------------------------
# REQUEST_TIMEOUT = 300        # seconds (local inference can be slow)
# MAX_TOKENS = 512             # cap output to avoid long generations
# RETRIES = 2                  # auto-retry once on failure
# RETRY_DELAY = 5              # seconds between retries


# def call_llm(model: str, prompt: str) -> str:
#     """
#     Robust LLM caller for LM Studio (OpenAI-compatible API).

#     Features:
#     - Long timeout for local inference
#     - Output token cap
#     - Automatic retry
#     - Defensive JSON parsing
#     - Clear error messages
#     """

#     payload = {
#         "model": model,
#         "messages": [
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0,
#         "max_tokens": MAX_TOKENS
#     }

#     last_error = None

#     for attempt in range(RETRIES):
#         try:
#             response = requests.post(
#                 LM_STUDIO_URL,
#                 json=payload,
#                 timeout=REQUEST_TIMEOUT
#             )

#             # HTTP-level error
#             if response.status_code != 200:
#                 last_error = f"HTTP {response.status_code}: {response.text}"
#                 raise Exception(last_error)

#             # Parse JSON safely
#             try:
#                 data = response.json()
#             except Exception:
#                 last_error = "LLM returned non-JSON response"
#                 raise Exception(last_error)

#             # OpenAI-style success response
#             if isinstance(data, dict) and "choices" in data and data["choices"]:
#                 content = data["choices"][0].get("message", {}).get("content", "")
#                 if content:
#                     return content.strip()

#             # LM Studio error object
#             if isinstance(data, dict) and "error" in data:
#                 last_error = f"LLM error: {data['error']}"
#                 raise Exception(last_error)

#             # Anything else is invalid
#             last_error = "Invalid LLM response structure"
#             raise Exception(last_error)

#         except Exception as e:
#             last_error = str(e)
#             if attempt < RETRIES - 1:
#                 time.sleep(RETRY_DELAY)
#             else:
#                 break

#     # If all retries failed
#     raise Exception(f"LLM connection failed after retries: {last_error}")
import os
import time
import requests

# -------------------------------
# GROQ CONFIG
# -------------------------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------
# Tunable parameters
# -------------------------------
REQUEST_TIMEOUT = 60
MAX_TOKENS = 1024
RETRIES = 2
RETRY_DELAY = 2


def call_llm(model: str, prompt: str) -> str:
    """
    Unified LLM caller (Groq-compatible, OpenAI-style).
    KEEP FUNCTION NAME: call_llm (required by architecture)
    """

    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY not set in environment variables")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": MAX_TOKENS
    }

    last_error = None

    for attempt in range(RETRIES):
        try:
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}: {response.text}"
                raise Exception(last_error)

            data = response.json()

            if "choices" in data and data["choices"]:
                content = data["choices"][0]["message"]["content"]
                return content.strip()

            last_error = "Invalid Groq response format"
            raise Exception(last_error)

        except Exception as e:
            last_error = str(e)
            if attempt < RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                break

    raise Exception(f"LLM call failed: {last_error}")
