import requests
import base64
import json

# Configuration
JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_url(encoded_str):
    if not encoded_str:
        return None
    try:
        # Step 1: Strip the prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # Step 2: Fix Base64 padding if necessary
        missing_padding = len(encoded_str) % 4
        if missing_padding:
            encoded_str += '=' * (4 - missing_padding)
        
        # Step 3: Decode
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8').strip()
    except Exception as e:
        print(f"Error decoding string: {e}")
        return None

def main():
    print(f"Fetching data from {JSON_URL}...")
    try:
        response = requests.get(JSON_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Failed to fetch or parse JSON: {e}")
        return

    # Check if data is a list; if not, look for common keys like 'data' or 'channels'
    channels_list = data if isinstance(data, list) else data.get("data", data.get("channels", []))

    count = 0
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        for item in channels_list:
            # Try both 'channel' and 'Channel' to be safe
            raw_val = item.get("channel") or item.get("Channel")
            if raw_val:
                final_url = decode_url(raw_val)
                if final_url:
                    name = item.get("name") or item.get("title") or "Sports Channel"
                    f.write(f"#EXTINF:-1, {name}\n")
                    f.write(f"{final_url}\n")
                    count += 1
    
    print(f"Successfully generated {OUTPUT_FILE} with {count} channels.")

if __name__ == "__main__":
    main()
