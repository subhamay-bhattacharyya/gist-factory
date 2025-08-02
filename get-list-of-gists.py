import requests
import os
import sys
import json

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
                gist_id = gist["id"]
                description = gist.get("description", "")
                files = gist.get("files", {})

                for filename, file_info in files.items():
                    raw_url = file_info.get("raw_url")
                    content = None
                    if raw_url:
                        content_response = requests.get(raw_url, headers=HEADERS)
                        if content_response.status_code == 200:
                            content = content_response.text
                        else:
                            content = f"[Failed to fetch content: {content_response.status_code}]"

                    secret_gists.append({
                        "id": gist_id,
                        "description": description,
                        "filename": filename,
                        "content": content
                    })

        page += 1

    return secret_gists

if __name__ == "__main__":
    gists = fetch_secret_gists()
    if gists:
        print(f"🔐 Found {len(gists)} secret gist file(s):")
        for g in gists:
            print(f"\n📄 Gist ID: {g['id']}")
            print(f"📝 Description: {g['description']}")
            print(f"📁 Filename: {g['filename']}")
            print(f"📄 Content:\n{g['content']}\n{'-'*60}")
        
        # Optional: write to a file
        with open("gists_fetched.json", "w") as f:
            json.dump(gists, f, indent=2)
        print("\n📂 Gists written to gists_fetched.json")
    else:
        print("ℹ️ No secret gists found.")
