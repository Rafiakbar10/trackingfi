from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

# Menggunakan teknik pencarian web (Google Dork style) untuk akurasi tinggi
PLATFORMS = [
    {"name": "LinkedIn", "url": "https://www.google.com/search?q=site:linkedin.com/in/+\"{}\""},
    {"name": "Instagram", "url": "https://www.google.com/search?q=site:instagram.com+\"{}\""},
    {"name": "TikTok", "url": "https://www.google.com/search?q=site:tiktok.com+\"{}\""},
    {"name": "Facebook", "url": "https://www.google.com/search?q=site:facebook.com+\"{}\""},
    {"name": "Pinterest", "url": "https://www.google.com/search?q=site:pinterest.com+\"{}\""},
    {"name": "Twitter / X", "url": "https://www.google.com/search?q=site:twitter.com+\"{}\""},
    {"name": "GitHub", "url": "https://www.google.com/search?q=site:github.com+\"{}\""}
]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    query_type = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        query_type = query.get("query_type", "name") # Memperbaiki ambil data form

        if query:
            clean_query = urllib.parse.quote(query)

            for platform in PLATFORMS:
                results.append({
                    "platform": platform["name"],
                    "link": platform["url"].format(clean_query)
                })

    return render_template("index.html", results=results, query=query, query_type=query_type)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
