import requests
import urllib.parse

BRANCH_URL = "https://district5.scenecinemas.com/branches/scene-district-5.html"
MOVIE_URL = "https://district5.scenecinemas.com/movie-details/the-odyssey.html"
DEFAULT_TOPIC = "amr_scene_tickets_2026"

# ==========================================
# TARGET CONFIGURATION (Change these anytime)
# ==========================================
MOVIE = "Dune"
EXP = ""
DATE = ""  # Leave blank "" to match any date, or enter e.g. "2026-06-15"
TIME = ""  # Leave blank "" to match any time, or enter e.g. "21:00"
# ==========================================

safe_topic = urllib.parse.quote(DEFAULT_TOPIC)
ntfy_url = f"https://ntfy.sh/{safe_topic}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

try:
    print("Checking Scene Cinema District 5...")
    res_branch = requests.get(BRANCH_URL, headers=headers, timeout=15)
    res_movie = requests.get(MOVIE_URL, headers=headers, timeout=15)
    
    combined_html = (res_branch.text + " " + res_movie.text).lower()
    clean_html = combined_html.replace(" ", "")

    movie_match = MOVIE.lower() in combined_html if MOVIE else True
    exp_match = EXP.lower().replace(" ", "") in clean_html if EXP else True
    date_match = DATE.lower().replace(" ", "") in clean_html if DATE else True
    time_match = TIME.lower().replace(" ", "") in clean_html if TIME else True

    if movie_match and exp_match and date_match and time_match:
        print("🎉 TICKETS ARE AVAILABLE!")
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
        print("[-] Showtimes not open yet. Staying quiet.")

except Exception as e:
    print(f"❌ Error checking cinema: {e}")
