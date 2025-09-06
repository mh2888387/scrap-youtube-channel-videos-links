#!/usr/bin/env python3
"""
YouTube Video Extractor from HTML
Extracts video links and titles from YouTube channel HTML files

Usage:
1. Copy the YouTube channel HTML from browser dev tools
2. Save it as 'youtube_channel.html'
3. Run this script
"""

import re
import json
import csv
from bs4 import BeautifulSoup
def extract_youtube_videos_from_html(html_content):
    """Extract video links and titles from YouTube channel HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    videos = []
    print("Attempting to extract videos using multiple methods...")

    # Method 1: ytInitialData extraction (most reliable)
    print("Method 1: Searching for ytInitialData...")
    script_tags = soup.find_all('script')
    for i, script in enumerate(script_tags):
        if script.string and 'ytInitialData' in script.string:
            try:
                script_content = script.string
                patterns = [
                    r'var ytInitialData = ({.*?});',
                    r'window\["ytInitialData"\] = ({.*?});',
                    r'ytInitialData = ({.*?});'
                ]
                for pattern in patterns:
                    match = re.search(pattern, script_content, re.DOTALL)
                    if match:
                        json_str = match.group(1)
                        data = json.loads(json_str)
                        videos.extend(extract_videos_from_data_structure(data))
                        if videos:
                            break
                if videos:
                    break
            except (json.JSONDecodeError, KeyError, TypeError):
                continue

    # Method 2: Direct HTML parsing
    if not videos:
        print("Method 2: Attempting direct HTML parsing...")
        videos = extract_videos_from_html_elements(soup)

    # Method 3: Look for video IDs in the entire HTML
    if not videos:
        print("Method 3: Searching for video IDs in HTML content...")
        videos = extract_video_ids_from_text(html_content)

    # Remove duplicates
    seen_ids = set()
    unique_videos = []
    for video in videos:
        if video['video_id'] not in seen_ids:
            seen_ids.add(video['video_id'])
            unique_videos.append(video)

    return unique_videos

def extract_videos_from_data_structure(data_structure):
    videos = []
    def recursive_search(obj):
        if isinstance(obj, dict):
            if 'videoRenderer' in obj:
                video = obj['videoRenderer']
                video_id = video.get('videoId', '')
                # Extract title
                title = ''
                if 'title' in video:
                    if isinstance(video['title'], dict):
                        if 'runs' in video['title']:
                            title = video['title']['runs'][0].get('text', '')
                        elif 'simpleText' in video['title']:
                            title = video['title']['simpleText']
                    elif isinstance(video['title'], str):
                        title = video['title']
                if video_id and title:
                    videos.append({
                        'title': title,
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'video_id': video_id
                    })
            for value in obj.values():
                recursive_search(value)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item)
    recursive_search(data_structure)
    return videos

def extract_videos_from_html_elements(soup):
    videos = []
    selectors = [
        'a[href*="/watch?v="]',
        'a[href*="youtu.be/"]',
        '[data-video-id]',
        '.ytd-video-renderer',
        '.ytd-grid-video-renderer'
    ]
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            video_id = ''
            title = ''
            href = element.get('href', '')
            data_video_id = element.get('data-video-id', '')
            if data_video_id:
                video_id = data_video_id
            elif href:
                match = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', href)
                if match:
                    video_id = match.group(1)
            title = (element.get('title', '') or 
                     element.get('aria-label', ''))


            if video_id and title:
                videos.append({
                    'title': title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'video_id': video_id
                })
    return videos

def extract_video_ids_from_text(html_content):
    videos = []
    video_id_pattern = r'(?:watch\?v=|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})'
    matches = re.finditer(video_id_pattern, html_content)
    seen_ids = set()
    for match in matches:
        video_id = match.group(1)
        if video_id not in seen_ids:
            seen_ids.add(video_id)
            videos.append({
                'title': f'Video ID: {video_id}',
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'video_id': video_id
            })
    return videos[:50]

def process_youtube_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        videos = extract_youtube_videos_from_html(html_content)
        if videos:
            print(f"Successfully extracted {len(videos)} videos!")
            return videos
        else:
            print("No videos found. The HTML structure might be different.")
            return []
    except FileNotFoundError:
        print(f"File {file_path} not found!")
        return []
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

def save_videos_to_csv(videos, output_file='youtube_videos.csv'):
    if not videos:
        print("No videos to save.")
        return
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['title', 'url', 'video_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for video in videos:
            writer.writerow(video)
    print(f"Videos saved to {output_file}")

def save_videos_to_json(videos, output_file='youtube_videos.json'):
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(videos, jsonfile, indent=2, ensure_ascii=False)
    print(f"Videos saved to {output_file}")

def main():
    html_file = 'youtube_channel.html'  # change as needed
    print("YouTube Video Extractor\n" + "="*50)
    videos = process_youtube_html_file(html_file)
    if videos:
        print(f"\nFound {len(videos)} unique videos:\n" + "-"*50)
        for i, video in enumerate(videos[:5]):
            print(f"{i+1}. {video['title']}\n   URL: {video['url']}\n")
        if len(videos) > 5:
            print(f"... and {len(videos)-5} more videos")
        save_videos_to_csv(videos)
        save_videos_to_json(videos)
        print(f"\nExtraction complete! Check youtube_videos.csv and youtube_videos.json")
    else:
        print("No videos were extracted. Please check your HTML file.")

if __name__ == "__main__":
    main()
