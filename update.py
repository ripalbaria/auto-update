import requests
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Configuration
JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

# Common keys for this template. 
# If these don't work, the key is unique to your APK version.
AES_KEY = b'1234567890123456' 
AES_IV  = b'1234567890123456'

def decrypt_channel(encoded_str):
    if not encoded_str: return None
    try:
        # 1. Remove Prefix
        clean_str = encoded_str.replace(PREFIX, "")
        
        # 2. Fix Base64 Padding
        missing_padding = len(clean_str) % 4
        if missing_padding:
            clean_str += '=' * (4 - missing_padding)
            
        # 3. Decode Base64
        encrypted_bytes = base64.b64decode(clean_str)
        
        # 4. AES-128-CBC Decryption
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        return decrypted.decode('utf-8').strip()
    except Exception as e:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"} #
    print(f"Fetching from {JSON_URL}...")
    
    try:
        response = requests.get(JSON_URL, headers=headers, timeout=15)
        data = response.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in data:
                raw_val = item.get("channel")
                url = decrypt_channel(raw_val)
                
                if url and url.startswith("http"):
                    name = item.get("name") or f"Channel {count+1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        print(f"Success! Decoded {count} channels into {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
