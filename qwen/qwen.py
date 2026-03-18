import dashscope
from config.settings import QWEN_MODEL, get_dashscope_api_key

def ask_qwen(prompt):
    api_key = get_dashscope_api_key()
    if not api_key:
        raise RuntimeError(
            "DASHSCOPE_API_KEY is empty. "
            "Set it in environment variable or project .env file."
        )
    dashscope.api_key = api_key

    response = dashscope.Generation.call(
        model=QWEN_MODEL,
        prompt=prompt
    )

    status_code = getattr(response, "status_code", None)
    if status_code and status_code != 200:
        message = getattr(response, "message", "Unknown API error")
        raise RuntimeError(f"Qwen API request failed: {message}")

    output = getattr(response, "output", None)
    text = getattr(output, "text", None) if output else None
    if not text:
        raise RuntimeError("Qwen API returned empty text.")

    return text
