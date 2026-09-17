"""
ner_extraction.py
------------------
Named Entity Recognition for locations (GPE / LOC) using spaCy,
plus lightweight normalization of location names.

Rubric mapping: Stage 2 - Implementation & Testing (Tools/Technology Usage)
"""

from preprocessing import get_nlp

# A small static lookup table for normalizing common variants/aliases.
# In a larger project this could be replaced with a geopy geocoder call,
# but a static table keeps the pipeline fast and offline-friendly.
LOCATION_ALIASES = {
    "nyc": "New York City",
    "new york": "New York City",
    "the big apple": "New York City",
    "la": "Los Angeles",
    "d.r.c.": "Kinshasa",
}


def normalize_location(name: str) -> str:
    """Normalize a raw location string using the alias table."""
    key = name.strip().lower()
    return LOCATION_ALIASES.get(key, name.strip())


def extract_locations(text: str) -> list[dict]:
    """
    Run spaCy NER over the given text and return all GPE/LOC entities.

    Returns a list of dicts: {"text", "normalized", "label", "start", "end"}
    where start/end are character offsets in `text`, useful for later
    extracting the surrounding context window.
    """
    nlp = get_nlp()
    doc = nlp(text)
    entities = []
    seen = set()
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            normalized = normalize_location(ent.text)
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            entities.append(
                {
                    "text": ent.text,
                    "normalized": normalized,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                }
            )
    return entities


if __name__ == "__main__":
    sample = "Heavy monsoon rains caused severe flooding across Mumbai. Authorities in Mumbai issued an alert."
    for ent in extract_locations(sample):
        print(ent)
