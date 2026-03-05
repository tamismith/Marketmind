from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

INTENSIFIERS = {
    "very", "really", "extremely", "highly", "deeply", "super", "incredibly",
    "absolutely", "totally", "definitely", "strongly", "seriously"
}
ASSERTIVE_WORDS = {
    "must", "start", "book", "buy", "join", "claim", "discover", "upgrade",
    "get", "shop", "now", "today"
}
HEDGE_WORDS = {
    "maybe", "might", "perhaps", "could", "possibly", "somewhat", "likely"
}


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)


def _estimate_arousal(text: str) -> float:
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    words = [w for w in words if w]
    if not words:
        return 0.0

    punctuation_boost = min((text.count("!") * 0.08) + (text.count("?") * 0.04), 0.4)
    intensifier_ratio = sum(1 for w in words if w in INTENSIFIERS) / len(words)
    uppercase_chars = sum(1 for c in text if c.isupper())
    alpha_chars = sum(1 for c in text if c.isalpha()) or 1
    uppercase_ratio = uppercase_chars / alpha_chars

    arousal = (punctuation_boost + (intensifier_ratio * 1.2) + (uppercase_ratio * 1.5))
    return _clamp(arousal, 0.0, 1.0)


def _estimate_dominance(text: str) -> float:
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    words = [w for w in words if w]
    if not words:
        return 0.0

    assertive_ratio = sum(1 for w in words if w in ASSERTIVE_WORDS) / len(words)
    hedge_ratio = sum(1 for w in words if w in HEDGE_WORDS) / len(words)

    dominance = 0.5 + (assertive_ratio * 1.2) - (hedge_ratio * 1.2)
    return _clamp(dominance, 0.0, 1.0)


def _describe_tone(tone: str, score: float) -> str:
    if tone == "positive":
        if score >= 0.7:
            return "Strongly upbeat and encouraging."
        return "Positive and supportive in tone."
    if tone == "negative":
        if score <= -0.7:
            return "Strongly critical or cautionary in tone."
        return "Leans negative or caution-focused."
    return "Balanced and neutral in tone."


def _describe_arousal(arousal: float) -> str:
    if arousal >= 0.66:
        return "High-energy delivery with strong intensity."
    if arousal >= 0.33:
        return "Moderate energy with active but controlled emphasis."
    return "Calm and low-intensity delivery."


def _describe_dominance(dominance: float) -> str:
    if dominance >= 0.66:
        return "Confident and assertive voice."
    if dominance >= 0.33:
        return "Moderately confident, balanced voice."
    return "Soft and tentative voice."


def evaluate_text(text: str) -> dict:
    if not text or not text.strip():
        return {
            "tone": "neutral",
            "score": 0.0,
            "vad": {"valence": 0.0, "arousal": 0.0, "dominance": 0.0},
            "explanation": {
                "tone_summary": "Balanced and neutral in tone.",
                "energy_summary": "Calm and low-intensity delivery.",
                "voice_summary": "Moderately confident, balanced voice.",
            },
        }

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]#i choose compound because it gives an overall summarise
    if compound >= 0.05:
        tone = "positive"
    elif compound <= -0.05:
        tone = "negative"
    else:
        tone = "neutral"
    valence = _clamp(compound, -1.0, 1.0)
    arousal = _estimate_arousal(text)
    dominance = _estimate_dominance(text)

    return {
        "tone": tone,
        "score": compound,
        "vad": {
            "valence": valence,
            "arousal": arousal,
            "dominance": dominance,
        },
        "explanation": {
            "tone_summary": _describe_tone(tone, compound),
            "energy_summary": _describe_arousal(arousal),
            "voice_summary": _describe_dominance(dominance),
        },
    }
