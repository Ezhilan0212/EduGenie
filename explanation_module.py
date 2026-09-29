from config import settings
from gemini_client import generate_text


async def _gemini_explanation(text: str) -> str:
    prompt = f"""
Explain the following concept to a beginner.

Concept:
{text}

Requirements:
- Start with a one-sentence definition.
- Explain the idea in simple steps.
- Give one small real-world or academic example.
- Avoid unnecessary jargon.
"""
    return await generate_text(
        prompt,
        system_instruction=(
            "You are an expert teacher. Make difficult concepts easy without "
            "changing their meaning."
        ),
        max_output_tokens=1100,
    )


async def _local_explanation(text: str) -> str:
    # Optional dependency path. The core project does not download a 783M model
    # during normal installation; enable it explicitly with the local requirements.
    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        device=-1,
    )
    prompt = (
        "Explain this educational concept simply with a definition, key points, "
        f"and one example: {text}"
    )
    result = generator(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


async def explain_concept(text: str) -> str:
    if settings.enable_local_explanation:
        try:
            return await _local_explanation(text)
        except Exception:
            # A failed optional local model should not break the application.
            pass
    return await _gemini_explanation(text)
