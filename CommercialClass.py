import os
from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QLabel
from VideoWidget import VideoWidget
import requests
from urllib.parse import urlparse
import random

BASE_URL = "https://node.alkowall.indigoingenium.ba"  # Intentional wrong URL for retry testing

class CommercialClass(QObject):
    def __init__(self):
        super().__init__()
        
        # Create the video widget instance
        self.video_widget = VideoWidget()
        
        # Connect the signal when the video finishes playing
        self.video_widget.video_finished.connect(self.on_video_finished)
        
        # Directory where videos are saved
        self.videos_directory = "videos/"
        self.device_id = 1
        
        # Initialize the retry mechanism with QTimer
        self.retry_timer = QTimer()
        self.retry_timer.timeout.connect(self.play_next_video)
        
        # Start the first video fetching process
        self.start_fetching_videos()

    def start_fetching_videos(self):
        # Start the retry timer to attempt to fetch a valid URL every 2 seconds
        self.retry_timer.start(1000)  # Retry every 2 seconds

    def play_next_video(self):
        # Get the video URL
        video_url = self.get_ad_url(self.device_id)
        
        if video_url:
            # Extract the video filename from the URL
            video_filename = self.extract_filename_from_url(video_url)
            video_path = os.path.join(self.videos_directory, video_filename)
            
            # Check if the video already exists
            if os.path.exists(video_path):
                # Play the video if it exists
                self.video_widget.play_video(video_path)
                print("Playing existing video..." + video_path)
                self.retry_timer.stop()  # Stop retrying
            else:
                # Download and then play the video
                self.download_and_play_video(video_url, video_path)
                print("Downloading and playing video..." + video_path)
                self.retry_timer.stop()  # Stop retrying
        else:
            print("Failed to retrieve video URL. Retrying...")

    def get_ad_url(self, device_id):
        # Function to get ad URL
        url = f"{BASE_URL}/advertisment/get_ad_url"
        payload = {"device_id": device_id}
        try:
            response = requests.post(url, json=payload)
            response.status_code = random.choice([200, 404])  # Simulate random status codes
            if response.status_code == 200:
                # Assuming the response JSON has an "ad_url" field
                ad_url = response.json().get("ad_url")
                if ad_url:
                    return ad_url
                else:
                    print("No ad URL found in the response.")
                    return None
            else:
                print(f"Failed to fetch ad URL. Status code: {response.status_code}")
                self.video_widget.show_placeholder()
                return None
        except requests.ConnectionError as e:
            print(f"Connection error: {e}")
            return None

    def extract_filename_from_url(self, video_url):
        # Extract the filename from the URL path
        parsed_url = urlparse(video_url)
        return os.path.basename(parsed_url.path)  # Extracts 'BudLight.mp4' from the URL

    def download_and_play_video(self, video_url, save_path):
        # Download the video from the ad URL
        try:
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                with open(save_path, 'wb') as video_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            video_file.write(chunk)
                print(f"Video downloaded successfully and saved to {save_path}")
                # Play the downloaded video
                self.video_widget.play_video(save_path)
            else:
                print(f"Failed to download video. Status code: {response.status_code}")
        except requests.ConnectionError as e:
            print(f"Connection error while downloading: {e}")
    
    def on_video_finished(self):
        print("Video finished playing. Attempting to play the next video...")
        self.start_fetching_videos()
