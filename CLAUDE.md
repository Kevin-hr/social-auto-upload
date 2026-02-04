# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

`social-auto-upload` is an automation tool for publishing videos to multiple social media platforms (Douyin, Bilibili, Xiaohongshu, Kuaishou, WeChat Channel, Baijiahao, TikTok).

**Tech Stack:**
- **Backend**: Flask (port 5409, dynamic on Railway)
- **Frontend**: Vue 3 + Vite + Element Plus + Pinia + Vue Router
- **Browser Automation**: Playwright
- **Database**: SQLite (`db/database.db` and `db/upload_state.db`)
- **Deployment**: Docker + Railway

## Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Install browser drivers
playwright install chromium firefox

# Initialize database
python db/createTable.py

# Run server (local)
python sau_backend.py
```

### Frontend
```bash
cd sau_frontend
npm install
npm run dev     # dev server on port 5173
npm run build   # production build
```

### Docker/Railway
```bash
# Build and run locally
docker build -t social-auto-upload .
docker run -p 5409:5409 social-auto-upload

# Railway deployment (railway.json configured)
railway up
```

### Electron Desktop
```bash
cd sau_frontend
npm run electron:dev     # Dev mode with local backend
npm run electron:build   # Build cross-platform installer (.exe)
```

### CLI & Turbo
```bash
# Interactive CLI
python cli_main.py [platform] [account_name] [action]
# Example: python cli_main.py douyin myAccount upload video.mp4

# Turbo Publish (Auto-scan and publish all platforms from C:\Users\52648\Videos\社媒发布)
python cli_turbo_publish.py
```

## Architecture

### Directory Structure
- `sau_backend.py` - Flask API entry point
- `cli_main.py` - CLI entry point
- `db/` - SQLite database and schema
- `sau_frontend/` - Vue.js frontend
- `uploader/` - Platform-specific upload modules
    - `douyin_uploader/main.py`
    - `bilibili_uploader/main.py`
    - `xhs_uploader/main.py` (and `xiaohongshu_uploader`)
    - `ks_uploader/main.py`
    - `tencent_uploader/main.py`
    - `baijiahao_uploader/main.py`
    - `tk_uploader/main_chrome.py`
- `myUtils/` - Core utilities (bridge between backend and uploaders)
    - `postVideo.py` - High-level upload wrappers
    - `login.py` - Browser login handlers
    - `auth.py` - Cookie verification
- `utils/` - Shared utilities (logging, constants, file helpers)
- `examples/` - Example scripts for each platform

### Database Schema
- `user_info`: Accounts (id, type, filePath, userName, status)
- `file_records`: Uploaded files (id, filename, filesize, upload_time, file_path)
- `upload_history` (in `upload_state.db`): Upload status tracking

**Platform Type Mapping:**
- `1` = Xiaohongshu (小红书)
- `2` = WeChat Channel/Tencent (视频号/腾讯)
- `3` = Douyin (抖音)
- `4` = Kuaishou (快手)
- `5` = Toutiao (头条)
- `6` = TikTok
- `7` = Bilibili (哔哩哔哩)
- `8` = Baijiahao (百家号)

### Key Directories
- `cookiesFile/` - Stores account cookies (json)
- `videoFile/` - Stores video files for backend upload

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Quick file upload |
| `/uploadSave` | POST | Upload and save to DB |
| `/getFiles` | GET | List all files |
| `/deleteFile` | GET | Delete file by ID |
| `/getAccounts` | GET | List all accounts |
| `/getValidAccounts` | GET | List validated accounts |
| `/deleteAccount` | GET | Delete account by ID |
| `/updateUserinfo` | POST | Update account info |
| `/uploadCookie` | POST | Upload cookie JSON file |
| `/downloadCookie` | GET | Download cookie file |
| `/login` | GET | SSE login stream (type, id params) |
| `/addAccount` | POST | Add account + cookie path |
| `/postVideo` | POST | Trigger video upload |
| `/postVideoBatch` | POST | Batch upload videos |
| `/getStats` | GET | Dashboard statistics |

### Adding a New Platform

1. **Create uploader module**: `uploader/<platform>_uploader/main.py`
   - Implement `<Platform>Video` class with `upload()` method
   - Implement `xxx_setup()` for browser-based login/cookie generation

2. **Update backend**: `sau_backend.py`
   - Add route handler in `run_async_function()`
   - Add video posting logic in `/postVideo` and `/postVideoBatch`

3. **Update utils**: `utils/base_social_media.py`
   - Add `SOCIAL_MEDIA_<PLATFORM>` constant
   - Update `get_supported_social_media()`

4. **Update CLI**: `cli_main.py`
   - Import and wire up new uploader

5. **Database**: Add account via frontend or direct SQL

### Platform Cookie Scripts

| Platform | Cookie Script Path |
|----------|-------------------|
| Douyin | `uploader/douyin_uploader/get_douyin_cookie.py` |
| Kuaishou | `uploader/ks_uploader/get_ks_cookie.py` |
| Xiaohongshu | `uploader/xhs_uploader/get_xhs_cookie.py` |
| Tencent | `uploader/tencent_uploader/get_tencent_cookie.py` |
| Bilibili | `uploader/bilibili_uploader/get_bilibili_cookie.py` |
| TikTok | `uploader/tk_uploader/get_tk_cookie.py` |

## Configuration

### Environment Variables (Railway)
- `PORT` - Railway dynamic port (handled automatically)
- `VITE_API_BASE_URL` - Frontend API URL (set during build)
- `RAILWAY_ENVIRONMENT` - Railway environment detection

### Local Config
Copy `conf.example.py` to `conf.py`:
- `LOCAL_CHROME_PATH` - Chrome executable path
- `LOCAL_CHROME_HEADLESS` - Run browser headless

## Deployment

### Railway
- `railway.json` - Deployment configuration
- `Dockerfile` - Multi-stage build (Python + Node.js)
- Start command: `python sau_backend.py` (dynamic port binding)

### Claude Skills
- `.claude/skills/social-auto-upload-setup/` - Complete setup automation
- `.claude/skills/railway-deployment/` - Railway deployment automation
