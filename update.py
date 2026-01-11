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

# Key found in screenshot 57198.jpg
MASTER_KEY = b"a56c44959930c1ef89e2787c607b0f9c"
MASTER_IV  = MASTER_KEY[:16]

def decrypt_payload(encrypted_str, key, iv):
    if not encrypted_str: return None
    try:
        # Step 1: Remove Prefix
        clean_str = encrypted_str.replace(PREFIX, "") if PREFIX in encrypted_str else encrypted_str
        # Step 2: Base64 Decode
        raw_bytes = base64.b64decode(clean_str.strip())
        # Step 3: AES-CBC Decryption
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(raw_bytes), AES.block_size)
        return decrypted.decode('utf-8').strip()
    except:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"} #
    
    print("Fetching Handshake Config...")
    try:
        # app.json se events block read karna
        conf_res = requests.get(CONFIG_URL, headers=headers, timeout=10)
        config_data = conf_res.json()
        # Events block decrypt karne ki koshish (Optional but helps session)
        events = config_data.get("events", [""])[0]
        decrypt_payload(events, MASTER_KEY, MASTER_IV)
    except:
        pass

    print("Fetching and Decrypting Channels...")
    try:
        chan_res = requests.get(CHANNELS_URL, headers=headers, timeout=15)
        channels = chan_res.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in channels:
                raw_val = item.get("channel")
                # Har channel ko decrypt karna
                url = decrypt_payload(raw_val, MASTER_KEY, MASTER_IV)
                
                if url and url.startswith("http"):
                    name = item.get("name") or f"Channel {count+1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        if count > 0:
            print(f"Success! {count} channels added to {OUTPUT_FILE}")
        else:
            print("Decryption failed. The key 'a56c4495...' might be only for ads.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
