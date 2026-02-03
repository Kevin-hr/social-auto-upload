
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path.cwd()))

try:
    from playwright.async_api import async_playwright
    from conf import LOCAL_CHROME_PATH
    from utils.base_social_media import set_init_script
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please run this script from the project root directory!")
    sys.exit(1)

async def get_ks_cookie_auto(account_file):
    async with async_playwright() as playwright:
        options = {
            'args': [
                '--lang=zh-CN',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
            ],
            'headless': False, 
            'executable_path': LOCAL_CHROME_PATH
        }
        
        print(f"Launching browser from: {LOCAL_CHROME_PATH}")
        browser = await playwright.chromium.launch(**options)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        await set_init_script(context)
        
        page = await context.new_page()
        
        print("Navigating to Kuaishou Creator Center...")
        # Kuaishou Creator Center URL
        await page.goto("https://cp.kuaishou.com/")
        
        print("\n" + "="*50)
        print("请在浏览器中扫码登录快手")
        print("Please scan the QR code to login to Kuaishou")
        print("="*50 + "\n")

        # Loop until logged in
        max_retries = 300 # 5 minutes max
        logged_in = False
        
        for i in range(max_retries):
            # Check for login indicators
            try:
                # After login, URL usually contains 'article/publish' or 'home'
                # Or specific elements appear like user avatar or "发布视频" button
                if "cp.kuaishou.com/article" in page.url or "cp.kuaishou.com/home" in page.url:
                    print(f"Detected login via URL: {page.url}")
                    logged_in = True
                    break
                
                # Check for "发布作品" or similar button
                if await page.get_by_text("发布作品").count() > 0 or await page.get_by_text("退出登录").count() > 0:
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
            await asyncio.sleep(3) # Wait for cookies to settle
            await context.storage_state(path=account_file)
            print(f"Cookies saved to: {account_file}")
        else:
            print("Timeout waiting for login.")
            
        await browser.close()

if __name__ == '__main__':
    # Determine cookie path: project_root/cookiesFile/ks_uploader/account.json
    cwd = Path.cwd()
    account_file = cwd / "cookiesFile" / "ks_uploader" / "account.json"
    
    # Ensure directory exists
    account_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Target Cookie File: {account_file}")
    
    asyncio.run(get_ks_cookie_auto(account_file))
