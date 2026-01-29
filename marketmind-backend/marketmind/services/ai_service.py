import os
import requests
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()

# Create OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def generate_marketing_text(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str = "",
    goal: str = "",
    region: str = "UK",
    length: str = "short",
) -> str:
    length_instruction = {
        "short": "1–2 sentences",
        "medium": "3–4 sentences"
    }.get(length.lower(), "1–2 sentences")

    prompt = f"""
You are a highly skilled AI marketing assistant specialising in small and medium-sized businesses (SMEs).
You understand how to create engaging, practical, and platform-appropriate marketing content that helps
businesses connect with their audience without sounding corporate or overly technical.

TASK:
Write a {length_instruction} marketing caption specifically for {platform}.

BUSINESS CONTEXT:
- Business name: {business_name}
- Industry: {industry}
- Description: {description}
- Target audience: {target_audience}
- Primary marketing goal: {goal if goal else "Increase engagement"}
- Desired tone: {tone}
- Target region or market: {region}

CONTENT GUIDELINES:
- Use clear, simple language that is easy to understand.
- Avoid technical jargon or complex marketing terms.
- Write in a friendly, human, and natural style.
- Make it suitable for a small business rather than a large corporation.

REGIONAL & CULTURAL ADAPTATION:
- Tailor spelling and phrasing to suit the target region.
- Avoid slang or references that would feel unfamiliar or inappropriate.

PLATFORM-SPECIFIC RULES:
- Adapt the writing style to suit {platform}.
- Instagram/Facebook: conversational; emojis sparingly if appropriate.
- LinkedIn: professional and approachable; avoid emojis unless appropriate.
- Twitter/X: concise and impactful.

STRUCTURE REQUIREMENTS:
- Start with an attention-grabbing line.
- Highlight the main value or benefit.
- End with a subtle call-to-action.

STYLE CONSTRAINTS:
- Do not use excessive punctuation or emojis.
- Do not use dashes (-) as punctuation.
- Avoid unrealistic claims.
- Avoid hashtags unless explicitly requested.
- Do not mention AI.

OUTPUT FORMAT:
Return only the final caption text.
"""

    try:
        response = openai_client.chat.completions.create(
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

    



client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


def generate_ad_text(
    business_name: str,
    industry: str,
    target_audience: str,
    tone: str,
    platform: str,
    description: str = "",
    goal: str = "",
    region: str = "UK",
    length: str = "short",
    offer: str = "",
    cta: str = ""
) -> dict:
    """
    Generates conversion-focused ad copy using GPT
    and a matching marketing image using Stability AI.
    """

    # -------------------------
    # 1. Generate ad copy text
    # -------------------------
    length_instruction = {
        "short": "1–2 sentences",
        "medium": "3–4 sentences"
    }.get(length.lower(), "1–2 sentences")

    text_prompt = f"""
You are an expert performance marketing copywriter for small businesses.

Write {length_instruction} ad copy for {platform}.
The copy should be direct, benefit-led, and focused on encouraging action.

Business name: {business_name}
Industry: {industry}
Description: {description}
Target audience: {target_audience}
Tone: {tone}
Region: {region}
Goal: {goal if goal else "Increase conversions"}
Offer: {offer if offer else "None"}
Call to action: {cta if cta else "Use a natural call to action"}

Rules:
- Clear and simple language
- No exaggerated claims
- No hashtags
- No dashes (-) as punctuation
- Do not mention AI

Return only the ad copy text.
"""

    try:
        text_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write effective ad copy for small businesses."},
                {"role": "user", "content": text_prompt}
            ],
            max_tokens=180,
            temperature=0.7
        )
        ad_copy = text_response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:", e)
        ad_copy = "Unable to generate ad copy at this time."

    
    image_base64 = ""

    image_prompt: str = f"""

Professional social media advertisement image for a small business.

Scene:
A modern, welcoming {industry.lower()} environment.
The main product or service is clearly visible in the foreground.

Composition:
Clean, uncluttered composition.
Subject centered and well framed.
Background softly blurred to keep focus on the product or service.

Lighting:
Bright natural lighting.
Warm, inviting tones.
Friendly and approachable mood.

Business context:
{description}

Target audience:
Designed to appeal to {target_audience}.
Feels relatable and realistic, not staged.

Style:
High-quality commercial photography.
Instagram-ready aesthetic.
Modern, professional, and polished.

Constraints:
No text.
No logos.
No watermarks.
No visible writing.
"""


    try:
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json={
                "text_prompts": [{"text": image_prompt}],
                "cfg_scale": 7,
                "steps": 30,
                "samples": 1,
                "height": 1024,
                "width": 1024
            },
            timeout=60
        )

        if response.status_code == 200:
            image_base64 = response.json()["artifacts"][0]["base64"]
        else:
            print("STABILITY STATUS:", response.status_code)
            print("STABILITY ERROR:", response.text)

    except Exception as e:
        print("STABILITY IMAGE ERROR:", e)

    
    # -------------------------
    return {
        "ad_copy": ad_copy,
        "image_base64": image_base64
    }


