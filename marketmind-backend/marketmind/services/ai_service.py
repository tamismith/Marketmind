from .ai_provider import (
    AIProvider,
    AIProviderError,
    ImageGenerationRequest,
    TextGenerationRequest,
)
import hashlib


ai_provider = AIProvider()


TEXT_STYLE_PRESETS = {
    "instagram": "vivid, sensory, upbeat, community-first",
    "facebook": "warm, relatable, trust-building, practical",
    "linkedin": "professional, confident, value-focused, concise",
    "twitter/x": "punchy, sharp, memorable, high energy",
}

PLATFORM_RULES = {
    "instagram": """
- Write with lifestyle energy and visual language.
- Keep it emotionally expressive and friendly.
- You may use at most 1 emoji if it feels natural.
- Keep sentence flow conversational and human.
- Structure: Hook sentence -> sensory/detail sentence -> light CTA.
""",
    "linkedin": """
- Write with professional clarity and business relevance.
- Focus on credibility, outcomes, and practical value.
- Do not use emojis.
- Keep tone polished and concise, suitable for a business audience.
- Structure: professional insight -> value/outcome statement -> business CTA.
""",
    "facebook": """
- Write in a warm, community-driven voice.
- Keep it practical and relatable for everyday readers.
- Emojis are optional but minimal.
""",
    "twitter/x": """
- Keep copy punchy and high-impact.
- Prioritize brevity and strong phrasing.
- No emojis unless explicitly requested.
""",
}

REGION_RULES = {
    "uk": """
- Use UK English spelling (e.g., organise, personalised, favourite).
- Keep references locally natural for UK audiences; avoid US-first phrasing.
- CTA tone should feel polite and understated.
""",
    "united kingdom": """
- Use UK English spelling (e.g., organise, personalised, favourite).
- Keep references locally natural for UK audiences; avoid US-first phrasing.
- CTA tone should feel polite and understated.
""",
    "us": """
- Use US English spelling (e.g., organize, personalized, favorite).
- Keep messaging direct and benefit-forward.
- CTA tone can be confident and action-oriented.
""",
    "usa": """
- Use US English spelling (e.g., organize, personalized, favorite).
- Keep messaging direct and benefit-forward.
- CTA tone can be confident and action-oriented.
""",
    "united states": """
- Use US English spelling (e.g., organize, personalized, favorite).
- Keep messaging direct and benefit-forward.
- CTA tone can be confident and action-oriented.
""",
    "canada": """
- Use Canadian English spelling and neutral North American phrasing.
- Keep tone warm, practical, and community-aware.
- Avoid niche US-only references.
""",
    "australia": """
- Use Australian English spelling and natural local phrasing.
- Keep the tone straightforward, conversational, and down-to-earth.
- Avoid US-only idioms and references.
""",
    "india": """
- Use clear international English with India-appropriate phrasing.
- Keep examples culturally broad and locally relatable.
- Avoid regionally inaccurate assumptions or stereotypes.
""",
}

IMAGE_STYLE_PRESETS = [
    "Editorial lifestyle photo with cinematic framing and soft film grain.",
    "Modern commercial campaign shot with bold composition and rich contrast.",
    "Minimalist premium product scene with clean geometry and intentional negative space.",
    "Human-centered candid brand moment with natural motion and authentic imperfection.",
]

PLATFORM_IMAGE_BASELINES = {
    "linkedin": {
        "voice": "professional, corporate, polished, credibility-focused",
        "creativity_bias": "low",
    },
    "instagram": {
        "voice": "visual-first, lifestyle-rich, expressive, emotionally resonant",
        "creativity_bias": "high",
    },
    "facebook": {
        "voice": "community-friendly, warm, practical, relatable",
        "creativity_bias": "medium",
    },
    "twitter/x": {
        "voice": "punchy, modern, bold, fast-scrolling attention capture",
        "creativity_bias": "medium-high",
    },
}

IMAGE_CREATIVITY_OPTIONS = [
    {
        "id": "safe",
        "label": "Safe",
        "instruction": "Conservative, clear composition, restrained styling, minimal artistic risk.",
    },
    {
        "id": "balanced",
        "label": "Balanced",
        "instruction": "Moderate creativity, attractive visual storytelling, still commercially safe.",
    },
    {
        "id": "bold",
        "label": "Bold",
        "instruction": "High creativity with stronger visual contrast and expressive composition.",
    },
    {
        "id": "experimental",
        "label": "Experimental",
        "instruction": "Most creative option: stylized mood, unconventional framing, high visual personality.",
    },
]


