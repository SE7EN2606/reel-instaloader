import instaloader
from google.cloud import storage

# Initialize Instaloader
L = instaloader.Instaloader()

def download_reel(url):
    post = instaloader.Post.from_url(L.context, url)
    L.download_post(post, target='downloaded_reels')
    print(f"Downloaded: {post.url}")

def upload_to_gcs(file_path, bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    blob.upload_from_filename(file_path)
    print(f"Uploaded {file_path} to {bucket_name}")

if __name__ == '__main__':
    url = 'https://www.instagram.com/reel/your_reel_id/'
    download_reel(url)
    upload_to_gcs('downloaded_reels/your_video.mp4', 'your-bucket-name')
