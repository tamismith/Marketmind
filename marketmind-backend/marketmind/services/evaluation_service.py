from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

INTENSIFIERS = {
    "very", "really", "extremely", "highly", "deeply", "super", "incredibly",
    "absolutely", "totally", "definitely", "strongly", "seriously", "exceptionally",
    "remarkably", "terrifically", "unbelievably", "insanely", "wildly", "urgently",
    "massively", "enormously", "immensely", "overwhelmingly", "fiercely", "blazing"
}

ASSERTIVE_WORDS = {
    "must", "start", "book", "buy", "join", "claim", "discover", "upgrade",
    "get", "shop", "now", "today", "act", "grab", "secure", "unlock", "take",
    "demand", "drive", "lead", "own", "dominate", "win", "crush", "achieve",
    "launch", "power", "transform", "accelerate", "guarantee", "proven", "results"
}

HEDGE_WORDS = {
    "maybe", "might", "perhaps", "could", "possibly", "somewhat", "likely",
    "arguably", "generally", "usually", "often", "sometimes", "occasionally",
    "rather", "fairly", "quite", "almost", "nearly", "apparently", "seemingly"
}


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)


def _classify_tone(compound: float) -> tuple[str, str]:
    """
    Returns (tone_key, tone_label) across 7 levels.
    tone_key  — used programmatically (stored in DB, compared to target)
    tone_label — human-readable display string
    """
    if compound >= 0.5:
        return "very_positive", "Very Positive"
    if compound >= 0.2:
        return "positive", "Positive"
    if compound >= 0.05:
        return "slightly_positive", "Slightly Positive"
    if compound > -0.05:
        return "neutral", "Neutral"
    if compound > -0.2:
        return "slightly_negative", "Slightly Negative"
    if compound > -0.5:
        return "negative", "Negative"
    return "very_negative", "Very Negative"


def _tone_category(tone_key: str) -> str:
    """Broad 3-way category kept for backward compatibility."""
    if tone_key in ("very_positive", "positive", "slightly_positive"):
        return "positive"
    if tone_key in ("very_negative", "negative", "slightly_negative"):
        return "negative"
    return "neutral"


def _estimate_arousal(text: str) -> tuple[float, str, str]:
    """Returns (score, arousal_key, arousal_label) across 5 levels."""
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    words = [w for w in words if w]
    if not words:
        return 0.0, "very_low", "Very Low"

    punctuation_boost = min((text.count("!") * 0.08) + (text.count("?") * 0.04), 0.4)
    intensifier_ratio = sum(1 for w in words if w in INTENSIFIERS) / len(words)
    uppercase_chars = sum(1 for c in text if c.isupper())
    alpha_chars = sum(1 for c in text if c.isalpha()) or 1
    uppercase_ratio = uppercase_chars / alpha_chars

    score = _clamp(
        punctuation_boost + (intensifier_ratio * 1.2) + (uppercase_ratio * 1.5),
        0.0, 1.0
    )

    if score >= 0.7:
        return score, "very_high", "Very High"
    if score >= 0.5:
        return score, "high", "High"
    if score >= 0.3:
        return score, "moderate", "Moderate"
    if score >= 0.1:
        return score, "low", "Low"
    return score, "very_low", "Very Low"


def _estimate_dominance(text: str) -> tuple[float, str, str]:
    """Returns (score, dominance_key, dominance_label) across 5 levels."""
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    words = [w for w in words if w]
    if not words:
        return 0.5, "balanced", "Balanced"

    assertive_ratio = sum(1 for w in words if w in ASSERTIVE_WORDS) / len(words)
    hedge_ratio = sum(1 for w in words if w in HEDGE_WORDS) / len(words)

    score = _clamp(0.5 + (assertive_ratio * 1.2) - (hedge_ratio * 1.2), 0.0, 1.0)

    if score >= 0.75:
        return score, "very_assertive", "Very Assertive"
    if score >= 0.6:
        return score, "assertive", "Assertive"
    if score >= 0.4:
        return score, "balanced", "Balanced"
    if score >= 0.25:
        return score, "tentative", "Tentative"
    return score, "very_tentative", "Very Tentative"


def _describe_tone(tone_key: str) -> str:
    descriptions = {
        "very_positive":     "Highly enthusiastic and uplifting — strong positive emotional charge.",
        "positive":          "Warm and encouraging with a clear positive outlook.",
        "slightly_positive": "Mildly optimistic with a gentle positive lean.",
        "neutral":           "Balanced and objective — no strong emotional direction.",
        "slightly_negative": "Cautious or mildly critical in tone.",
        "negative":          "Noticeably negative — leans towards concern or criticism.",
        "very_negative":     "Strongly critical or alarming — high negative emotional charge.",
    }
    return descriptions.get(tone_key, "Balanced and neutral in tone.")


def _describe_arousal(arousal_key: str) -> str:
    descriptions = {
        "very_high": "Extremely high energy — intense, urgent, and highly stimulating.",
        "high":      "High-energy delivery with strong emphasis and excitement.",
        "moderate":  "Moderate energy — active and engaging without being overwhelming.",
        "low":       "Calm and measured delivery with quiet confidence.",
        "very_low":  "Very low energy — subdued, gentle, and understated.",
    }
    return descriptions.get(arousal_key, "Moderate energy with active but controlled emphasis.")


def _describe_dominance(dominance_key: str) -> str:
    descriptions = {
        "very_assertive": "Commanding and authoritative — direct, bold, and action-driven.",
        "assertive":      "Confident and purposeful with a clear call to act.",
        "balanced":       "Balanced voice — neither overly forceful nor passive.",
        "tentative":      "Somewhat soft and uncertain — hedged language present.",
        "very_tentative": "Very passive and hesitant — lacks assertiveness.",
    }
    return descriptions.get(dominance_key, "Moderately confident, balanced voice.")


def evaluate_text(text: str) -> dict:
    if not text or not text.strip():
        return {
            "tone": "neutral",
            "tone_label": "Neutral",
            "tone_category": "neutral",
            "score": 0.0,
            "vad": {
                "valence": 0.0,
                "arousal": 0.0,
                "arousal_label": "Very Low",
                "dominance": 0.5,
                "dominance_label": "Balanced",
            },
            "explanation": {
                "tone_summary": "Balanced and neutral in tone.",
                "energy_summary": "Very low energy — subdued, gentle, and understated.",
                "voice_summary": "Balanced voice — neither overly forceful nor passive.",
            },
        }

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]

    tone_key, tone_label = _classify_tone(compound)
    tone_cat = _tone_category(tone_key)
    valence = _clamp(compound, -1.0, 1.0)

    arousal_score, arousal_key, arousal_label = _estimate_arousal(text)
    dominance_score, dominance_key, dominance_label = _estimate_dominance(text)

    return {
        "tone": tone_key,
        "tone_label": tone_label,
        "tone_category": tone_cat,
        "score": compound,
        "vad": {
            "valence": valence,
            "arousal": arousal_score,
            "arousal_label": arousal_label,
            "dominance": dominance_score,
            "dominance_label": dominance_label,
        },
        "explanation": {
            "tone_summary": _describe_tone(tone_key),
            "energy_summary": _describe_arousal(arousal_key),
            "voice_summary": _describe_dominance(dominance_key),
        },
    }
