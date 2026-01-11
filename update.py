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

# The Master Key found in your screenshot
MASTER_KEY = b"a56c44959930c1ef89e2787c607b0f9c"
MASTER_IV  = MASTER_KEY[:16]

def aes_decrypt(data, key, iv):
    try:
        # Step 1: Remove Prefix
        clean_data = data.replace(PREFIX, "") if PREFIX in data else data
        
        # Step 2: Fix Base64 Padding
        missing_padding = len(clean_data) % 4
        if missing_padding:
            clean_data += '=' * (4 - missing_padding)
        
        # Step 3: Decrypt
        raw_bytes = base64.b64decode(clean_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(raw_bytes), AES.block_size)
        return decrypted.decode('utf-8')
    except:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"} #
    
    print("Step 1: Unlocking Handshake (app.json)...")
    try:
        # Fetch the config from the server
        conf_res = requests.get(CONFIG_URL, headers=headers, timeout=10)
        config_json = conf_res.json()
        
        # The 'events' field in your app.json is a stringified list
        events_str = config_json[0]['events']
        events_list = json.loads(events_str)
        
        # We decrypt the first event to initialize the session
        session_info = aes_decrypt(events_list[0], MASTER_KEY, MASTER_IV)
        
        if session_info:
            print("Handshake successful.")
        else:
            print("Handshake failed to decrypt session info.")
    except Exception as e:
        print(f"Config Error: {e}")

    print("Step 2: Decrypting Channels...")
    try:
        response = requests.get(CHANNELS_URL, headers=headers, timeout=15)
        channels = response.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in channels:
                # Using the Master Key on channels as a fallback
                url = aes_decrypt(item.get("channel"), MASTER_KEY, MASTER_IV)
                
                if url and url.startswith("http"):
                    name = item.get("name") or f"Channel {count+1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        print(f"Successfully processed {count} channels.")
    except Exception as e:
        print(f"Channel Fetch Error: {e}")

if __name__ == "__main__":
    main()
