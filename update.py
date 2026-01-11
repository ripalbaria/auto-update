import requests
import base64
import json

JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_url(encoded_str):
    if not encoded_str: return None
    try:
        # Step 1: Remove custom prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # Step 2: Fix Base64 padding (Length must be multiple of 4)
        missing_padding = len(encoded_str) % 4
        if missing_padding:
            encoded_str += '=' * (4 - missing_padding)
        
        # Step 3: Decode to plain text
        return base64.b64decode(encoded_str).decode('utf-8').strip()
    except Exception as e:
        print(f"Skipping malformed entry: {e}")
        return None

def main():
    print(f"Fetching: {JSON_URL}")
    try:
        response = requests.get(JSON_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Check for direct list or nested data
        channels = data if isinstance(data, list) else data.get("channels", data.get("data", []))
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in channels:
                raw_val = item.get("channel") or item.get("Channel")
                url = decode_url(raw_val)
                if url:
                    name = item.get("name") or item.get("title") or "Sports Channel"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        print(f"Success! {count} channels added to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
