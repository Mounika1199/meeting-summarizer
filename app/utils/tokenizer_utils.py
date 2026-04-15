from typing import List
from app.config import get_tokenizer, MAX_CONTEXT_TOKENS

def chunk_text(text: str, max_tokens: int = MAX_CONTEXT_TOKENS) -> List[str]:
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(text)
    return [
        tokenizer.convert_tokens_to_string(tokens[i:i + max_tokens])
        for i in range(0, len(tokens), max_tokens)
    ]