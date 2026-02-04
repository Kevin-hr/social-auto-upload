---
name: social-auto-upload-setup
description: >-
  Start-to-finish automation for social media video uploads (Douyin, Kuaishou, WeChat, Xiaohongshu).
  Includes environment setup, auto-login (cookie capture), and safe upload verification.
---

# Social Auto Upload Setup Expert

This skill provides a **proven, standardized workflow** for configuring and verifying the `social-auto-upload` project. It serves as a comprehensive guide and toolkit, encapsulating hours of debugging and validation into reusable scripts.

## 📦 Bundle Contents

*   `scripts/setup_environment.py`: One-click system verification (Dirs, DB, Config).
*   `scripts/get_*_cookie_auto.py`: Platform-specific login automations.
*   `scripts/upload_*_simple.py`: Safe, isolated upload verifiers with auto-recovery.


## 🧬 Self-Evolution System (Upgrade v2.1)

> **"From Tool to Life"**

This skill now includes a **Self-Evolution Engine** that tracks its own health and performance.

### 🌟 Telemetry & Diagnostics
Every time an upload script runs, it automatically logs its performance to `db/usage_log.json`.
*   **Success Tracking**: Which platform has the highest failure rate?
*   **Performance**: How long does an upload take on average?
*   **Self-Healing**: (Future) Automatically optimizing selectors based on error patterns.

### 📊 How to View Reports
The project includes a built-in diagnostic tool.

**View Basic Stats (Success Rate Table):**
```bash
python utils/usage_tracker.py --stats --days 30
```

**Export Report (JSON):**
```bash
python utils/usage_tracker.py --export
```

---

## 🚀 Proven Workflows (The "Golden Path")

### Phase 1: Environment Initialization
**Goal**: Deploy scripts + State Manager + Config.
**Action**:
```bash
python .gemini/antigravity/skills/social-auto-upload-setup/scripts/setup_environment.py
```
**Outcome**: Installs `conf.py` and `utils/state_manager.py` into your project.

### Phase 2: Authentication (Same as before)
Run `get_*_cookie_auto.py` to capture persistent sessions.

### Phase 3: Intelligent Batch Upload
**Goal**: "Set and Forget" - Upload all videos in your folder.

**Usage**:
Just run the script. It handles the rest.
```bash
python .gemini/antigravity/skills/social-auto-upload-setup/scripts/upload_douyin_simple.py
python .gemini/antigravity/skills/social-auto-upload-setup/scripts/upload_xhs_simple.py
python .gemini/antigravity/skills/social-auto-upload-setup/scripts/upload_ks_simple.py
python .gemini/antigravity/skills/social-auto-upload-setup/scripts/upload_tencent_simple.py
```

---

## 🧠 Historical Experience & Engineering Notes

### 1. State Management (Anti-Fragility)
*   **Problem**: Scripts used to be stateless. If you had 10 videos and it crashed on #5, you had to manually figure out where to resume.
*   **Solution**: We implemented `UploadStateManager`. It checks `db/upload_state.db` before every action.
*   **Benefit**: You can run the script every hour via cron/task scheduler. It will only upload *new* videos.

### 2. Selector Resilience (Xiaohongshu)
*   **Context**: CSS selectors are fragile.
*   **Solution**: The scripts now use "Fuzzy Logic" (e.g., detecting "Upload Success" text instead of relying on a specific div ID) and multiple fallback selectors for text input.

### 3. Absolute Paths
*   **Learnings**: Relative paths (`./videos`) cause confusion when running scripts from other directories.
*   **Standard**: We standardized on absolute paths (e.g., user's Video library) to ensure the source of truth is consistent across all tools.

### 4. Douyin Direct Upload Workflow (2026-02-04)
*   **Context**: Successfully uploaded video directly via Python without using simple wrapper scripts.
*   **Key Steps**:
    1. **Video Naming Convention**: Videos in `videos/` folder follow pattern `<filename>.mp4`
    2. **Metadata File**: Paired `<filename>.txt` contains title (line 1) and hashtags (line 2)
    3. **Cookie Location**: `cookiesFile/douyin_uploader/account.json`
    4. **Quick Upload Command**:
    ```bash
    # Method 1: Using skill script (recommended)
    cd .claude/skills/social-auto-upload-setup/scripts
    python upload_douyin_simple.py

    # Method 2: Direct Python execution
    python -c "
    import asyncio
    from pathlib import Path
    from uploader.douyin_uploader.main import douyin_setup, DouYinVideo

    BASE_DIR = Path('C:/Users/52648/Documents/GitHub/social-auto-upload')
    video_file = BASE_DIR / 'videos' / '456d0d86-8e79-42c7-ba67-f68711438fba.mp4'
    account_file = BASE_DIR / 'cookiesFile' / 'douyin_uploader' / 'account.json'

    title = '456d0d86-8e79-42c7-ba67-f68711438fba'
    tags = ['日常', '分享']

    cookie_ok = asyncio.run(douyin_setup(account_file, handle=False))
    if cookie_ok:
        app = DouYinVideo(title, video_file, tags, 0, account_file)
        asyncio.run(app.main())
    "
    ```
*   **Success Criteria**:
    * `[+] Cookie 有效` - Cookie verification passed
    * `[+] 成功进入version_2发布页面` - Page navigation successful
    * `[+] 视频上传完毕` - Video upload completed
    * `[+] 视频发布成功` - Publish confirmed

### 5. Encoding Issue Workaround
*   **Problem**: Windows GBK encoding causes `UnicodeEncodeError` with emoji/special chars
*   **Solution**: Use ASCII characters in print statements, or run in proper encoding environment
*   **Workaround**: The upload still succeeds despite the error message display issue

