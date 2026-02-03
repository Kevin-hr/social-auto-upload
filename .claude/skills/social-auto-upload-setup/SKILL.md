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

## 🚀 Proven Workflows (The "Golden Path")

Follow these verified steps to replicate success.

### Phase 1: Environment Initialization
**Goal**: prevent "File Not Found" and "DB Missing" errors.
**Action**:
```bash
python .claude/skills/social-auto-upload-setup/scripts/setup_environment.py
```
**Outcome**: Ensures `conf.py` covers Chrome paths, and `cookiesFile/` exists for isolation.

### Phase 2: Authentication & Cookie Capture
**Goal**: Acquire persistent sessions without polluting the main browser profile.

#### 🎵 Douyin (抖音)
1.  **Run**: `python .claude/skills/social-auto-upload-setup/scripts/get_douyin_cookie_auto.py`
2.  **User Action**: Scan QR code with Douyin App.
3.  **Result**: Cookie saved to `cookiesFile/douyin_uploader/account.json`.

#### ⚡ Kuaishou (快手)
1.  **Run**: `python .claude/skills/social-auto-upload-setup/scripts/get_ks_cookie_auto.py`
2.  **User Action**: Scan QR code with Kuaishou App.
3.  **Result**: Cookie saved to `cookiesFile/ks_uploader/account.json`.

#### 💬 WeChat Channels (视频号)
*This platform requires strict mobile confirmation.*
1.  **Run**: `python .claude/skills/social-auto-upload-setup/scripts/get_tencent_cookie_auto.py`
2.  **User Action**:
    *   Browser opens `channels.weixin.qq.com`.
    *   **CRITICAL**: Use **Mobile WeChat (手机微信)** to scan.
    *   Confirm login on phone.
3.  **Result**: Script detects URL change/avatar load and saves verified `account.json` to `cookiesFile/tencent_uploader/`.

#### 🌸 Xiaohongshu (小红书)
1.  **Run**: `python .claude/skills/social-auto-upload-setup/scripts/get_xhs_cookie_auto.py`
2.  **User Action**: Scan QR code with Xiaohongshu App.
3.  **Result**: Cookie saved to `cookiesFile/xhs_uploader/account.json`.

### Phase 3: Validation & Upload Testing
**Goal**: Confirm the pipeline works before attempting bulk tasks.
**Auto-Recovery**: These scripts include a `ensure_metadata()` fix. If your video `test.mp4` lacks `test.txt`, the script **automatically generates it** to prevent immediate crashes.

**Douyin**:
```bash
python .claude/skills/social-auto-upload-setup/scripts/upload_douyin_simple.py
```

**Kuaishou**:
```bash
python .claude/skills/social-auto-upload-setup/scripts/upload_ks_simple.py
```

**WeChat Channels**:
```bash
python .claude/skills/social-auto-upload-setup/scripts/upload_tencent_simple.py
```

**Xiaohongshu**:
```bash
python .claude/skills/social-auto-upload-setup/scripts/upload_xhs_simple.py
```

---

## 🧠 Historical Experience & Engineering Notes

These notes document "Why things are done this way" based on verified success.

### 1. The "Metadata Crash" Fix
*   **Context**: The upstream `social-auto-upload` project crashes if `.txt` metadata files are missing.
*   **Solution**: We do not strictly require users to create these manually for testing. The `upload_*_simple.py` wrappers in this skill perform a "Pre-flight Check".
*   **Logic**: `if not txt_exists: create_default_txt(title=filename, tags=['#daily'])`.
*   **Benefit**: Users can drop a raw `.mp4` into `videos/` and run the validater immediately.

### 2. Cookie Isolation Architecture
*   **Context**: Default browser profiles often have stale sessions or conflicting extensions.
*   **Solution**: This skill uses `playwright.chromium.launch(storage_state=specific_json)`.
*   **Structure**:
    *   `cookiesFile/douyin_uploader/account.json`
    *   `cookiesFile/ks_uploader/account.json`
    *   `cookiesFile/tencent_uploader/account.json`
    *   `cookiesFile/xhs_uploader/account.json`
*   **Benefit**: Zero cross-contamination between platforms.

### 3. Platform-Specific Notes
*   **WeChat Channels (视频号)**: ⭐⭐⭐⭐⭐ Proven.
    *   **Login**: Requires active mobile WeChat confirmation.
    *   **Originality**: The script attempts to handle "Original" declarations automatically if eligible, but manual intervention may be needed if the account has penalties.
*   **Xiaohongshu (小红书)**: ⭐⭐⭐⭐ High capability, high fragility.
    *   **Selectors**: site structure updates frequently. We implemented fallback selectors for description (`#post-textarea`, `div[contenteditable='true']`).
    *   **Intervention**: May trigger captchas or "Agree to Terms" pop-ups during upload. Manual clicking in the headed browser is often required to proceed.
*   **Login Timeout**: The `get_tencent_cookie_auto.py` script waits up to 300 seconds (5 mins) because WeChat mobile confirmation can sometimes be slow or require network switching.

### 4. Code Resilience
*   **Experience**: Standard project code in `xhs_uploader` had obsolete selectors for the description box. We patched it to use a list of fallback selectors and added error handling to ensure the upload logic doesn't crash if optional fields (like tags) fail.

### 5. Chrome Integration
*   **Context**: Playwright needs a headful Chrome for QR scanning.
*   **Solution**: `setup_environment.py` writes a `conf.py` pointing to `C:/Program Files/Google/Chrome/Application/chrome.exe`.
*   **Verification**: Verified working on Windows 10/11 environments.
