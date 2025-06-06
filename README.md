
# 📊 YouTube Trends Dashboard

A Python-based pipeline that fetches trending YouTube videos, stores them in a local SQLite database, and visualizes key insights using a Streamlit dashboard.

---

## 🧠 Overview

This project automates the following:

1. **Fetch** trending videos from YouTube (regions: US, GB, CA)
2. **Clean** and preprocess data (e.g., fix dates, split tags)
3. **Store** data in an SQLite database (`youtube_trends.db`)
4. **Visualize** trends in an interactive Streamlit dashboard

---

## 🗂️ Project Structure

```
.
├── config/
│   └── config.yaml                # Stores YouTube API key & DB path
├── data/
│   └── youtube_trends.db         # SQLite database file
├── src/
│   ├── data_extraction.py        # Fetches trending videos via API
│   ├── data_cleaning.py          # Cleans and transforms raw data
│   ├── data_storage.py           # Stores data in SQLite
│   └── dashboard.py              # Streamlit dashboard app
├── main.py                       # Orchestrates the full pipeline
└── requirements.txt              # Required packages
```

---

## 🔁 Pipeline Workflow

1. `main.py` triggers the pipeline
2. `data_extraction.py` fetches raw video data
3. `data_cleaning.py` processes and cleans it
4. `data_storage.py` stores it in SQLite
5. `dashboard.py` visualizes the trends via Streamlit

---

## 📊 Dashboard Features

- **Top 10 Videos**: Title, channel, views, likes
- **Top Categories**: Bar chart of top 5
- **Top Channels**: By number of trending videos
- **Top Tags**: Ranked tag frequency
- **Top Keywords**: Keyword count and relevance
- **Filters**: Region, category, date

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/youtube-trends-dashboard.git
cd youtube-trends-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Your YouTube API Key

Create `config/config.yaml`:

```yaml
api_key: "YOUR_YOUTUBE_API_KEY"
db_path: "data/youtube_trends.db"
```

### 4. Run the Pipeline

```bash
python main.py
```

### 5. Launch the Dashboard

```bash
streamlit run src/dashboard.py
```

---


## 🧑‍💻 Author

🔗 [LinkedIn](https://linkedin.com/in/Akshat-talwar)
