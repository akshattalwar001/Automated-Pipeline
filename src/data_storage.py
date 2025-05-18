import sqlite3
import yaml
import pandas as pd
from datetime import datetime


def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)


def init_db():
    config = load_config()
    db_path = config["database"]["path"]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            published_at TEXT,
            category_id TEXT,
            tags TEXT,
            views INTEGER,
            likes INTEGER,
            channel_title TEXT,
            region_code TEXT,
            fetch_date TEXT
        )
    """)
    conn.commit()
    conn.close()


def store_data(df):
    config = load_config()
    db_path = config["database"]["path"]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add fetch_date column
    df["fetch_date"] = datetime.now().strftime("%Y-%m-%d")

    # Convert tags list to string
    df["tags"] = df["tags"].apply(lambda x: ",".join(x))

    # Create a temporary table
    temp_table = "temp_videos"
    df.to_sql(temp_table, conn, if_exists="replace", index=False)

    # Merge new data into videos table: update existing, insert new
    cursor.execute("""
        INSERT OR REPLACE INTO videos (
            video_id, title, published_at, category_id, tags,
            views, likes, channel_title, region_code, fetch_date
        )
        SELECT
            video_id, title, published_at, category_id, tags,
            views, likes, channel_title, region_code, fetch_date
        FROM temp_videos
    """)

    # Drop temporary table
    cursor.execute(f"DROP TABLE {temp_table}")

    conn.commit()
    conn.close()