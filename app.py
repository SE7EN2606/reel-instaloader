import whisper
import instaloader
import os
import json
import ffmpeg
from google.cloud import storage
from google.cloud import videointelligence
from pathlib import Path

# Initialize Whisper model (using OpenAI's official Whisper)
whisper_model = whisper.load_model("tiny")  # Switch to the smallest model if necessary

# Initialize Instaloader
L = instaloader.Instaloader()

# Initialize Google Cloud Video Intelligence client
video_intelligence_client = videointelligence.VideoIntelligenceServiceClient()

# Function to download a single Instagram reel by URL
def download_reel(reel_url, download_path="downloaded_reels"):
    short_code = reel_url.split("/")[-2]  # Extract the short code from the URL
    try:
        # Download the reel (this will download the video and metadata)
        print(f"Attempting to download reel: {short_code}")
        L.download_post(instaloader.Post.from_shortcode(L.context, short_code), target=download_path)
        reel_path = os.path.join(download_path, f"{short_code}.mp4")
        if os.path.exists(reel_path):
            return reel_path
        else:
            print(f"Downloaded file not found at expected path: {reel_path}")
            return None
    except Exception as e:
        print(f"Error downloading reel: {str(e)}")
        return None

# Function to extract frames from the video using ffmpeg (optimized for less memory usage)
def extract_frames(video_path, frames_dir="extracted_frames"):
    os.makedirs(frames_dir, exist_ok=True)
    output_pattern = os.path.join(frames_dir, "frame_%04d.jpg")
    try:
        # Extract frames from the video (every 5 seconds for lower memory usage)
        ffmpeg.input(video_path, v='error', r=0.2).output(output_pattern).run()  # Every 5 seconds
        print(f"Frames extracted to {frames_dir}")
    except Exception as e:
        print(f"Error extracting frames: {e}")

# Function to transcribe audio from the video using Whisper
def transcribe_audio(video_path):
    try:
        print("Transcribing audio...")
        result = whisper_model.transcribe(video_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# Function to analyze video content using Google Cloud Video Intelligence
def analyze_video(video_path):
    try:
        with open(video_path, "rb") as video_file:
            video_content = video_file.read()

        features = [videointelligence.Feature.LABEL_DETECTION]
        operation = video_intelligence_client.annotate_video(
            input_content=video_content,
            features=features
        )
        result = operation.result(timeout=90)
        
        # Extracting labels (objects, scenes, activities)
        labels = []
        for label in result.annotation_results[0].segment_label_annotations:
            labels.append(label.entity.description)
        
        print(f"Video labels: {labels}")
        return labels
    except Exception as e:
        print(f"Error analyzing video: {e}")
        return []

# Function to generate hashtags and categorization
def generate_hashtags(caption, vision_labels, transcript):
    try:
        # Create a prompt for a language model (e.g., OpenAI GPT) to generate hashtags and categorization
        prompt = f"""
        Given the following caption, visual labels, and transcript, categorize this Instagram Reel and suggest relevant hashtags:
        Caption: {caption}
        Vision Labels: {vision_labels}
        Transcript: {transcript}
        """

        # Call OpenAI API or similar model here to generate categorization and hashtags
        # (For simplicity, returning dummy hashtags here)
        response = {
            "category": "Entertainment",
            "hashtags": ["#funny", "#dance", "#viral", "#trend"]
        }

        print(f"Generated Category: {response['category']}")
        print(f"Generated Hashtags: {', '.join(response['hashtags'])}")
        return response
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        return {}

# Function to upload the video to Google Cloud Storage
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try:
        print(f"Uploading file {source_file_name} to Google Cloud Storage...")
        blob.upload_from_filename(source_file_name)
        print(f"File {source_file_name} uploaded to {destination_blob_name}.")
    except Exception as e:
        print(f"Error uploading to Google Cloud Storage: {e}")

# Main function
if __name__ == "__main__":
    reel_url = "https://www.instagram.com/reel/DPrwenMjKtw/"  # Use your own Reel URL
    download_path = "downloaded_reels"
    
    # Step 1: Download the Instagram Reel
    video_path = download_reel(reel_url, download_path)
    
    if video_path and os.path.exists(video_path):
        print(f"Reel downloaded at: {video_path}")

        # Step 2: Extract frames from the video
        extract_frames(video_path)

        # Step 3: Transcribe audio
        transcript = transcribe_audio(video_path)

        # Step 4: Analyze video for labels (objects/scenes)
        labels = analyze_video(video_path)

        # Step 5: Generate categorization and hashtags
        caption = "Sample caption from the post"  # This could be fetched using Instaloader as well
        result = generate_hashtags(caption, labels, transcript)
        
        # Optionally, upload video to Google Cloud Storage
        bucket_name = "recolekt-uploader"  # Replace with your actual bucket name
        upload_to_gcs(bucket_name, video_path, Path(video_path).name)
    else:
        print(f"Failed to download the reel or file not found: {video_path}")
