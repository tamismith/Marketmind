import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_marketing_caption(business_details: str, platform: str) -> str:
    """
    Service: calls OpenAI and applies simple post-processing.
    """
    # For now, keep it simple – later you can refine the prompt.
    prompt = (
        f"Write a short, engaging social media caption for {platform}.\n"
        f"Business details: {business_details}\n"
        "Keep the language clear and friendly for small business customers."
    )

    # PSEUDO-CALL - you'll adapt to the current OpenAI API style you're using
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful marketing assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=120,
    )

    caption = response.choices[0].message["content"].strip()
    return caption
