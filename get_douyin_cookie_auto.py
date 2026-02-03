
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from conf import BASE_DIR, LOCAL_CHROME_PATH, LOCAL_CHROME_HEADLESS
from utils.base_social_media import set_init_script

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
            # 1. URL change to /creator-micro/home or similar
            # 2. Presence of "Upload" button or user avatar
            url = page.url
            if "creator-micro" in url:
                print(f"Detected login via URL: {url}")
                logged_in = True
                break
                
            # Check for elements that only appear when logged in
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
    account_file = Path(BASE_DIR) / "cookiesFile" / "douyin_uploader" / "account.json" # Use cookiesFile dir we created
    # Ensure directory exists
    account_file.parent.mkdir(parents=True, exist_ok=True)
    
    asyncio.run(get_douyin_cookie_auto(account_file))
