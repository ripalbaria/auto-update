import requests
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration
CONFIG_URL = "http://sufyanpromax.space/app.json"
CHANNELS_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

# Ye key app.json ke events block ko unlock karti hai
MASTER_KEY = b"a56c44959930c1ef89e2787c607b0f9c"
MASTER_IV  = MASTER_KEY[:16]

def decrypt_data(encrypted_str, key, iv):
    if not encrypted_str: return None
    try:
        # Remove prefix
        clean_str = encrypted_str.replace(PREFIX, "") if PREFIX in encrypted_str else encrypted_str
        # Fix padding
        missing_padding = len(clean_str) % 4
        if missing_padding:
            clean_str += '=' * (4 - missing_padding)
        # Decode and Decrypt
        raw_bytes = base64.b64decode(clean_str)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(raw_bytes), AES.block_size).decode('utf-8').strip()
    except:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"}
    
    print("Step 1: Handshake - Extracting Session Key...")
    try:
        conf_res = requests.get(CONFIG_URL, headers=headers, timeout=10)
        events_block = conf_res.json().get("events", [""])[0]
        # Events block decrypt karke asli key dhundna
        decrypted_config = decrypt_data(events_block, MASTER_KEY, MASTER_IV)
        print("Session Key Extracted.")
    except Exception as e:
        print(f"Handshake failed: {e}")

    print("Step 2: Fetching and Unlocking Channels...")
    try:
        response = requests.get(CHANNELS_URL, headers=headers, timeout=15)
        channels = response.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in channels:
                raw_val = item.get("channel")
                # Channels ko unlock karne ki koshish
                url = decrypt_data(raw_val, MASTER_KEY, MASTER_IV)
                
                if url and url.startswith("http"):
                    name = item.get("name") or f"Channel {count+1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        if count > 0:
            print(f"Success! {count} channels added to {OUTPUT_FILE}")
        else:
            print("Final Decryption failed. The app is using a rotating session key.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
