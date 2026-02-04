
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path.cwd()))

try:
    from conf import BASE_DIR
    from conf import BASE_DIR
    from uploader.douyin_uploader.main import douyin_setup, DouYinVideo
    from utils.files_times import get_title_and_hashtags
    # New: State Manager & Smart Metadata
    from utils.state_manager import UploadStateManager
    from utils.smart_metadata import ensure_smart_metadata
    # New: Self-Evolution Telemetry
    from utils.usage_tracker import auto_track
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please run this script from the project root directory!")
    sys.exit(1)

# Local ensure_metadata removed in favor of utils.smart_metadata

@auto_track("social-upload-douyin")
async def main():
    # Setup Paths
    # video_dir = Path(BASE_DIR) / "videos"  # Project's videos folder
    video_dir = Path(r"C:\Users\52648\Videos\社媒发布")  # Absolute path as requested
    account_file = Path(BASE_DIR) / "cookiesFile" / "douyin_uploader" / "account.json"
    
    # Initialize State Manager
    state_manager = UploadStateManager()
    PLATFORM = "douyin"
    
    # 1. Find all videos
    all_videos = list(video_dir.glob("*.mp4"))
    
    if not all_videos:
        print(f"[-] No .mp4 videos found in {video_dir}")
        return

    # 2. Filter pending videos
    pending_videos = state_manager.filter_pending_videos(all_videos, PLATFORM)
    
    print(f"[*] Total Videos: {len(all_videos)}")
    print(f"[*] Pending Upload: {len(pending_videos)}")
    
    if not pending_videos:
        print("[+] All videos have been uploaded. Good job!")
        return

    # 3. Check Account
    if not account_file.exists():
        print(f"[-] Cookie file not found at {account_file}")
        print("Please run 'get_douyin_cookie_auto.py' first.")
        return

    print(f"[*] Verifying cookies from {account_file}...")
    valid = await douyin_setup(account_file, handle=False)
    if not valid:
        print("[-] Cookies invalid! Please re-login.")
        return

    # 4. Batch Process
    for target_video in pending_videos:
        print(f"\n--- Processing: {target_video.name} ---")
        
        # Mark start
        state_manager.mark_start(str(target_video), PLATFORM)
        
        try:
            # Auto-generate metadata (Smart AI or Fallback)
            ensure_smart_metadata(target_video, platform=PLATFORM)
            
            # Prepare
            title, tags = get_title_and_hashtags(str(target_video))
            print(f"[+] Title: {title}\n[+] Tags: {tags}")
            
            # Upload
            app = DouYinVideo(title, target_video, tags, 0, account_file)
            await app.main()
            
            # Mark Success
            state_manager.mark_success(str(target_video), PLATFORM)
            print(f"[+] Successfully uploaded: {target_video.name}")
            
        except Exception as e:
            # Mark Failure
            error_msg = str(e)
            state_manager.mark_failed(str(target_video), PLATFORM, error_msg)
            print(f"[-] Failed to upload {target_video.name}: {error_msg}")
            
            # Optional: Decide if you want to stop on first error or continue
            # continue 

    print("\n[=] Batch Processing Finished.")

if __name__ == '__main__':
    asyncio.run(main())
