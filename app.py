import instaloader
import os

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

# Example usage:
reel_url = "https://www.instagram.com/reel/DPrwenMjKtw/"  # Replace with your reel URL
download_path = download_reel(reel_url)

if download_path:
    print(f"Reel downloaded at: {download_path}")
