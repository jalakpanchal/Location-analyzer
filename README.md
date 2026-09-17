# Location Entity Extraction & News Context Analyzer

**Student:** Jalak Panchal | **Roll No:** 23UF17721AI036

A system that identifies geographical locations mentioned in news articles and
analyzes their contextual association with events — categorizing the event type
(disaster, political, economic, sports, health) and the sentiment of the
surrounding text.

## Problem Statement

Locations mentioned in news can provide important geographical information.
This project develops a system that identifies locations and analyzes their
contextual association with events, so patterns (which places are experiencing
which kinds of events, and with what tone) can be surfaced from unstructured
news text.

## Project Structure

```
location-analyzer/
├── data/
│   ├── news_sample.csv       # 50+ sample news articles
│   └── test_labels.csv       # manually labeled test set for evaluation
├── src/
│   ├── preprocessing.py      # text cleaning + sentence segmentation
│   ├── ner_extraction.py     # spaCy GPE/LOC NER + normalization
│   ├── context_analysis.py   # context window, event category, sentiment
│   ├── aggregation.py        # dataset-wide frequency/category/sentiment stats
│   ├── geocode.py            # static lat/lon lookup for mapping
│   └── evaluate.py           # precision / recall / F1 evaluation
├── app/
│   └── main.py                # Streamlit dashboard (pastel theme)
├── requirements.txt
└── README.md
```

## Setup & Running

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app/main.py
```

The app opens in your browser with 5 tabs: Home/Overview, Live Analyzer,
Dataset Explorer, Evaluation Metrics, and About/SDG Impact.

## Methodology (mapped to rubric stages)

### Stage 1 — Problem Identification & Design Planning
- **Problem Definition & Scope:** Extract locations from news text and classify
  the event context around each mention.
- **Design & Methodology:** A modular pipeline — preprocessing → NER →
  context/semantic analysis → aggregation → evaluation — chosen for
  transparency, offline reproducibility, and ease of testing at each stage.
- **SDG Consideration:** Maps to SDG 11 and SDG 16 (see below).

### Stage 2 — Implementation & Testing
- **Implementation Quality:** Fully functional end-to-end pipeline, from raw
  CSV to live analysis in a dashboard.
- **Tools/Technology Usage:** spaCy (`en_core_web_sm`) for NER and sentence
  segmentation; VADER for sentiment; a rule-based keyword classifier for event
  category (fast, transparent, and easy to evaluate for a micro-project scope);
  a static lookup table for location-to-coordinate mapping (keeps the app
  offline-friendly and reliable during a live viva/demo).
- **Testing & Validation:** `evaluate.py` computes precision, recall, F1
  (macro-averaged), and accuracy against a manually labeled 37-example test
  set (`data/test_labels.csv`). Current results: **~92% accuracy**, F1
  (macro) ≈ 0.69 — errors are visible and explainable (e.g., an article
  about subway funding not using the word "economic" explicitly).

### Stage 3 — Analysis, Report & Presentation
- **Data Analysis & Interpretation:** Aggregation functions surface the most
  frequently mentioned locations, the event category breakdown, and the
  sentiment breakdown across the dataset.
- **Report & Presentation:** The Streamlit dashboard presents results via a
  world map (color-coded by event category), bar/pie charts, a searchable
  results table, and a live analyzer for new articles.

## SDG Impact

This project supports:
- **SDG 11 — Sustainable Cities and Communities:** by surfacing where
  disaster or infrastructure-related events are being reported, supporting
  faster situational awareness for city planners and emergency responders.
- **SDG 16 — Peace, Justice and Strong Institutions:** by helping track where
  political unrest or governance-related events are occurring, supporting
  transparency and misinformation/context tracking.

## Limitations & Future Improvements

- The event classifier is rule-based (keyword matching); a zero-shot
  transformer (e.g. `facebook/bart-large-mnli`) could improve nuance at the
  cost of speed and offline reliability.
- Geocoding uses a static lookup table, so locations outside the sample
  dataset won't appear on the map unless added or replaced with a live
  geocoder (e.g. `geopy` + Nominatim).
- VADER sentiment is lexicon-based and can miss sarcasm or complex tone.

## Screenshots

_(Insert dashboard screenshots here for your report: Home tab, Live Analyzer
result, Dataset Explorer map + charts, and Evaluation Metrics tab.)_
