"""
evaluate.py
-----------
Evaluate the NER + event-category classification pipeline against a
manually labeled test set (data/test_labels.csv) using precision,
recall, and F1 (macro-averaged across categories).

Rubric mapping: Stage 2 - Testing & Validation, Stage 3 - Data Analysis
"""

import pandas as pd
from sklearn.metrics import classification_report, precision_recall_fscore_support
from context_analysis import analyze_article


def evaluate(news_df: pd.DataFrame, labels_df: pd.DataFrame) -> dict:
    """
    For each (article_id, location) pair in labels_df, run the pipeline
    on the matching article and compare the predicted event_category to
    the expected_category. Returns a metrics dict plus a detail dataframe.
    """
    news_lookup = news_df.set_index("article_id")["full_text"].to_dict()

    y_true, y_pred, details = [], [], []
    for _, row in labels_df.iterrows():
        article_id = row["article_id"]
        expected_location = row["location"]
        expected_category = row["expected_category"]
        text = news_lookup.get(article_id, "")
        if not text:
            continue

        results = analyze_article(article_id, text)
        # find the prediction matching this location (case-insensitive)
        match = next(
            (r for r in results if r["location"].lower() == expected_location.lower()),
            None,
        )
        predicted_category = match["event_category"] if match else "not_detected"

        y_true.append(expected_category)
        y_pred.append(predicted_category)
        details.append(
            {
                "article_id": article_id,
                "location": expected_location,
                "expected_category": expected_category,
                "predicted_category": predicted_category,
                "correct": expected_category == predicted_category,
            }
        )

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )
    accuracy = sum(d["correct"] for d in details) / len(details) if details else 0

    metrics = {
        "precision_macro": round(precision, 3),
        "recall_macro": round(recall, 3),
        "f1_macro": round(f1, 3),
        "accuracy": round(accuracy, 3),
        "n_examples": len(details),
    }
    return {"metrics": metrics, "details": pd.DataFrame(details)}


if __name__ == "__main__":
    news_df = pd.read_csv("../data/news_sample.csv")
    labels_df = pd.read_csv("../data/test_labels.csv")
    result = evaluate(news_df, labels_df)
    print(result["metrics"])
    print(result["details"])
