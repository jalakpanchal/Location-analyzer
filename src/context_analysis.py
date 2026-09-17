"""
context_analysis.py
--------------------
Semantic & context analysis for each detected location:
  - context window extraction (surrounding sentence(s))
  - event category classification (rule-based keyword classifier)
  - sentiment analysis (VADER)

Rubric mapping: Stage 2 - Implementation & Testing (Implementation Quality,
Technical Role), Stage 3 - Data Analysis & Interpretation
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from preprocessing import segment_sentences
from ner_extraction import extract_locations

_SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()

# Rule-based keyword classifier for event category.
# A production system might swap this for a zero-shot transformer
# (e.g. facebook/bart-large-mnli), but keyword rules are fast, fully
# offline, transparent, and easy to justify/evaluate for a micro-project.
CATEGORY_KEYWORDS = {
    "disaster": [
        "flood", "earthquake", "wildfire", "landslide", "cyclone", "tsunami",
        "drought", "storm", "volcanic", "eruption", "heatwave", "disaster",
        "evacuat", "damage", "snowfall", "displaced",
    ],
    "political": [
        "protest", "government", "election", "parliament", "political",
        "coalition", "diplomatic", "reform", "scandal", "unrest", "rally",
        "opposition", "summit", "sanctions",
    ],
    "economic": [
        "stock", "market", "economic", "economy", "inflation", "trade",
        "unemployment", "funding", "startup", "manufacturing", "growth",
        "recession", "stimulus", "investment",
    ],
    "sports": [
        "football", "cricket", "basketball", "tennis", "marathon",
        "championship", "tournament", "olympic", "match", "league", "team",
    ],
    "health": [
        "health", "vaccin", "disease", "outbreak", "malaria", "hospital",
        "medical", "strike over pay", "medicine", "clinic",
    ],
}


def classify_category(text: str) -> str:
    """
    Rule-based classification of an event category from context text.
    Counts keyword hits per category and returns the top match,
    defaulting to 'other' if nothing matches.
    """
    lowered = text.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                scores[cat] += 1
    best_cat = max(scores, key=scores.get)
    if scores[best_cat] == 0:
        return "other"
    return best_cat


def analyze_sentiment(text: str) -> dict:
    """Return VADER sentiment scores and a simplified label."""
    scores = _SENTIMENT_ANALYZER.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"compound": compound, "label": label}


def get_context_window(text: str, ent_start: int, ent_end: int) -> str:
    """
    Return the sentence (or sentences) in `text` that contain the
    entity span [ent_start, ent_end).
    """
    sentences = segment_sentences(text)
    # Re-walk the original text to find sentence character offsets,
    # since segment_sentences() only returns sentence strings.
    cursor = 0
    context_sentences = []
    for sent in sentences:
        start = text.find(sent, cursor)
        if start == -1:
            continue
        end = start + len(sent)
        cursor = end
        if start <= ent_start < end or start < ent_end <= end:
            context_sentences.append(sent)
    return " ".join(context_sentences) if context_sentences else text


def analyze_article(article_id, text: str) -> list[dict]:
    """
    Full per-article analysis: extract locations, build a context
    window per location, classify event category, and score sentiment.

    Returns a list of result dicts, one per unique location found.
    """
    results = []
    entities = extract_locations(text)
    for ent in entities:
        context = get_context_window(text, ent["start"], ent["end"])
        category = classify_category(context)
        sentiment = analyze_sentiment(context)
        results.append(
            {
                "article_id": article_id,
                "location": ent["normalized"],
                "raw_mention": ent["text"],
                "context": context,
                "event_category": category,
                "sentiment_label": sentiment["label"],
                "sentiment_score": sentiment["compound"],
            }
        )
    return results


if __name__ == "__main__":
    sample = (
        "Heavy monsoon rains caused severe flooding across Mumbai on Tuesday, "
        "submerging low-lying areas. Authorities in Mumbai issued an emergency alert."
    )
    for r in analyze_article(1, sample):
        print(r)
