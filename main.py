from src.data_extraction import extract_trending_videos
from src.data_cleaning import clean_data
from src.data_storage import init_db, store_data


def main():
    # Initialize database
    init_db()

    # List of regions to fetch
    regions = ["US", "GB", "CA"]  # Add more as needed

    for region in regions:
        # Extract data
        videos = extract_trending_videos(region_code=region)

        # Clean data
        df = clean_data(videos)

        # Store data
        store_data(df)


if __name__ == "__main__":
    main()