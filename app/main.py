"""
main.py
-------
Streamlit dashboard for the Location Entity Extraction & News Context
Analyzer micro-project.

Run with: streamlit run app/main.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pandas as pd
import plotly.express as px
import streamlit as st

from context_analysis import analyze_article
from aggregation import analyze_dataset, location_frequency, category_breakdown, sentiment_breakdown
from evaluate import evaluate
from geocode import get_coords

# ---------------------------------------------------------------------
# Page config + pastel theme CSS
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Location Entity Extraction & News Context Analyzer",
    page_icon="🗺️",
    layout="wide",
)

PASTEL_CSS = """
<style>
:root {
    --lavender: #E6E0F8;
    --blush: #FBE4EC;
    --mint: #E0F5EC;
    --powder-blue: #E1F0FA;
    --cream: #FFF9F0;
    --text-dark: #4A4458;
}

.stApp {
    background: linear-gradient(180deg, var(--cream) 0%, var(--powder-blue) 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--lavender) 0%, var(--blush) 100%);
}

h1, h2, h3 {
    color: var(--text-dark) !important;
    font-family: 'Georgia', serif;
}

.header-card {
    background: white;
    border-radius: 18px;
    padding: 24px 32px;
    box-shadow: 0 4px 18px rgba(180, 160, 220, 0.25);
    margin-bottom: 24px;
    border: 1px solid #F0E6F6;
}

.metric-card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 3px 12px rgba(180, 160, 220, 0.18);
    text-align: center;
    border: 1px solid #F0E6F6;
}

