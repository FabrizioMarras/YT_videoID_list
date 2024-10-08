import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch API key and Channel ID from environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY')
CHANNEL_ID = os.getenv('CHANNEL_ID')

BASE_URL = 'https://www.googleapis.com/youtube/v3'

def get_videos_from_channel(api_key, channel_id):
    video_list = []
    url = f'{BASE_URL}/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&type=video&maxResults=50'
    
    while True:
        response = requests.get(url)
        data = response.json()
        
        if 'items' not in data:
            print("Error fetching data.")
            break
        
        # Iterate through the videos in the response and store video ID and title
        for item in data['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            video_list.append({'Video ID': video_id, 'Title': title})
        
        # Check if there is a next page and get the nextPageToken for the next request
        if 'nextPageToken' in data:
            next_page_token = data['nextPageToken']
            url = f'{BASE_URL}/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&type=video&maxResults=50&pageToken={next_page_token}'
        else:
            # No more pages
            break
    
    return video_list

# Fetch all videos
videos = get_videos_from_channel(API_KEY, CHANNEL_ID)

# Create a pandas DataFrame from the list of videos
df = pd.DataFrame(videos)

# Save the DataFrame to an Excel file
output_file = 'youtube_videos.xlsx'
df.to_excel(output_file, index=False)

print(f"Video list saved to {output_file}")
