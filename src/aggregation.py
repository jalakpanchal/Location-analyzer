"""
aggregation.py
---------------
Aggregate per-article location/context results across the whole
dataset: most frequent locations, event type breakdown, sentiment
breakdown.

Rubric mapping: Stage 3 - Data Analysis & Interpretation, Report & Presentation
"""

import pandas as pd
from context_analysis import analyze_article


def analyze_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the full pipeline over every article in the dataframe
    (expects columns: article_id, full_text) and return a flat
    results dataframe with one row per (article, location) pair.
    """
    all_results = []
    for _, row in df.iterrows():
        text = row.get("full_text", "") or row.get("headline", "")
        results = analyze_article(row["article_id"], text)
        for r in results:
            r["headline"] = row.get("headline", "")
            r["date"] = row.get("date", "")
            r["source"] = row.get("source", "")
            all_results.append(r)
    return pd.DataFrame(all_results)


def location_frequency(results_df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Top N most frequently mentioned locations."""
    if results_df.empty:
        return pd.DataFrame(columns=["location", "count"])
    freq = (
        results_df.groupby("location")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(top_n)
    )
    return freq


def category_breakdown(results_df: pd.DataFrame) -> pd.DataFrame:
    """Count of location-event pairs per event category."""
    if results_df.empty:
        return pd.DataFrame(columns=["event_category", "count"])
    return (
        results_df.groupby("event_category")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )


def sentiment_breakdown(results_df: pd.DataFrame) -> pd.DataFrame:
    """Count of location-event pairs per sentiment label."""
    if results_df.empty:
        return pd.DataFrame(columns=["sentiment_label", "count"])
    return (
        results_df.groupby("sentiment_label")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )


if __name__ == "__main__":
    df = pd.read_csv("../data/news_sample.csv")
    results = analyze_dataset(df)
    print(results.head())
    print(location_frequency(results))
    print(category_breakdown(results))
