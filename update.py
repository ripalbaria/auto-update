import requests
import base64
import json

JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_url(encoded_str):
    if not encoded_str: return None
    try:
        # 1. Remove custom prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # 2. Fix Base64 padding
        missing_padding = len(encoded_str) % 4
        if missing_padding:
            encoded_str += '=' * (4 - missing_padding)
        
        # 3. Decode to BYTES (do not .decode('utf-8') yet)
        decoded_bytes = base64.b64decode(encoded_str)
        
        # If the data is text, it will work here. 
        # If it is encrypted binary, this will catch the error and return the raw hex for debugging.
        try:
            return decoded_bytes.decode('utf-8').strip()
        except UnicodeDecodeError:
            # This is where your previous script was failing. 
            # We will return the binary as hex so you can see it in the logs.
            return f"ENCRYPTED_DATA:{decoded_bytes.hex()[:20]}..." 
            
    except Exception as e:
        print(f"Failed to process string: {e}")
        return None

def main():
    print(f"Fetching: {JSON_URL}")
    try:
        response = requests.get(JSON_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        channels = data if isinstance(data, list) else data.get("channels", data.get("data", []))
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in channels:
                raw_val = item.get("channel") or item.get("Channel")
                url = decode_url(raw_val)
                if url:
                    name = item.get("name") or "Channel"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        print(f"Success! Processed {count} items into {OUTPUT_FILE}")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
