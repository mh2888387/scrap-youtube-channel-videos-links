# scrap-youtube-channel-videos-links
# YouTube Video Extractor

Extract video information (titles, URLs, video IDs) from YouTube channel HTML files and export to CSV/JSON formats.

## 🚀 Features

- **Multiple Extraction Methods**: Uses 3 fallback strategies for maximum reliability
- **Robust Parsing**: Handles various YouTube page structures and HTML formats
- **Dual Output Formats**: Exports to both CSV and JSON files
- **Deduplication**: Automatically removes duplicate videos
- **Arabic/International Support**: Full UTF-8 encoding support for all languages

## 📋 Requirements

```
beautifulsoup4
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-video-extractor.git
cd youtube-video-extractor
```

2. Install dependencies:
```bash
pip install beautifulsoup4
```

## 📖 Usage

### Step 1: Get YouTube Channel HTML
1. Open YouTube channel in your browser
2. Press `F12` to open Developer Tools
3. Go to **Elements** tab
4. Right-click on `<html>` element  **Copy**  **Copy outerHTML**
5. Save the copied HTML as `youtube_channel.html`

### Step 2: Run the Script
```bash
python youtube_extractor.py
```

### Step 3: Check Results
The script will generate:
- `youtube_videos.csv` - Spreadsheet format
- `youtube_videos.json` - Structured data format

## 🔧 How It Works

The extractor uses **3 extraction methods** in order of reliability:

### Method 1: ytInitialData Extraction (Most Reliable)
Searches for embedded JSON data (`ytInitialData`) in `<script>` tags that YouTube uses to populate the page.

### Method 2: HTML Element Parsing
Uses CSS selectors to parse rendered HTML elements:
- `'a[href*="/watch?v="]'` - Standard YouTube video links
- `'a[href*="youtu.be/"]'` - Short YouTube URLs  
- `'[data-video-id]'` - Elements with video ID attributes
- `'.ytd-video-renderer'` - YouTube video renderer components
- `'.ytd-grid-video-renderer'` - YouTube grid components

### Method 3: Pattern Matching (Fallback)
Extracts video IDs using regex patterns when other methods fail.

## 📊 Output Format

### CSV Output
```csv
title,url,video_id
"ما تيسر من سورة الكهف - طارق يوسف عرفة",https://www.youtube.com/watch?v=uPZIqazuoZc,uPZIqazuoZc
```

### JSON Output
```json
[
  {
    "title": "ما تيسر من سورة الكهف - طارق يوسف عرفة",
    "url": "https://www.youtube.com/watch?v=uPZIqazuoZc",
    "video_id": "uPZIqazuoZc"
  }
]
```

## ⚙️ Configuration

You can modify the input file by changing this line in `main()`:
```python
html_file = 'youtube_channel.html'  # Change to your HTML file name
```

## 🎯 Use Cases

- **Content Analysis**: Analyze video catalogs and content patterns
- **Research**: Study channel content themes and video metadata
- **Backup/Archival**: Create local records of channel videos
- **Data Mining**: Extract video information for further analysis

## 🐛 Troubleshooting

**No videos extracted?**
- Ensure your HTML file contains the complete page source
- Try copying HTML from browser's "View Page Source" instead of Elements tab
- Check that the HTML file is properly saved with UTF-8 encoding

**Missing some videos?**
- YouTube's dynamic loading may not include all videos in initial HTML
- The script extracts only videos present in the provided HTML

## 📝 Example Output

```
YouTube Video Extractor
==================================================
Attempting to extract videos using multiple methods...
Method 1: Searching for ytInitialData...
Successfully extracted 24 videos!

Found 24 unique videos:
--------------------------------------------------
1. ما تيسر من سورة الكهف - طارق يوسف عرفة
   URL: https://www.youtube.com/watch?v=uPZIqazuoZc

2. Another Video Title
   URL: https://www.youtube.com/watch?v=xyz123

... and 22 more videos

Videos saved to youtube_videos.csv
Videos saved to youtube_videos.json

Extraction complete! Check youtube_videos.csv and youtube_videos.json
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please respect YouTube's Terms of Service and robots.txt when using this script. The authors are not responsible for any misuse of this tool.

---

**Note**: YouTube frequently changes their HTML structure. If the script stops working, please check for updates or report an issue.
