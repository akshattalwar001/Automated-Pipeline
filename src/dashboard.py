import streamlit as st
import sqlite3
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import os
from collections import Counter
from googleapiclient.discovery import build

st.set_page_config(page_title="YouTube Trends Dashboard", layout="wide")
st.title("YouTube Trends Dashboard")

# Load config and data
src_dir = os.path.dirname(__file__)
with open(os.path.join(src_dir, "..", "config", "config.yaml"), "r") as file:
    config = yaml.safe_load(file)

conn = sqlite3.connect(os.path.join(src_dir, "..", config["database"]["path"]))
df = pd.read_sql_query("SELECT * FROM videos", conn)
conn.close()

df["tags"] = df["tags"].apply(lambda x: x.split(",") if x and isinstance(x, str) else [])
df["published_at"] = pd.to_datetime(df["published_at"], errors="coerce")
df["fetch_date"] = pd.to_datetime(df["fetch_date"], errors="coerce")

# Fetch category names using YouTube API
youtube = build("youtube", "v3", developerKey=config["youtube"]["api_key"])
regions = df["region_code"].dropna().unique()
category_map = {}
for region in regions:
    categories = youtube.videoCategories().list(part="snippet", regionCode=region).execute()
    for category in categories["items"]:
        category_map[category["id"]] = category["snippet"]["title"]

# Filters
st.sidebar.header("Filters")
regions = ["All"] + sorted(df["region_code"].dropna().unique())
selected_region = st.sidebar.selectbox("Region", regions)
categories = ["All"] + sorted(df["category_id"].dropna().unique())
selected_category = st.sidebar.selectbox("Category", categories)
dates = ["All"] + sorted(df["fetch_date"].dropna().dt.strftime("%Y-%m-%d").unique())
selected_date = st.sidebar.selectbox("Date", dates)

# Apply filters
filtered_df = df
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region_code"] == selected_region]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category_id"] == selected_category]
if selected_date != "All":
    filtered_df = filtered_df[filtered_df["fetch_date"].dt.strftime("%Y-%m-%d") == selected_date]

# Analyze data
top_videos = filtered_df.nlargest(10, "views")[["video_id", "title", "channel_title", "views", "likes"]]
top_categories = filtered_df["category_id"].value_counts().nlargest(5)
top_categories.index = top_categories.index.map(lambda x: category_map.get(str(x), str(x)))
top_channels = filtered_df["channel_title"].value_counts().nlargest(5)
all_tags = [tag for tags in filtered_df["tags"] for tag in tags if tag]
tag_counts = Counter(all_tags)
all_titles = " ".join(filtered_df["title"].astype(str).str.lower())
words = [word for word in all_titles.split() if len(word) > 3 and word.isalnum()]
keyword_counts = Counter(words)

# Layout
col1, col2 = st.columns(2)

# Top 10 Videos
with col1:
    st.subheader("Top 10 Trending Videos")
    videos_df = pd.DataFrame(top_videos)
    videos_df["views"] = videos_df["views"].apply(lambda x: f"{x:,}")
    videos_df["likes"] = videos_df["likes"].apply(lambda x: f"{x:,}")
    st.table(videos_df[["title", "channel_title", "views", "likes"]])

# Top Categories
with col2:
    st.subheader("Top Categories")
    fig, ax = plt.subplots()
    pd.Series(top_categories).plot(kind="bar", ax=ax)
    ax.set_xlabel("Category")
    ax.set_ylabel("Number of Videos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

# Top Channels
with col1:
    st.subheader("Top Channels")
    fig, ax = plt.subplots()
    pd.Series(top_channels).plot(kind="bar", ax=ax)
    ax.set_xlabel("Channel")
    ax.set_ylabel("Number of Videos")
    st.pyplot(fig)

# Top Tags (Ranked List)
with col2:
    st.subheader("Top Tags")
    if tag_counts:
        top_tags = tag_counts.most_common(10)
        for rank, (tag, count) in enumerate(top_tags, 1):
            st.write(f"{rank}. {tag} ({count})")
    else:
        st.write("No tags available.")

# Top Title Keywords (Ranked List)
with col1:
    st.subheader("Top Title Keywords")
    if keyword_counts:
        top_keywords = keyword_counts.most_common(10)
        for rank, (keyword, count) in enumerate(top_keywords, 1):
            st.write(f"{rank}. {keyword} ({count})")
    else:
        st.write("No keywords available.")