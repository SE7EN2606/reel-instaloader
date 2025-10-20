import instaloader
import os
from google.cloud import storage
from pathlib import Path

# Initialize Instaloader
L = instaloader.Instaloader()

# Function to download a single Instagram reel by URL
def download_reel(reel_url, download_path="downloaded_reels"):
    short_code = reel_url.split("/")[-2]  # Extract the short code from the URL
    try:
        # Download the reel (this will download the video and metadata)
        L.download_post(instaloader.Post.from_shortcode(L.context, short_code), target=download_path)
        return os.path.join(download_path, f"{short_code}.mp4")  # Return the downloaded video path
    except Exception as e:
        print(f"Error downloading reel: {str(e)}")
        return None

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Function to upload file to Google Cloud Storage bucket
def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

# Example usage
if __name__ == "__main__":
    # Replace with the Instagram reel URL you want to download
    reel_url = "https://www.instagram.com/reel/DPrwenMjKtw/"  # Use your own Reel URL
    download_path = "downloaded_reels"
    
    # Download the Reel video
    video_path = download_reel(reel_url, download_path)
    
    if video_path:
        print(f"Reel downloaded at: {video_path}")
        
        # Google Cloud Storage bucket name
        bucket_name = "recolekt-uploader"  # Replace with your actual bucket name
        
        # Upload video to Google Cloud Storage
        upload_to_gcs(bucket_name, video_path, Path(video_path).name)
    else:
        print("Failed to download the reel.")
