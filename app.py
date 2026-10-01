from flask import Flask, render_template, request
import urllib.parse
import re

app = Flask(__name__)

# Database Platform yang komprehensif untuk intelijen data
PLATFORMS = {
    "Media Sosial Utama": [
        {"name": "Facebook", "url": "https://www.google.com/search?q=site:facebook.com+{}"},
        {"name": "Instagram", "url": "https://www.google.com/search?q=site:instagram.com+{}"},
        {"name": "TikTok", "url": "https://www.google.com/search?q=site:tiktok.com+{}"},
        {"name": "Twitter / X", "url": "https://www.google.com/search?q=site:twitter.com+{}"},
        {"name": "Pinterest", "url": "https://www.google.com/search?q=site:pinterest.com+{}"},
        {"name": "YouTube", "url": "https://www.google.com/search?q=site:youtube.com+{}"}
    ],
    "Jejak Karir & Profesional": [
        {"name": "LinkedIn", "url": "https://www.google.com/search?q=site:linkedin.com/in/+{}"},
        {"name": "JobStreet", "url": "https://www.google.com/search?q=site:jobstreet.co.id+{}"},
        {"name": "Glints", "url": "https://www.google.com/search?q=site:glints.com/id+{}"}
    ],
    "Marketplace & Transaksi": [
        {"name": "Shopee", "url": "https://www.google.com/search?q=site:shopee.co.id+{}"},
        {"name": "Tokopedia", "url": "https://www.google.com/search?q=site:tokopedia.com+{}"},
        {"name": "Bukalapak", "url": "https://www.google.com/search?q=site:bukalapak.com+{}"},
        {"name": "Carousell", "url": "https://www.google.com/search?q=site:carousell.co.id+{}"}
    ],
    "Jejak Publik & Dokumen": [
        {"name": "Pencarian Universal", "url": "https://www.google.com/search?q=\"{}\""},
        {"name": "GetContact (Web Dork)", "url": "https://www.google.com/search?q=site:getcontact.com+{}"},
        {"name": "Scribd (Dokumen/Tugas)", "url": "https://www.google.com/search?q=site:scribd.com+{}"},
        {"name": "Blogspot / WordPress", "url": "https://www.google.com/search?q=site:blogspot.com+OR+site:wordpress.com+{}"}
    ]
}

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    query = ""
    query_type = ""
    wa_link = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        query_type = request.form.get("query_type", "name")

        if query:
            clean_query = urllib.parse.quote(query)

            # Fitur Khusus: Generate Link Direct WhatsApp jika input adalah nomor HP
            if query_type == "phone":
                phone_num = re.sub(r'\D', '', query) # Bersihkan karakter selain angka
                if phone_num.startswith('0'):
                    phone_num = '62' + phone_num[1:] # Konversi format 08 ke 628
                elif phone_num.startswith('+'):
                    phone_num = phone_num[1:]
                
                if phone_num:
                    wa_link = f"https://wa.me/{phone_num}"

            # Eksekusi pembuatan link pencarian berdasarkan kategori
            for category, platforms in PLATFORMS.items():
                results[category] = []
                for platform in platforms:
                    results[category].append({
                        "name": platform["name"],
                        "link": platform["url"].format(clean_query)
                    })

    return render_template("index.html", results=results, query=query, query_type=query_type, wa_link=wa_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