def _choose_image_style_seed(*parts: str) -> str:
    seed = "|".join(parts).encode("utf-8")
    index = int(hashlib.md5(seed).hexdigest(), 16) % len(IMAGE_STYLE_PRESETS)
    return IMAGE_STYLE_PRESETS[index]


def _platform_rule_block(platform_key: str) -> str:
    return PLATFORM_RULES.get(
        platform_key,
        """
- Match tone and style to the selected platform.
- Keep wording clear and natural.
""",
    )


def _platform_output_shape(platform_key: str) -> str:
    if platform_key == "instagram":
        return """
- Sentence 1: bold lifestyle hook.
- Sentence 2: concrete sensory scene/detail tied to audience benefit.
- Sentence 3 (or end of sentence 2 for short mode): soft CTA.
"""
    if platform_key == "linkedin":
        return """
- Sentence 1: professional market/customer insight.
- Sentence 2: clear value proposition or business outcome.
- Sentence 3 (or end of sentence 2 for short mode): clear business CTA.
"""
    return """
- Keep a clear beginning, middle (value), and end CTA.
"""


def _region_rule_block(region: str) -> str:
    region_key = region.strip().lower()
    return REGION_RULES.get(
        region_key,
        """
- Match spelling and phrasing to the specified region.
- Keep cultural references neutral unless clearly relevant.
- Avoid assumptions that conflict with local context.
""",
    )


def _region_visual_cues(region: str) -> str:
    region_key = region.strip().lower()
    cues = {
        "uk": "subtle UK urban streetscape cues, soft overcast natural light, everyday high-street realism",
        "united kingdom": "subtle UK urban streetscape cues, soft overcast natural light, everyday high-street realism",
        "us": "clean North American storefront context, brighter directional daylight, modern lifestyle composition",
        "usa": "clean North American storefront context, brighter directional daylight, modern lifestyle composition",
        "united states": "clean North American storefront context, brighter directional daylight, modern lifestyle composition",
        "canada": "community-centered neighborhood context, natural seasonal realism, balanced warm-cool tones",
        "australia": "sunlit outdoor-friendly context, airy composition, natural vibrant but realistic color grade",
        "india": "locally relatable urban context, rich but controlled colors, authentic everyday environment",
    }
    return cues.get(
        region_key,
        "local context should feel authentic to the specified region with realistic environmental cues",
    )


