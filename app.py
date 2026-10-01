from flask import Flask, render_template, request
import urllib.parse
import re

app = Flask(__name__)

# Database Platform Komprehensif untuk Desk Collection / OSINT
PLATFORMS = {
    "Media Sosial Utama": [
        {"name": "Facebook", "domain": "facebook.com"},
        {"name": "Instagram", "domain": "instagram.com"},
        {"name": "TikTok", "domain": "tiktok.com"},
        {"name": "Threads", "domain": "threads.net"},
        {"name": "Twitter / X", "domain": "twitter.com"},
        {"name": "Pinterest", "domain": "pinterest.com"},
        {"name": "YouTube", "domain": "youtube.com"}
    ],
    "Forum & Komunitas": [
        {"name": "Kaskus", "domain": "kaskus.co.id"},
        {"name": "Reddit", "domain": "reddit.com"},
        {"name": "Medium", "domain": "medium.com"},
        {"name": "GitHub (IT/Tech)", "domain": "github.com"}
    ],
    "Jejak Karir & Profesional": [
        {"name": "LinkedIn", "domain": "linkedin.com/in"},
        {"name": "JobStreet", "domain": "jobstreet.co.id"},
        {"name": "Glints", "domain": "glints.com/id"},
        {"name": "Fastwork (Freelance)", "domain": "fastwork.id"},
        {"name": "Sribulancer", "domain": "sribulancer.com"}
    ],
    "Marketplace & Transaksi": [
        {"name": "Shopee", "domain": "shopee.co.id"},
        {"name": "Tokopedia", "domain": "tokopedia.com"},
        {"name": "Bukalapak", "domain": "bukalapak.com"},
        {"name": "Carousell (Barang Bekas)", "domain": "carousell.co.id"},
        {"name": "OLX Indonesia", "domain": "olx.co.id"},
        {"name": "Lazada", "domain": "lazada.co.id"},
        {"name": "Blibli", "domain": "blibli.com"}
    ],
    "Kreator & Donasi (Sering Bocor Identitas)": [
        {"name": "Trakteer", "domain": "trakteer.id"},
        {"name": "Saweria", "domain": "saweria.co"},
        {"name": "Sociabuzz", "domain": "sociabuzz.com"}
    ],
    "Jejak Publik, Dokumen & Hukum": [
        {"name": "Putusan Mahkamah Agung (Kasus Hukum)", "domain": "putusan3.mahkamahagung.go.id"},
        {"name": "Scribd (Dokumen/Tugas)", "domain": "scribd.com"},
        {"name": "Blogspot / WordPress", "domain": "blogspot.com OR site:wordpress.com"},
        {"name": "GetContact (Web)", "domain": "getcontact.com"}
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
            # Fitur Link Langsung WhatsApp
            if query_type == "phone":
                phone_num = re.sub(r'\D', '', query)
                if phone_num.startswith('0'):
                    phone_num = '62' + phone_num[1:]
                elif phone_num.startswith('+'):
                    phone_num = phone_num[1:]
                
                if phone_num:
                    wa_link = f"https://wa.me/{phone_num}"

            # Generate Link Pencarian Google Dork Cerdas
            for category, platforms in PLATFORMS.items():
                results[category] = []
                for platform in platforms:
                    # Rumus Dork: site:domain.com "query" OR query
                    dork_query = f'site:{platform["domain"]} "{query}" OR {query}'
                    
                    params = {'q': dork_query}
                    google_search_url = "https://www.google.com/search?" + urllib.parse.urlencode(params)
                    
                    results[category].append({
                        "name": platform["name"],
                        "link": google_search_url
                    })

            # Fitur Pencarian Bebas (Universal) ditambahkan di urutan pertama pada Jejak Publik
            universal_dork = f'"{query}" OR {query}'
            results["Jejak Publik, Dokumen & Hukum"].insert(0, {
                "name": "Pencarian Universal (Seluruh Internet)",
                "link": "https://www.google.com/search?" + urllib.parse.urlencode({'q': universal_dork})
            })

    return render_template("index.html", results=results, query=query, query_type=query_type, wa_link=wa_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
