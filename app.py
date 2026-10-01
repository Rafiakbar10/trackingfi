from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

PLATFORMS = [
    {"name": "Instagram", "url": "https://www.instagram.com/{}"},
    {"name": "TikTok", "url": "https://www.tiktok.com/@{}"},
    {"name": "Facebook", "url": "https://www.facebook.com/public/{}"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com/pub/dir?firstName={}&lastName=&trkid=bf-guest-home-page-guest-search-submit"},
    {"name": "Pinterest", "url": "https://www.pinterest.com/search/users/?q={}"},
    {"name": "Twitter / X", "url": "https://x.com/search?q={}&src=typed_query"},
    {"name": "GitHub", "url": "https://github.com/search?q={}&type=users"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    query_type = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        query_type = request.form.get("query_type", "name")

        if query:
            clean_query = urllib.parse.quote(query)
            formatted_username = query.lower().replace(" ", "")

            for platform in PLATFORMS:
                if query_type == "name":
                    target = clean_query if "LinkedIn" in platform["name"] or "Pinterest" in platform["name"] or "Twitter" in platform["name"] else formatted_username
                else:
                    target = clean_query

                results.append({
                    "platform": platform["name"],
                    "link": platform["url"].format(target)
                })

    return render_template("index.html", results=results, query=query, query_type=query_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
