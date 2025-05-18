import pandas as pd


def clean_data(videos):
    df = pd.DataFrame(videos)

    # Convert data types
    df["views"] = pd.to_numeric(df["views"], errors="coerce").fillna(0).astype(int)
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0).astype(int)
    df["published_at"] = pd.to_datetime(df["published_at"])

    # Handle missing tags
    df["tags"] = df["tags"].apply(lambda x: x if isinstance(x, list) else [])

    # Remove duplicates
    df = df.drop_duplicates(subset=["video_id"])

    # Replace NaN titles and channels with "Unknown"
    df["title"] = df["title"].fillna("Unknown")
    df["channel_title"] = df["channel_title"].fillna("Unknown")

    # Ensure region_code is valid
    df["region_code"] = df["region_code"].fillna("Unknown")

    return df