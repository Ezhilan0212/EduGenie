from gemini_client import generate_text


async def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""
Create a structured learning path for:

Topic: {topic}
Learner level: {level}

Include:
1. Prerequisites.
2. Beginner foundations.
3. Intermediate topics.
4. Advanced topics.
5. A suggested timeline.
6. Practice activities or mini-projects.
7. Recommended resource types (videos, documentation, books, courses).

Keep it practical and ordered from easier to harder.
Do not invent specific URLs.
"""
    return await generate_text(
        prompt,
        system_instruction=(
            "You are a curriculum designer. Build realistic, learner-friendly "
            "study paths with progressive difficulty."
        ),
        max_output_tokens=1600,
    )
