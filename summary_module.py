from gemini_client import generate_text


async def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage for quick revision.

Passage:
{text}

Requirements:
- Keep the important facts and relationships.
- Remove repetition and filler.
- Use clear, simple language.
- Prefer a short paragraph followed by bullet points when appropriate.
"""
    return await generate_text(
        prompt,
        system_instruction=(
            "You are an educational summarization assistant. Preserve the meaning "
            "of the supplied material and do not introduce unsupported facts."
        ),
        max_output_tokens=1000,
    )
