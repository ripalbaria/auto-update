import requests
import base64
import json

# Configuration
JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_url(encoded_str):
    try:
        # Step 1: Remove the specific prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # Step 2: Decode Base64
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8').strip()
    except Exception as e:
        print(f"Error decoding: {e}")
        return None

def main():
    print(f"Fetching data from {JSON_URL}...")
    response = requests.get(JSON_URL, timeout=10)
    
    if response.status_code != 200:
        print("Failed to fetch JSON file.")
        return

    data = response.json()
    
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        for item in data:
            # Note: We use .get("channel") based on your screenshot
            raw_channel = item.get("channel", "")
            final_url = decode_url(raw_channel)
            
            if final_url:
                # Giving a default name; if JSON has a 'name' key, replace 'Channel' with item.get('name')
                f.write(f"#EXTINF:-1, Sports Channel\n")
                f.write(f"{final_url}\n")
    
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
