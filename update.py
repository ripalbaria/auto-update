import requests
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration
CHANNELS_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

# Aapki dhundi hui key (Screenshot 57198.jpg se)
RAW_KEY = b"a56c44959930c1ef89e2787c607b0f9c"
AES_KEY = RAW_KEY 
AES_IV  = RAW_KEY[:16] # Pehle 16 chars IV ke liye

def decrypt_url(encoded_str):
    if not encoded_str: return None
    try:
        # Prefix ko remove karein
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # Base64 padding fix karein
        missing_padding = len(encoded_str) % 4
        if missing_padding:
            encoded_str += '=' * (4 - missing_padding)
            
        encrypted_bytes = base64.b64decode(encoded_str)
        
        # AES-256-CBC Decryption logic
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted.decode('utf-8').strip()
    except Exception:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"} #
    print("Fetching and Decrypting channels...")
    
    try:
        response = requests.get(CHANNELS_URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in data:
                raw_val = item.get("channel")
                url = decrypt_url(raw_val)
                
                if url and url.startswith("http"):
                    name = item.get("name") or f"Channel {count+1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        print(f"Success! {count} channels added to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
