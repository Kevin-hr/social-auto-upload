
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


async def get_xiaohongshu_cookie_auto(account_file):
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

        print("Navigating to Xiaohongshu Creator Center...")
        await page.goto("https://creator.xiaohongshu.com/")

        print("\n" + "="*50)
        print("请在浏览器中扫码登录小红书创作者中心")
        print("Please scan the QR code to login to Xiaohongshu")
        print("="*50 + "\n")

        # Use page.pause() for manual login
        print("[*] Pausing for manual login...")
        print("[*] After scanning QR code and logging in, press the Play button in DevTools to continue.")
        await page.pause()

        # After continue, save cookies
        print("[+] Saving cookies...")
        await context.storage_state(path=account_file)
        print(f"[+] Cookies saved to: {account_file}")

        await browser.close()


if __name__ == '__main__':
    # Determine cookie path: project_root/cookiesFile/xiaohongshu_uploader/account.json
    cwd = Path.cwd()
    account_file = cwd / "cookiesFile" / "xiaohongshu_uploader" / "account.json"

    # Ensure directory exists
    account_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Target Cookie File: {account_file}")

    asyncio.run(get_xiaohongshu_cookie_auto(account_file))