def _platform_image_baseline(platform: str) -> dict:
    return PLATFORM_IMAGE_BASELINES.get(
        platform.strip().lower(),
        {
            "voice": "clean, audience-aware, commercial social content",
            "creativity_bias": "medium",
        },
    )

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
        "short": "1-2 sentences",
        "medium": "3-4 sentences"
    }.get(length.lower(), "1-2 sentences")
    platform_key = platform.strip().lower()
    platform_style = TEXT_STYLE_PRESETS.get(platform_key, "clear, modern, audience-aware, creative")
    platform_rules = _platform_rule_block(platform_key)
    platform_shape = _platform_output_shape(platform_key)
    region_rules = _region_rule_block(region)

    prompt = f"""
You are a senior creative strategist for SME marketing campaigns.

Write one platform-ready caption for {platform} with a distinct voice.

Context:
- Business: {business_name}
- Industry: {industry}
- Offer summary: {description}
- Audience: {target_audience}
- Goal: {goal if goal else "Increase engagement"}
- Tone: {tone}
- Region: {region}
- Length: {length_instruction}

Creative direction:
- Style profile: {platform_style}
- Use one vivid image, detail, or scene to make the copy feel concrete.
- Emphasize one clear benefit for the audience.
- End with a subtle but actionable call to action.

Platform-specific execution:
{platform_rules}

Regional adaptation:
{region_rules}

Output shape:
{platform_shape}

Quality guardrails:
- Plain, natural language.
- Region-appropriate spelling and phrasing.
- No exaggerated claims.
- No hashtags unless explicitly requested.
- Do not mention AI.
- Avoid repetitive sentence rhythm.

Output:
Return only the final caption text. No labels, bullets, or quotes.
"""

    try:
        request = TextGenerationRequest(
            system_prompt="You help small businesses create marketing content.",
            user_prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return ai_provider.generate_text(request)
    except AIProviderError:
        return "Unable to generate content at this time."


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
        "short": "1-2 sentences",
        "medium": "3-4 sentences"
    }.get(length.lower(), "1-2 sentences")
    platform_key = platform.strip().lower()
    platform_style = TEXT_STYLE_PRESETS.get(platform_key, "direct, energetic, conversion-focused")
    platform_rules = _platform_rule_block(platform_key)
    platform_shape = _platform_output_shape(platform_key)
    region_rules = _region_rule_block(region)

    text_prompt = f"""
You are an expert performance marketing copywriter for small businesses.

Write {length_instruction} ad copy for {platform}.
The copy should be benefit-led, specific, and conversion-focused.

Business name: {business_name}
Industry: {industry}
Description: {description}
Target audience: {target_audience}
Tone: {tone}
Region: {region}
Goal: {goal if goal else "Increase conversions"}
Offer: {offer if offer else "None"}
Call to action: {cta if cta else "Use a natural call to action"}
Style profile: {platform_style}

Rules:
- Clear and simple language
- No exaggerated claims
- No hashtags
- Do not mention AI
- Include one concrete detail that makes the ad feel real, not generic
- End with one strong action line
Platform-specific execution:
{platform_rules}
Regional adaptation:
{region_rules}
Output shape:
{platform_shape}

Return only the ad copy text.
"""

    try:
        text_request = TextGenerationRequest(
            system_prompt="You write effective ad copy for small businesses.",
            user_prompt=text_prompt,
            max_tokens=180,
            temperature=0.7,
        )
        ad_copy = ai_provider.generate_text(text_request)
    except AIProviderError as e:
        print("GPT ERROR:", e)
        ad_copy = "Unable to generate ad copy at this time."

    
    image_base64 = ""
    image_options = []

    selected_image_style = _choose_image_style_seed(
        business_name, industry, platform, target_audience, tone
    )
    regional_visual_cues = _region_visual_cues(region)
    platform_baseline = _platform_image_baseline(platform)

    base_image_prompt: str = f"""
Creative social media campaign image for a small business.

Brand context:
- Business: {business_name}
- Industry: {industry}
- Offer summary: {description}
- Audience: {target_audience}
- Tone: {tone}
- Region: {region}

Art direction:
- {selected_image_style}
- Platform baseline ({platform}): {platform_baseline["voice"]}.
- Default creativity level for this platform is {platform_baseline["creativity_bias"]}; keep outputs platform-appropriate.
- Make the scene feel story-driven and emotionally resonant.
- Use a strong focal subject with layered depth.
- Add tactile details and natural imperfection for realism.
- Keep visual mood aligned with audience expectations for {platform}.
- Regional cues: {regional_visual_cues}.

Lighting and composition:
- Natural cinematic light, controlled highlights, realistic shadows.
- Rule-of-thirds composition with clean negative space for social layout.
- Premium commercial quality, not stock-photo stiffness.

Strict constraints:
- No text, no letters, no logos, no watermark, no signage.
- No distorted hands, faces, or anatomy.
"""

    for option in IMAGE_CREATIVITY_OPTIONS:
        option_prompt = f"""
{base_image_prompt}

Creativity mode:
- Option: {option["label"]} ({option["id"]})
- {option["instruction"]}
"""
        try:
            image_request = ImageGenerationRequest(prompt=option_prompt)
            generated_image = ai_provider.generate_image_base64(image_request)
            if generated_image:
                image_options.append(
                    {
                        "id": option["id"],
                        "label": option["label"],
                        "creativity_level": option["id"],
                        "image_base64": generated_image,
                        "platform_alignment": platform_baseline["voice"],
                    }
                )
        except AIProviderError as e:
            print(f"STABILITY IMAGE ERROR ({option['id']}):", e)

    if image_options:
        image_base64 = image_options[0]["image_base64"]

    
    # -------------------------
    return {
        "ad_copy": ad_copy,
        "image_base64": image_base64,
        "image_options": image_options,
    }
