import json
from gemini_client import generate_json
from models import QuizQuestion

QUIZ_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "maxItems": 3,
    "items": {
        "type": "object",
        "properties": {
            "question": {"type": "string"},
            "options": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,
                "items": {"type": "string"},
            },
            "correct_answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["question", "options", "correct_answer", "explanation"],
    },
}

SYSTEM = """
You create educational multiple-choice quizzes.
Return exactly three questions, four options per question, and one correct answer.
The correct_answer field must exactly match one of the four option strings.
Questions must be answerable from the supplied passage or topic.
Avoid trick questions and ambiguous options.
"""


async def generate_quiz(text: str) -> list[QuizQuestion]:
    prompt = f"""
Create a three-question MCQ quiz from this material:

{text}

Each question needs exactly four options. Include a short explanation for
the correct answer. Return only the requested JSON structure.
"""
    raw = await generate_json(
        prompt,
        schema=QUIZ_SCHEMA,
        system_instruction=SYSTEM,
        max_output_tokens=1800,
    )

    try:
        data = json.loads(raw)
        questions = [QuizQuestion.model_validate(item) for item in data]
    except Exception as exc:
        raise RuntimeError(f"Quiz JSON could not be validated: {exc}") from exc

    if len(questions) != 3:
        raise RuntimeError("Quiz generation did not return exactly three questions.")

    for question in questions:
        if question.correct_answer not in question.options:
            raise RuntimeError(
                "Quiz generation returned a correct answer not present in its options."
            )
    return questions
