import requests
import urllib.parse

BRANCH_URL = "https://district5.scenecinemas.com/branches/scene-district-5.html"
DEFAULT_TOPIC = "amr_scene_tickets_2026"

safe_topic = urllib.parse.quote(DEFAULT_TOPIC)
ntfy_url = f"https://ntfy.sh/{safe_topic}"

# Use a standard desktop browser User-Agent to avoid simple bot blocks
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

try:
    print("Testing connection to Scene Cinema...")
    response = requests.get(BRANCH_URL, headers=headers, timeout=15)
    
    print(f"Website HTTP Status Code: {response.status_code}")
    print(f"Response text length: {len(response.text)}")

    # FORCE a notification right now to test if ntfy.sh is working
    test_message = f"Diagnostic Test: HTTP Status {response.status_code} (Length: {len(response.text)})"
    
    requests.post(
        ntfy_url,
        data=test_message.encode("utf-8"),
        headers={
            "Title": "Watcher Test Ping",
            "Priority": "default",
            "Tags": "bell",
        },
        timeout=10
    )
    print("Test notification dispatched to ntfy!")

except Exception as e:
    error_msg = f"❌ Error connecting to cinema: {str(e)}"
    print(error_msg)
    
    # Send error to your phone so you know it failed
    requests.post(
        ntfy_url,
        data=error_msg.encode("utf-8"),
        headers={"Title": "Watcher Error", "Priority": "high"},
        timeout=10
    )
