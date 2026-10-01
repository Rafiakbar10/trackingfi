from flask import Flask, render_template, request, jsonify
import re
import requests
from urllib.parse import quote

app = Flask(__name__)

PLATFORMS = {
    "Instagram": "https://www.instagram.com/{q}/",
    "TikTok": "https://www.tiktok.com/@{q}",
    "Facebook": "https://www.facebook.com/{q}",
    "LinkedIn": "https://www.linkedin.com/in/{q}/",
    "Pinterest": "https://www.pinterest.com/{q}/",
    "X": "https://x.com/{q}",
    "YouTube": "https://www.youtube.com/@{q}",
    "GitHub": "https://github.com/{q}",
    "Reddit": "https://www.reddit.com/user/{q}/",
    "Telegram": "https://t.me/{q}",
}

USERNAME_RE = re.compile(r"^[A-Za-z0-9._-]{2,80}$")

def clean_username(value):
    value = value.strip()
    value = re.sub(r"^@", "", value)
    return value

def public_profile_check(url):
    """Best-effort public URL check. A result is only a lead, not identity proof."""
    try:
        r = requests.get(
            url,
            timeout=7,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 SocialFinder/1.0"}
        )
        # Some platforms return 200 for login/challenge pages, so HTTP 200
        # is deliberately marked as 'possible', not 'confirmed'.
        if 200 <= r.status_code < 300:
            return {"status": "possible", "http_status": r.status_code, "url": r.url}
        if r.status_code == 404:
            return {"status": "not_found", "http_status": r.status_code, "url": url}
        return {"status": "unknown", "http_status": r.status_code, "url": url}
    except requests.RequestException as e:
        return {"status": "unknown", "error": str(e), "url": url}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/search")
def search():
    data = request.get_json(silent=True) or {}
    query = str(data.get("query", "")).strip()
    mode = data.get("mode", "username")

    if not query:
        return jsonify({"error": "Masukkan username atau kata pencarian."}), 400

    if mode == "phone":
        # Do not attempt to reverse-map private phone numbers to social accounts.
        digits = re.sub(r"\D", "", query)
        if len(digits) < 8:
            return jsonify({"error": "Nomor HP tampaknya tidak valid."}), 400
        return jsonify({
            "mode": "phone",
            "query": query,
            "message": "Pencarian nomor HP langsung ke akun sosial tidak dilakukan. "
                       "Gunakan username publik atau layanan/API resmi yang memiliki izin."
        })

    username = clean_username(query)
    if not USERNAME_RE.match(username):
        return jsonify({"error": "Untuk mode username gunakan 2–80 karakter: huruf, angka, titik, _, atau -."}), 400

    results = []
    for name, template in PLATFORMS.items():
        url = template.format(q=quote(username))
        result = public_profile_check(url)
        result["platform"] = name
        results.append(result)

    return jsonify({
        "mode": "username",
        "query": username,
        "disclaimer": "Hasil adalah lead berdasarkan halaman publik; bukan verifikasi identitas.",
        "results": results
    })

@app.get("/api/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
