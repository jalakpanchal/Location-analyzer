"""
preprocessing.py
----------------
Text cleaning and sentence segmentation utilities for the
Location Entity Extraction & News Context Analyzer.

Rubric mapping: Stage 2 - Implementation & Testing (Implementation Quality)
"""

import re
import string
import spacy

# Load a single shared spaCy pipeline instance for sentence
# segmentation + NER (loaded lazily so importing this module is cheap).
_NLP = None


def get_nlp():
    """Lazily load and cache the spaCy English pipeline."""
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def clean_text(text: str) -> str:
    """
    Basic text cleaning: lowercase, strip extra whitespace,
    remove stray punctuation that doesn't help NER (keep periods
    since spaCy uses them for sentence boundaries).
    """
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    # Remove punctuation that is not a sentence terminator, but keep
    # capitalization intact since spaCy's NER relies on casing cues.
    keep_chars = string.ascii_letters + string.digits + " .,!?'-"
    text = "".join(ch for ch in text if ch in keep_chars)
    return text


def lowercase_for_matching(text: str) -> str:
    """Lowercased copy used only for keyword/category matching,
    never for NER (NER needs original casing)."""
    return text.lower()


def segment_sentences(text: str) -> list[str]:
    """Split article text into a list of sentences using spaCy."""
    nlp = get_nlp()
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation-aware tokenizer using spaCy."""
    nlp = get_nlp()
    doc = nlp(text)
    return [tok.text for tok in doc if not tok.is_space]


if __name__ == "__main__":
    sample = "Heavy monsoon rains caused severe flooding across Mumbai on Tuesday. Authorities issued an emergency alert."
    print("Cleaned:", clean_text(sample))
    print("Sentences:", segment_sentences(sample))
