from .ai_provider import (
    AIProvider,
    AIProviderError,
    ImageGenerationRequest,
    TextGenerationRequest,
)
import hashlib
import logging
import time

logger = logging.getLogger(__name__)


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

PALETTE_PRESETS = {
    "earthy": "earthy tones (olive, warm brown, beige), natural muted saturation",
    "pastel": "soft pastel tones, gentle contrast, light airy color mood",
    "vibrant": "vibrant saturated colors with strong but controlled contrast",
    "corporate_blue": "corporate blue-led palette with neutral grays and clean whites",
    "warm": "warm palette with amber, coral, and soft golden highlights",
    "cool": "cool palette with blue/teal tones and crisp low-warmth balance",
    "monochrome": "monochrome palette with tonal depth and grayscale discipline",
}

LOGO_STYLE_PRESETS = {
    "minimal": "flat 2D vector icon, minimal lines, single colour or two-tone, lots of negative space, clean and simple",
    "modern": "modern flat vector logo mark, geometric precision, bold clean shapes, strong contrast, professional app icon aesthetic",
    "bold": "bold graphic logo mark, thick strokes, high contrast colours, strong and impactful, solid shapes",
    "classic": "classic emblem-style logo mark, balanced symmetry, refined details, timeless professional look",
}

LOGO_FEELING_PRESETS = {
    "premium": "sophisticated, high-end, luxurious feel",
    "playful": "fun, friendly, approachable energy",
    "trustworthy": "reliable, solid, professional credibility",
    "bold": "strong, confident, impactful presence",
    "calm": "peaceful, gentle, soft and serene",
    "energetic": "dynamic, vibrant, high-energy movement",
}

LOGO_SHAPE_PRESETS = {
    "abstract": "abstract mark with unique non-representational form",
    "monogram": "letter or monogram-based mark, typographic identity",
    "geometric": "precise geometric shapes, clean angular or circular forms",
    "nature": "nature-inspired organic shapes, leaf, wave, or plant motif",
    "badge": "badge or emblem style, contained circular or shield composition",
    "icon": "simple recognisable icon or object symbol",
}

LOGO_COLOUR_PRESETS = {
    "teal_white": "teal and white colour palette",
    "navy_gold": "navy blue and gold colour palette",
    "black_white": "black and white monochrome palette",
    "earthy": "earthy tones, olive, warm brown, beige",
    "pastels": "soft pastel tones, gentle and light",
    "vibrant": "vibrant saturated bold colours",
    "monochrome": "single colour monochrome with tonal depth",
}

STYLE_PRESET_RULES = {
    "realistic": "photorealistic style, natural textures, commercially authentic details",
    "bold": "bold visual style, stronger contrast, more expressive art direction",
    "minimal": "minimal visual style, clean composition, reduced clutter and focused subject",
    "warm": "warm visual style, inviting mood, soft highlight glow and approachable tone",
}

SHOT_TYPE_RULES = {
    "close_up": "close-up framing that emphasizes subject detail and texture",
    "medium": "medium shot framing with balanced subject and contextual background",
    "wide": "wide shot framing that shows environment and setting context",
}

ASPECT_RATIO_DIMENSIONS = {
    "1:1": (1024, 1024),
    "4:5": (896, 1152),
    "16:9": (1344, 768),
}


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


def _palette_instruction(color_palette: str) -> str:
    if not color_palette or not color_palette.strip():
        return "No explicit palette provided; keep color grading platform-appropriate and realistic."
    palette_key = color_palette.strip().lower()
    preset = PALETTE_PRESETS.get(palette_key)
    if preset:
        return f"Use this color palette direction: {preset}."
    return (
        f"Use this user-defined color palette direction: {color_palette.strip()}. "
        "Respect it while keeping visual realism and brand appropriateness."
    )


def _style_preset_instruction(style_preset: str) -> str:
    return STYLE_PRESET_RULES.get(
        (style_preset or "").strip().lower(),
        STYLE_PRESET_RULES["realistic"],
    )


def _shot_type_instruction(shot_type: str) -> str:
    return SHOT_TYPE_RULES.get(
        (shot_type or "").strip().lower(),
        SHOT_TYPE_RULES["medium"],
    )


