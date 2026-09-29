from google import genai
from google.genai import types

from config import settings


class GeminiNotConfiguredError(RuntimeError):
    pass


_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.gemini_configured:
            raise GeminiNotConfiguredError(
                "GEMINI_API_KEY is not configured. Copy .env.example to .env "
                "and add your Google Gemini API key."
            )
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


async def generate_text(
    prompt: str,
    *,
    system_instruction: str,
    temperature: float = 0.3,
    max_output_tokens: int = 1200,
) -> str:
    client = get_client()
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


async def generate_json(
    prompt: str,
    *,
    schema: dict,
    system_instruction: str,
    temperature: float = 0.2,
    max_output_tokens: int = 1800,
) -> str:
    client = get_client()
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    text = response.text
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text.strip()
