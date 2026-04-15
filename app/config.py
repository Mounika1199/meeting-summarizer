import os
import logging
from transformers import AutoTokenizer
from huggingface_hub import login
from functools import lru_cache

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
MAX_CONTEXT_TOKENS = 6000
DEFAULT_MODEL = "gemma3:12b-20k"

# Hugging Face login
if HF_TOKEN:
    try:
        login(token=HF_TOKEN)
        logging.info("✅ Logged in to Hugging Face successfully.")
    except Exception as e:
        logging.warning(f"⚠️ Hugging Face login failed: {e}")

# Tokenizer cache
@lru_cache()
def get_tokenizer():
    return AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