def _aspect_ratio_dimensions(aspect_ratio: str) -> tuple[int, int]:
    return ASPECT_RATIO_DIMENSIONS.get(aspect_ratio, ASPECT_RATIO_DIMENSIONS["1:1"])


def _normalize_keywords(value) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value or "")
    return [part.strip() for part in text.split(",") if part.strip()]


def _is_timeout_error(exc: Exception) -> bool:
    text = str(exc).lower()
    return "status=504" in text or "gateway time-out" in text or "gateway timeout" in text


def _fallback_dimensions(width: int, height: int, scale: float = 0.75) -> tuple[int, int]:
    fallback_w = max(512, int(width * scale))
    fallback_h = max(512, int(height * scale))
    return fallback_w, fallback_h

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
    vad_instruction: str = "",
    campaign_instruction: str = "",
    temperature: float = 0.7,
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

    emotional_target_section = (
        f"\nEmotional target:\n{vad_instruction}\n"
        if vad_instruction else ""
    )
    campaign_section = (
        f"\nCampaign context:\n{campaign_instruction}\n"
        if campaign_instruction else ""
    )

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
{campaign_section}{emotional_target_section}
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
            temperature=temperature,
        )
        return ai_provider.generate_text(request)
    except AIProviderError as e:
        logger.error("TEXT GENERATION ERROR: %s", e)
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
    cta: str = "",
    color_palette: str = "",
    high_quality: bool = True,
    style_preset: str = "realistic",
    aspect_ratio: str = "1:1",
    shot_type: str = "medium",
    include_keywords="",
    avoid_keywords="",
    vad_instruction: str = "",
    campaign_instruction: str = "",
    text_only: bool = False,
) -> dict:
    """
    Generates conversion-focused ad copy using GPT
    and a matching marketing image using Stability AI.
    Pass text_only=True to skip image generation and return only ad_copy.
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

    emotional_target_section = (
        f"\nEmotional target:\n{vad_instruction}\n"
        if vad_instruction else ""
    )

    campaign_section = (
        f"\nCampaign context:\n{campaign_instruction}\n"
        if campaign_instruction else ""
    )

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
{campaign_section}{emotional_target_section}
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
        logger.error("GPT ERROR: %s", e)
        ad_copy = "Unable to generate ad copy at this time."

    if text_only:
        return {"ad_copy": ad_copy, "image_base64": "", "image_options": [], "image_warnings": []}

    image_base64 = ""
    image_options = []

    selected_image_style = _choose_image_style_seed(
        business_name, industry, platform, target_audience, tone
    )
    regional_visual_cues = _region_visual_cues(region)
    platform_baseline = _platform_image_baseline(platform)
    palette_instruction = _palette_instruction(color_palette)
    style_preset_instruction = _style_preset_instruction(style_preset)
    shot_type_instruction = _shot_type_instruction(shot_type)
    image_width, image_height = _aspect_ratio_dimensions(aspect_ratio)
    include_list = _normalize_keywords(include_keywords)
    avoid_list = _normalize_keywords(avoid_keywords)
    include_line = ", ".join(include_list) if include_list else "None"
    avoid_line = ", ".join(avoid_list) if avoid_list else "None"

    quality_instruction = (
        "Prioritize sharp commercial detail, clean edge definition, and crisp focus."
        if high_quality
        else "Keep quality acceptable while optimizing for faster generation."
    )

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
- Color palette direction: {palette_instruction}
- Style preset direction: {style_preset_instruction}
- Shot type direction: {shot_type_instruction}
- Make the scene feel story-driven and emotionally resonant.
- Use a strong focal subject with layered depth.
- Add tactile details and natural imperfection for realism.
- Keep visual mood aligned with audience expectations for {platform}.
- Regional cues: {regional_visual_cues}.
- Include these visual elements if natural: {include_line}
- Avoid these visual elements: {avoid_line}

Lighting and composition:
- Natural cinematic light, controlled highlights, realistic shadows.
- Rule-of-thirds composition with clean negative space for social layout.
- Premium commercial quality, not stock-photo stiffness.
- Quality mode: {quality_instruction}

Strict constraints:
- No text, no letters, no logos, no watermark, no signage.
- No distorted hands, faces, or anatomy.
"""

    image_warnings = []

    
    # -------------------------
    for option in IMAGE_CREATIVITY_OPTIONS:
        option_prompt = f"""
{base_image_prompt}

Creativity mode:
- Option: {option["label"]} ({option["id"]})
- {option["instruction"]}
"""

        primary_cfg = 8 if high_quality else 7
        primary_steps = 40 if high_quality else 30
        fallback_w, fallback_h = _fallback_dimensions(image_width, image_height)

        attempts = [
            {"cfg_scale": primary_cfg, "steps": primary_steps, "width": image_width, "height": image_height},
            {"cfg_scale": 7, "steps": 30, "width": image_width, "height": image_height},
            {"cfg_scale": 7, "steps": 26, "width": fallback_w, "height": fallback_h},
        ]

        for attempt_index, attempt in enumerate(attempts):
            try:
                image_request = ImageGenerationRequest(
                    prompt=option_prompt,
                    width=attempt["width"],
                    height=attempt["height"],
                    cfg_scale=attempt["cfg_scale"],
                    steps=attempt["steps"],
                )
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
                break
            except AIProviderError as e:
                if attempt_index < len(attempts) - 1 and _is_timeout_error(e):
                    time.sleep(0.35 * (attempt_index + 1))
                    continue
                image_warnings.append(
                    f"{option['id']}: {str(e)}"
                )
                logger.error("STABILITY IMAGE ERROR (%s): %s", option['id'], e)
                break

    if image_options:
        image_base64 = image_options[0]["image_base64"]

    return {
        "ad_copy": ad_copy,
        "image_base64": image_base64,
        "image_options": image_options,
        "image_warnings": image_warnings,
    }


