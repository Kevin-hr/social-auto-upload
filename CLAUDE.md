# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

`social-auto-upload` is an automation tool for publishing videos to multiple social media platforms (Douyin, Bilibili, Xiaohongshu, Kuaishou, WeChat Channel, Baijiahao, TikTok).

**Tech Stack:**
- **Backend**: Flask (port 5409)
- **Frontend**: Vue 3 + Vite + Element Plus + Pinia + Vue Router
- **Browser Automation**: Playwright
- **Database**: SQLite (`db/database.db`)

## Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Install browser drivers
playwright install chromium

# Initialize database
python db/createTable.py

# Run server
python sau_backend.py
```

### Frontend
```bash
cd sau_frontend
npm install
npm run dev     # dev server on port 5173
npm run build   # production build
```

### CLI
```bash
# Login
python cli_main.py <platform> <account_name> login

# Upload (immediate)
python cli_main.py <platform> <account_name> upload <video_file>

# Upload (scheduled)
python cli_main.py <platform> <account_name> upload <video_file> -pt 1 -t "YYYY-MM-DD HH:MM"
```

## Architecture

### Directory Structure
- `sau_backend.py` - Flask API entry point
- `cli_main.py` - CLI entry point
- `db/` - SQLite database and schema
- `sau_frontend/` - Vue.js frontend
- `uploader/<platform>_uploader/` - Platform-specific upload modules
- `myUtils/` - Core utilities (auth, login, postVideo)
- `utils/` - Shared utilities (logging, constants, file helpers)
- `examples/` - Example scripts for each platform

### Database Schema
- `user_info`: Accounts (id, type, filePath, userName, status)
- `file_records`: Uploaded files (id, filename, filesize, upload_time, file_path)

**Platform Type Mapping:**
- `1` = Xiaohongshu
- `2` = WeChat Channel/Tencent
- `3` = Douyin
- `4` = Kuaishou

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Quick file upload |
| `/uploadSave` | POST | Upload and save to DB |
| `/getFiles` | GET | List all files |
| `/deleteFile` | GET | Delete file by ID |
| `/getAccounts` | GET | List all accounts |
| `/getValidAccounts` | GET | List accounts with cookie validation |
| `/deleteAccount` | GET | Delete account by ID |
| `/updateUserinfo` | POST | Update account info |
| `/uploadCookie` | POST | Upload cookie JSON file |
| `/downloadCookie` | GET | Download cookie file |
| `/login` | GET | SSE login (type, id params) |
| `/postVideo` | POST | Trigger video upload |

### Storage
- **Cookies**: `cookiesFile/` - JSON files per account
- **Videos**: `videoFile/` - Uploaded video files
- **Browser State**: Playwright storage state files

## Adding a New Platform

1. **Create uploader module**: `uploader/<platform>_uploader/main.py`
   - Implement `<Platform>Video` class with `upload()` method
   - Implement `xxx_setup()` for login/cookie generation

2. **Update backend**: `sau_backend.py`
   - Add route handler in `run_async_function()`
   - Add video posting logic in `/postVideo` and `/postVideoBatch`

3. **Update utils**: `utils/base_social_media.py`
   - Add `SOCIAL_MEDIA_<PLATFORM>` constant
   - Update `get_supported_social_media()`

4. **Update CLI**: `cli_main.py`
   - Import and wire up new uploader

5. **Database**: Add account via frontend or direct SQL

## Configuration

Copy `conf.example.py` to `conf.py`:
- `LOCAL_CHROME_PATH` - Chrome executable path
- `LOCAL_CHROME_HEADLESS` - Run browser headless
- `XHS_SERVER` - Xiaohongshu API server
