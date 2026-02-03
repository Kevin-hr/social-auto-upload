
import asyncio
from pathlib import Path
from conf import BASE_DIR
from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from utils.files_times import get_title_and_hashtags

async def main():
    # Setup Paths
    video_dir = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR) / "cookiesFile" / "douyin_uploader" / "account.json"
    
    # Target specific test video
    files = list(video_dir.glob("test_douyin_upload.mp4"))
    
    if not files:
        print("Test video not found!")
        return

    # Ensure cookies exist
    if not account_file.exists():
        print(f"Cookie file not found at {account_file}")
        return

    print(f"Found {len(files)} video(s). Starting upload using cookies from {account_file}...")

    # Setup (check cookies validity)
    valid = await douyin_setup(account_file, handle=False)
    if not valid:
        print("Cookies invalid!")
        return
        
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        print(f"Uploading: {file.name}\nTitle: {title}\nTags: {tags}")
        
        # publish_date = 0 implies immediate publish (based on douyin_uploader logic)
        app = DouYinVideo(title, file, tags, 0, account_file)
        
        await app.main()
        print("Upload task finished.")

if __name__ == '__main__':
    asyncio.run(main())
