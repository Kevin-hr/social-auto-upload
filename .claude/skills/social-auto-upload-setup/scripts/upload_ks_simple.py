
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path.cwd()))

try:
    from conf import BASE_DIR
    from uploader.ks_uploader.main import ks_setup, KSVideo
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
    account_file = Path(BASE_DIR) / "cookiesFile" / "ks_uploader" / "account.json"
    
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
        print("Please run 'get_ks_cookie_auto.py' first.")
        return

    # 3. Setup (KS specific)
    print(f"[*] Verifying cookies from {account_file}...")
    valid = await ks_setup(account_file, handle=False)
    if not valid:
        print("[-] Cookies invalid! Please re-login.")
        return
        
    # 4. Upload
    title, tags = get_title_and_hashtags(str(target_video))
    print(f"[+] Starting Upload...\nTitle: {title}\nTags: {tags}")
    
    # publish_date = 0 -> immediate
    app = KSVideo(title, target_video, tags, 0, account_file)
    
    await app.main()
    print("[+] Upload task finished.")

if __name__ == '__main__':
    asyncio.run(main())
