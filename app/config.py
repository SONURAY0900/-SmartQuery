# LM_STUDIO_URL = "http://10.0.14.24:9009/v1/chat/completions"

# MODELS = {
#     "intent": "mistralai/mistral-7b-instruct-v0.3",
#     "generator": "lapinmalin/deepseek-coder-6.7b-instruct",
#     "validator": "lapinmalin/deepseek-coder-6.7b-instruct",
#     "explainer": "mistralai/mistral-7b-instruct-v0.3"
# }



import os

# -------------------------------
# GROQ CONFIGURATION
# -------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# -------------------------------
# MODELS (FAST + FREE TIER)
# -------------------------------

MODELS = {
    "intent": "llama-3.1-8b-instant",
    "generator": "llama-3.1-8b-instant",
    "validator": "llama-3.1-8b-instant",
    "explainer": "llama-3.1-8b-instant"
}