def generate_logo_image(
    description: str,
    style: str = "minimal",
    feeling: str = "",
    shape: str = "",
    colours: str = "",
) -> str:
    style_instruction = LOGO_STYLE_PRESETS.get(style.strip().lower(), LOGO_STYLE_PRESETS["minimal"])
    feeling_line = f"- Emotional feel: {LOGO_FEELING_PRESETS[feeling]}" if feeling in LOGO_FEELING_PRESETS else ""
    shape_line = f"- Shape/symbol direction: {LOGO_SHAPE_PRESETS[shape]}" if shape in LOGO_SHAPE_PRESETS else ""
    colour_line = f"- Colour palette: {LOGO_COLOUR_PRESETS[colours]}" if colours in LOGO_COLOUR_PRESETS else ""

    extra_context = "\n".join(filter(None, [feeling_line, shape_line, colour_line]))

    image_prompt = f"""
Professional brand logo icon for a {description}.
Style: {style_instruction}.
{extra_context}

The logo must be:
- A single clean icon or symbol, centred on a plain white background
- Flat 2D vector-style illustration, not photorealistic
- Simple enough to work as an app icon or favicon
- One strong recognisable shape — not a collage or scene
- Solid fills, clean edges, no gradients unless part of the style
- Isolated symbol only — no surrounding decoration, no frames, no badges unless badge style was requested

This is a logo icon — NOT a photograph, NOT a scene, NOT a pattern, NOT abstract art.
Think: Airbnb, Spotify, Dropbox — a single clean recognisable mark.

Strict: no text, no letters, no words, no numbers, no watermarks, plain white background only.
"""
    try:
        image_request = ImageGenerationRequest(
            prompt=image_prompt,
            width=1024,
            height=1024,
            cfg_scale=12,
            steps=45,
        )
        return ai_provider.generate_image_base64(image_request)
    except AIProviderError as e:
        logger.error("LOGO GENERATION ERROR: %s", e)
        try:
            fallback = ImageGenerationRequest(
                prompt=image_prompt,
                width=512,
                height=512,
                cfg_scale=10,
                steps=35,
            )
            return ai_provider.generate_image_base64(fallback)
        except AIProviderError:
            return ""
