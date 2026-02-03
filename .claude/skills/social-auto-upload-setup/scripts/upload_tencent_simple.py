
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path.cwd()))

try:
    from conf import BASE_DIR
    # Note: tencent_uploader.main uses 'weixin_setup' and 'TencentVideo'
    from uploader.tencent_uploader.main import weixin_setup, TencentVideo
    from utils.files_times import get_title_and_hashtags
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please run this script from the project root directory!")
    sys.exit(1)

def ensure_metadata(file_path: Path):
    txt_path = file_path.with_suffix('.txt')
    if not txt_path.exists():
        print(f"[!] Metadata file missing for {file_path.name}")
        print(f"[+] Creating default metadata: {txt_path.name}")
        title = file_path.stem
        hashtags = "#日常 #分享"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"{title}\n{hashtags}")
    return txt_path

async def main():
    # Setup Paths
    video_dir = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR) / "cookiesFile" / "tencent_uploader" / "account.json"
    
    # 1. Find a video
    files = list(video_dir.glob("*.mp4"))
    
    if not files:
        print(f"[-] No .mp4 videos found in {video_dir}")
        return

    target_video = files[0]
    print(f"[*] Target Video: {target_video.name}")
    
    # 1.5 Auto-generate metadata
    ensure_metadata(target_video)

    # 2. Check content
    if not account_file.exists():
        print(f"[-] Cookie file not found at {account_file}")
        print("Please run 'get_tencent_cookie_auto.py' first.")
        return

    # 3. Setup (Tencent specific)
    print(f"[*] Verifying cookies from {account_file}...")
    # Handle=False means don't auto-open browser if cookie fails, just return False
    valid = await weixin_setup(account_file, handle=False)
    if not valid:
        print("[-] Cookies invalid! Please re-login.")
        return
        
    # 4. Upload
    title, tags = get_title_and_hashtags(str(target_video))
    print(f"[+] Starting Upload...\nTitle: {title}\nTags: {tags}")
    
    # publish_date = 0 -> immediate (API expects a datetime object or 0, but TencentVideo init hint says datetime)
    # Looking at main.py: if self.publish_date != 0: await self.set_schedule_time_tencent(...)
    # So 0 is valid for immediate upload.
    
    # TencentVideo(self, title, file_path, tags, publish_date: datetime, account_file, category=None, is_draft=False)
    app = TencentVideo(title, target_video, tags, 0, account_file)
    
    await app.main()
    print("[+] Upload task finished.")

if __name__ == '__main__':
    asyncio.run(main())