.pastel-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.85em;
    font-weight: 600;
    margin: 2px;
}
.badge-disaster { background: #FBE4E4; color: #B04A4A; }
.badge-political { background: #E6E0F8; color: #6A4E9E; }
.badge-economic { background: #E0F5EC; color: #3E8E6D; }
.badge-sports { background: #E1F0FA; color: #3B7FA6; }
.badge-health { background: #FCEFE0; color: #B5762D; }
.badge-other { background: #F0F0F0; color: #777777; }

.stButton>button {
    background: linear-gradient(135deg, #E6E0F8, #E1F0FA);
    color: var(--text-dark);
    border-radius: 12px;
    border: none;
    padding: 8px 20px;
    font-weight: 600;
}

.stDataFrame { border-radius: 14px; overflow: hidden; }
</style>
"""
st.markdown(PASTEL_CSS, unsafe_allow_html=True)

CATEGORY_COLORS = {
    "disaster": "#E9A9A9",
    "political": "#B7A6E0",
    "economic": "#8FCFB0",
    "sports": "#9BC8E8",
    "health": "#EFC08A",
    "other": "#CFCFCF",
    "not_detected": "#DDDDDD",
}


def badge(category: str) -> str:
    cls = f"badge-{category}" if category in CATEGORY_COLORS else "badge-other"
    return f'<span class="pastel-badge {cls}">{category}</span>'


# ---------------------------------------------------------------------
# Data loading (cached)
# ---------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@st.cache_data
def load_news():
    return pd.read_csv(os.path.join(DATA_DIR, "news_sample.csv"))


@st.cache_data
def load_labels():
    return pd.read_csv(os.path.join(DATA_DIR, "test_labels.csv"))


@st.cache_data
def run_pipeline(news_df):
    return analyze_dataset(news_df)


news_df = load_news()
labels_df = load_labels()
results_df = run_pipeline(news_df)

# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------
st.markdown(
    """
    <div class="header-card">
        <h1>🗺️ Location Entity Extraction & News Context Analyzer</h1>
        <p style="color:#7A7189; font-size:1.05em; margin-top:-8px;">
            Identifying geographical locations in news and analyzing their contextual association with events.
        </p>
        <p style="color:#9A90AC; font-size:0.9em;">
            <b>Jalak Panchal</b> &nbsp;|&nbsp; Roll No: 23UF17721AI036
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------
tab = st.sidebar.radio(
    "Navigate",
    ["🏠 Home / Overview", "🔍 Live Analyzer", "📊 Dataset Explorer", "✅ Evaluation Metrics", "🌍 About / SDG Impact"],
)

# ---------------------------------------------------------------------
# HOME / OVERVIEW
# ---------------------------------------------------------------------
if tab == "🏠 Home / Overview":
    st.subheader("Project Overview")
    st.write(
        "This project identifies **locations** mentioned in news articles and analyzes the "
        "**event context** surrounding each mention — its event category (disaster, political, "
        "economic, sports, health) and sentiment (positive, neutral, negative)."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h3>{len(news_df)}</h3>Articles</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h3>{results_df["location"].nunique()}</h3>Unique Locations</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><h3>{len(results_df)}</h3>Location Mentions</div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><h3>{results_df["event_category"].nunique()}</h3>Event Categories</div>', unsafe_allow_html=True)

    st.markdown("### Methodology Pipeline")
    st.write(
        "1. **Preprocessing** — text cleaning + sentence segmentation (spaCy)\n"
        "2. **NER** — extract GPE/LOC entities using spaCy `en_core_web_sm`, normalized via a lookup table\n"
        "3. **Context Analysis** — extract the surrounding sentence(s) per location, classify event category "
        "(rule-based keyword classifier), score sentiment (VADER)\n"
        "4. **Aggregation** — location frequency, category and sentiment breakdowns\n"
        "5. **Evaluation** — precision/recall/F1 against a manually labeled test set"
    )

# ---------------------------------------------------------------------
# LIVE ANALYZER
# ---------------------------------------------------------------------
elif tab == "🔍 Live Analyzer":
    st.subheader("Paste a news article to analyze")
    default_text = (
        "A powerful earthquake struck near the coast close to Lima on Thursday, "
        "damaging buildings and prompting evacuation orders. Emergency teams in Lima "
        "are assessing the extent of the destruction."
    )
    user_text = st.text_area("Article text", value=default_text, height=150)

    if st.button("Analyze Article"):
        if user_text.strip():
            with st.spinner("Running NER + context analysis..."):
                results = analyze_article("live_input", user_text)
            if not results:
                st.info("No locations (GPE/LOC entities) were detected in this text.")
            else:
                for r in results:
                    st.markdown(
                        f"""
                        <div class="metric-card" style="text-align:left; margin-bottom:12px;">
                            <b>📍 {r['location']}</b> &nbsp; {badge(r['event_category'])}
                            &nbsp; <i>sentiment: {r['sentiment_label']} ({r['sentiment_score']:+.2f})</i>
                            <p style="color:#7A7189; margin-top:8px;">{r['context']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.warning("Please paste some article text first.")

# ---------------------------------------------------------------------
# DATASET EXPLORER
# ---------------------------------------------------------------------
elif tab == "📊 Dataset Explorer":
    st.subheader("Dataset-wide Results")

    col1, col2 = st.columns(2)
    with col1:
        categories = ["All"] + sorted(results_df["event_category"].unique().tolist())
        selected_cat = st.selectbox("Filter by event category", categories)
    with col2:
        search_term = st.text_input("Search location", "")

    filtered = results_df.copy()
    if selected_cat != "All":
        filtered = filtered[filtered["event_category"] == selected_cat]
    if search_term:
        filtered = filtered[filtered["location"].str.contains(search_term, case=False, na=False)]

    st.dataframe(
        filtered[["article_id", "location", "event_category", "sentiment_label", "sentiment_score", "headline"]],
        use_container_width=True,
        height=300,
    )

    st.markdown("### 🌍 Location Map")
    map_rows = []
    for _, row in filtered.drop_duplicates("location").iterrows():
        coords = get_coords(row["location"])
        if coords:
            map_rows.append({"location": row["location"], "lat": coords[0], "lon": coords[1],
                              "event_category": row["event_category"]})
    if map_rows:
        map_df = pd.DataFrame(map_rows)
        fig = px.scatter_geo(
            map_df, lat="lat", lon="lon", color="event_category",
            hover_name="location", color_discrete_map=CATEGORY_COLORS,
            projection="natural earth",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            geo=dict(bgcolor="rgba(0,0,0,0)", landcolor="#F5F0FA", showocean=True, oceancolor="#E1F0FA"),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No mapped coordinates for the current filter.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Top Mentioned Locations")
        freq = location_frequency(results_df)
        fig2 = px.bar(freq, x="count", y="location", orientation="h",
                       color_discrete_sequence=["#B7A6E0"])
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        st.markdown("### Event Category Breakdown")
        cat_df = category_breakdown(results_df)
        fig3 = px.pie(cat_df, names="event_category", values="count",
                       color="event_category", color_discrete_map=CATEGORY_COLORS, hole=0.45)
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------
# EVALUATION METRICS
# ---------------------------------------------------------------------
elif tab == "✅ Evaluation Metrics":
    st.subheader("Model Evaluation")
    st.write("Precision, recall, and F1 computed against a manually labeled test set (`data/test_labels.csv`).")

    eval_result = evaluate(news_df, labels_df)
    m = eval_result["metrics"]

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><h3>{m["precision_macro"]}</h3>Precision (macro)</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><h3>{m["recall_macro"]}</h3>Recall (macro)</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><h3>{m["f1_macro"]}</h3>F1 (macro)</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><h3>{m["accuracy"]}</h3>Accuracy</div>', unsafe_allow_html=True)

    st.markdown("### Per-Example Predictions")
    st.dataframe(eval_result["details"], use_container_width=True, height=350)

# ---------------------------------------------------------------------
# ABOUT / SDG
# ---------------------------------------------------------------------
elif tab == "🌍 About / SDG Impact":
    st.subheader("SDG Impact & Real-World Relevance")
    st.write(
        "This project supports **SDG 11 (Sustainable Cities and Communities)** and "
        "**SDG 16 (Peace, Justice and Strong Institutions)** by helping identify where "
        "events (disasters, unrest, health crises) are occurring in real time from news text, "
        "which can support faster disaster response, situational awareness, and misinformation tracking."
    )
    st.markdown("### Limitations")
    st.write(
        "- Rule-based event classification is fast and transparent but less nuanced than a fine-tuned model.\n"
        "- Geocoding uses a static lookup table (offline-friendly), so unseen locations won't map.\n"
        "- Sentiment analysis with VADER is lexicon-based and can miss sarcasm or nuanced tone."
    )
    st.markdown("### Future Improvements")
    st.write(
        "- Swap rule-based classifier for a zero-shot transformer (e.g. `facebook/bart-large-mnli`)\n"
        "- Add live geocoding via `geopy`/Nominatim for arbitrary locations\n"
        "- Expand the dataset and add a live news API integration"
    )
