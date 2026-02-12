from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def evaluate_text(text: str) -> dict:
    if not text or not text.strip():
        return {"tone": "neutral", "score": 0.0}

    scores = _analyzer.polarity_scores(text)
    compound = scores["compound"]#i choose compound because it gives an overall summarise
    if compound >= 0.05:
        tone = "positive"
    elif compound <= -0.05:
        tone = "negative"
    else:
        tone = "neutral"
    return {
    "tone": tone,
    "score": compound
}