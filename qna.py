from gemini_client import generate_text

SYSTEM = """
You are EduGenie, a careful educational assistant.
Answer academic questions clearly and concisely.
Use simple language suitable for a learner unless the question requires technical depth.
Do not invent citations, facts, or references.
If a question is ambiguous, state the assumption you are making.
Prefer short headings or bullet points when they improve readability.
"""

async def answer_question(question: str) -> str:
    prompt = f"""
Answer this student's question:

{question}

Give the direct answer first, then a short explanation or example if useful.
"""
    return await generate_text(prompt, system_instruction=SYSTEM, max_output_tokens=900)
