import os
from openai import OpenAI

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_marketing_text(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str = "",
    goal: str = "",
    length: str = "short"
) -> str:
    """
    Generates AI marketing text based on business input.
    """

    # Decide output length
    length_instruction = {
        "short": "1–2 sentences",
        "medium": "3–4 sentences"
    }.get(length.lower(), "1–2 sentences")

    # Build the prompt
    prompt = f"""
You are an AI marketing assistant for small businesses.

Write a {length_instruction} marketing caption for {platform}.
Business name: {business_name}
Industry: {industry}
Target audience: {target_audience}
Tone: {tone}
Description: {description}
Goal: {goal if goal else "Increase engagement"}

Requirements:
- Keep the language clear and simple
- Avoid jargon
- Make it suitable for small business marketing
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You help small businesses create marketing content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "Unable to generate content at this time."
