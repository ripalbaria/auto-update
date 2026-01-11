import requests
import json
import base64

# Configuration
JSON_URL = "http://sufyanpromax.space/channels/SPORTS-WORLD.json"
PREFIX = "alZhLW1nOzro"
OUTPUT_FILE = "final.m3u"

def decode_sufyan(encoded_str):
    if not encoded_str: return None
    try:
        # Step 1: Remove the known prefix
        if encoded_str.startswith(PREFIX):
            encoded_str = encoded_str.replace(PREFIX, "", 1)
        
        # Step 2: Character Translation Map
        # These apps often swap characters like 'a' with 'n', etc.
        # This is a common IPTV obfuscation pattern.
        source = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        target = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM5678901234"
        trans_table = str.maketrans(target, source)
        translated = encoded_str.translate(trans_table)
        
        # Step 3: Standard Base64 Decode
        missing_padding = len(translated) % 4
        if missing_padding:
            translated += '=' * (4 - missing_padding)
            
        decoded = base64.b64decode(translated).decode('utf-8', errors='ignore')
        
        # Filter only actual URLs
        if "http" in decoded:
            return decoded.split("http")[-1].split("\n")[0].strip().replace(" ", "")
            # Re-add http if it was split
            return "http" + decoded.split("http")[-1].strip()
            
        return None
    except:
        return None

def main():
    headers = {"User-Agent": "okhttp/4.12.0"} # Match your canary logs
    print(f"Fetching from {JSON_URL}...")
    
    try:
        response = requests.get(JSON_URL, headers=headers, timeout=15)
        data = response.json()
        
        count = 0
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for item in data:
                raw_channel = item.get("channel")
                url = decode_sufyan(raw_channel)
                
                if url:
                    # Using a placeholder name; use item.get('name') if available
                    name = f"Channel {count + 1}"
                    f.write(f"#EXTINF:-1, {name}\n{url}\n")
                    count += 1
        
        print(f"Success! Decoded {count} channels into {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
