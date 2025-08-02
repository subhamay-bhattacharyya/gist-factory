import requests
import os
import sys

# Get GitHub token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("❌ Error: Environment variable 'GITHUB_TOKEN' is not set.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_secret_gists():
    page = 1
    per_page = 100
    secret_gists = []

    while True:
        url = f"https://api.github.com/gists?per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ Failed to fetch gists: {response.status_code}")
            print(response.json())
            break

        gists = response.json()
        if not gists:
            break

        for gist in gists:
            if not gist.get("public", True):
                secret_gists.append({
                    "id": gist["id"],
                    "description": gist["description"],
                    "url": gist["html_url"],
                    "files": list(gist["files"].keys())
                })

        page += 1

    return secret_gists

if __name__ == "__main__":
    gists = fetch_secret_gists()
    if gists:
        print(f"🔐 Found {len(gists)} secret gist(s):")
        for g in gists:
            print(f"- {g['description'] or 'No description'}: {g['url']} ({', '.join(g['files'])})")
    else:
        print("ℹ️ No secret gists found.")
