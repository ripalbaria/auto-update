import requests
import base64
import json

JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_url(encoded_str):
    if not encoded_str: return None
    try:
        # Remove prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # FIX: Padding must make string length a multiple of 4
        missing_padding = len(encoded_str) % 4
        if missing_padding:
            encoded_str += '=' * (4 - missing_padding)
        
        return base64.b64decode(encoded_str).decode('utf-8').strip()
    except Exception as e:
        print(f"Failed to decode: {e}")
        return None

def main():
    try:
        response = requests.get(JSON_URL, timeout=10)
        data = response.json()
        
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in data:
                raw_channel = item.get("channel")
                url = decode_url(raw_channel)
                if url:
                    f.write(f"#EXTINF:-1, {item.get('name', 'Channel')}\n{url}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
