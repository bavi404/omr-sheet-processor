"""
Download model weights from remote storage (Google Drive, S3, etc.)
This script runs before the app starts on cloud platforms like Render
"""

import os
import sys
import requests
from tqdm import tqdm

def download_file(url, destination):
    """Download file with progress bar."""
    print(f"Downloading model from: {url}")
    print(f"Destination: {destination}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        
        with open(destination, 'wb') as f:
            if total_size > 0:
                # Show progress bar
                with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading') as pbar:
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                # No content-length header, download without progress
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
        
        file_size = os.path.getsize(destination) / (1024 * 1024)  # MB
        print(f"✅ Download complete! Size: {file_size:.2f} MB")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        if os.path.exists(destination):
            os.remove(destination)
        return False

def main():
    """Main download function."""
    # Get configuration from environment variables
    MODEL_URL = os.getenv('MODEL_URL', '')
    MODEL_PATH = os.getenv('MODEL_PATH', 'best.pt')
    
    print("="*60)
    print("MODEL DOWNLOAD SCRIPT")
    print("="*60)
    
    # Check if model already exists
    if os.path.exists(MODEL_PATH):
        file_size = os.path.getsize(MODEL_PATH) / (1024 * 1024)  # MB
        print(f"✅ Model already exists: {MODEL_PATH} ({file_size:.2f} MB)")
        print("Skipping download.")
        return 0
    
    # Check if MODEL_URL is set
    if not MODEL_URL:
        print("⚠️  WARNING: MODEL_URL environment variable not set!")
        print("Model will not be downloaded.")
        print("\nTo fix this:")
        print("1. Upload best.pt to Google Drive")
        print("2. Get the direct download link:")
        print("   https://drive.google.com/uc?export=download&id=YOUR_FILE_ID")
        print("3. Set MODEL_URL environment variable in Render")
        return 1
    
    # Download model
    print(f"\nDownloading model to: {MODEL_PATH}")
    success = download_file(MODEL_URL, MODEL_PATH)
    
    if success:
        print("\n✅ Model download successful!")
        return 0
    else:
        print("\n❌ Model download failed!")
        print("API will start but model-dependent endpoints will not work.")
        return 1

if __name__ == '__main__':
    exit_code = main()
    print("="*60)
    sys.exit(exit_code)

