import os
import requests
import urllib.parse

BRANCH_URL = "https://district5.scenecinemas.com/branches/scene-district-5.html"
MOVIE_URL = "https://district5.scenecinemas.com/movie-details/the-odyssey.html"
DEFAULT_TOPIC = "amr_scene_tickets_2026"

# Target configuration
MOVIE = "The Odyssey"
EXP = ""
DATE = ""
TIME = ""

safe_topic = urllib.parse.quote(DEFAULT_TOPIC)
ntfy_url = f"https://ntfy.sh/{safe_topic}"

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    print("Checking Scene Cinema...")
    res_branch = requests.get(BRANCH_URL, headers=headers, timeout=10)
    res_movie = requests.get(MOVIE_URL, headers=headers, timeout=10)
    
    combined_html = (res_branch.text + " " + res_movie.text).lower()
    clean_html = combined_html.replace(" ", "")

    movie_match = MOVIE.lower() in combined_html if MOVIE else True
    exp_match = EXP.lower().replace(" ", "") in clean_html if EXP else True
    date_match = DATE.lower().replace(" ", "") in clean_html if DATE else True
    time_match = TIME.lower().replace(" ", "") in clean_html if TIME else True

    if movie_match and exp_match and date_match and time_match:
        print("🎉 TICKETS AVAILABLE!")
        payload_data = f"Showtimes for {MOVIE.upper()} ({EXP.upper()}) are live at District 5! Tap to book now."
        
        requests.post(
            ntfy_url,
            data=payload_data.encode("utf-8"),
            headers={
                "Title": "TICKETS ARE LIVE!",
                "Priority": "high",
                "Tags": "clapper,ticket",
                "Click": BRANCH_URL,
            },
            timeout=10
        )
    else:
        print("[-] Showtimes not open yet.")

except Exception as e:
    print(f"❌ Network error: {e}")
