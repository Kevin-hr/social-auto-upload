
import asyncio
import sys
from pathlib import Path

# Add project root to path so we can import 'conf' etc. if run from project root
# Or simply assume we are pointing to the file.
# For standalone robustness, we'll try to dynamically add the project root.

current_file = Path(__file__).resolve()
# Assuming this script is run from project root, or we can just try to import.

try:
    from playwright.async_api import async_playwright
    # Function to import conf from current working directory
    sys.path.append(str(Path.cwd()))
    from conf import LOCAL_CHROME_PATH
    from utils.base_social_media import set_init_script
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run this script from the root of the 'social-auto-upload' project.")
    sys.exit(1)

async def get_douyin_cookie_auto(account_file):
    async with async_playwright() as playwright:
        options = {
            'args': [
                '--lang=zh-CN',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ],
            'headless': False, # Must be false to see QR code
            'executable_path': LOCAL_CHROME_PATH
        }
        
        print(f"Launching browser from: {LOCAL_CHROME_PATH}")
        browser = await playwright.chromium.launch(**options)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        await set_init_script(context)
        
        page = await context.new_page()
        
        print("Navigating to Douyin Creator Center...")
        await page.goto("https://creator.douyin.com/")
        
        print("\n" + "="*50)
        print("请在浏览器中扫码登录抖音")
        print("Please scan the QR code to login")
        print("="*50 + "\n")

        # Loop until logged in
        max_retries = 300 # 5 minutes max
        logged_in = False
        
        for i in range(max_retries):
            # Check for indicators of being logged in
            url = page.url
            if "creator-micro" in url:
                print(f"Detected login via URL: {url}")
                logged_in = True
                break
                
            try:
                # "上传视频" button or "首页" link usually indicates login
                if await page.get_by_text("上传视频").count() > 0 or await page.get_by_text("首页").count() > 0:
                     print("Detected login via Page Elements")
                     logged_in = True
                     break
            except:
                pass
            
            await asyncio.sleep(1)
            if i % 10 == 0:
                print(f"Waiting for login... ({i}/{max_retries})")
        
        if logged_in:
            print("Login successful! Saving cookies...")
            # Wait a bit for cookies to fully set
            await asyncio.sleep(3)
            await context.storage_state(path=account_file)
            print(f"Cookies saved to: {account_file}")
        else:
            print("Timeout waiting for login.")
            
        await browser.close()

if __name__ == '__main__':
    # Determine cookie path: project_root/cookiesFile/douyin_uploader/account.json
    cwd = Path.cwd()
    account_file = cwd / "cookiesFile" / "douyin_uploader" / "account.json"
    
    # Ensure directory exists
    account_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Target Cookie File: {account_file}")
    
    asyncio.run(get_douyin_cookie_auto(account_file))
