
import os
import sys
from pathlib import Path

# --- Configuration Template ---
CONF_TEMPLATE = """from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = "http://127.0.0.1:11901"
LOCAL_CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LOCAL_CHROME_HEADLESS = False
"""

def setup_environment():
    cwd = Path.cwd()
    print(f"[*] Initializing environment in: {cwd}")

    # 1. Create conf.py
    conf_path = cwd / "conf.py"
    if not conf_path.exists():
        print("[+] Creating conf.py...")
        with open(conf_path, "w", encoding="utf-8") as f:
            f.write(CONF_TEMPLATE)
    else:
        print("[!] conf.py already exists. Skipping.")

    # 2. Create directories
    for dirname in ["cookiesFile", "videoFile", "videos"]:
        dir_path = cwd / dirname
        if not dir_path.exists():
            print(f"[+] Creating directory: {dirname}")
            dir_path.mkdir(exist_ok=True)
        else:
            print(f"[!] Directory {dirname} exists.")

    # 3. Initialize Database
    db_path = cwd / "db" / "database.db"
    create_table_script = cwd / "db" / "createTable.py"
    
    if not db_path.exists():
        if create_table_script.exists():
            print("[+] Initializing database...")
            exit_code = os.system(f"python {create_table_script}")
            if exit_code == 0:
                print("[+] Database initialized successfully.")
            else:
                print("[-] Database initialization failed.")
        else:
            print("[-] db/createTable.py not found. Cannot init DB.")
    else:
        print("[!] Database already exists.")

    print("\n[+] Environment setup complete!")

if __name__ == "__main__":
    setup_environment()
