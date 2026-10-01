from flask import Flask, render_template, request
import urllib.parse
import re

app = Flask(__name__)

# Mengubah struktur database menjadi domain saja agar URL bisa dirakit otomatis dan lebih bersih
PLATFORMS = {
    "Media Sosial Utama": [
        {"name": "Facebook", "domain": "facebook.com"},
        {"name": "Instagram", "domain": "instagram.com"},
        {"name": "TikTok", "domain": "tiktok.com"},
        {"name": "Twitter / X", "domain": "twitter.com"},
        {"name": "Pinterest", "domain": "pinterest.com"},
        {"name": "YouTube", "domain": "youtube.com"}
    ],
    "Jejak Karir & Profesional": [
        {"name": "LinkedIn", "domain": "linkedin.com/in"},
        {"name": "JobStreet", "domain": "jobstreet.co.id"},
        {"name": "Glints", "domain": "glints.com/id"}
    ],
    "Marketplace & Transaksi": [
        {"name": "Shopee", "domain": "shopee.co.id"},
        {"name": "Tokopedia", "domain": "tokopedia.com"},
        {"name": "Bukalapak", "domain": "bukalapak.com"},
        {"name": "Carousell", "domain": "carousell.co.id"}
    ],
    "Jejak Publik & Dokumen": [
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
            # Fitur Nomor WhatsApp
            if query_type == "phone":
                phone_num = re.sub(r'\D', '', query)
                if phone_num.startswith('0'):
                    phone_num = '62' + phone_num[1:]
                elif phone_num.startswith('+'):
                    phone_num = phone_num[1:]
                
                if phone_num:
                    wa_link = f"https://wa.me/{phone_num}"

            # Generate Link Pencarian Google Dork yang lebih fleksibel
            for category, platforms in PLATFORMS.items():
                results[category] = []
                for platform in platforms:
                    # Rumus Dork: site:domain.com "nama lengkap" OR nama lengkap
                    # Ini menyuruh Google: "Cari yang urutannya sama persis, JIKA TIDAK ADA, cari yang kata-katanya ada di halaman itu"
                    dork_query = f'site:{platform["domain"]} "{query}" OR {query}'
                    
                    # URL Encode yang standar agar karakter seperti spasi, titik, atau kutip tidak merusak link Google
                    params = {'q': dork_query}
                    google_search_url = "https://www.google.com/search?" + urllib.parse.urlencode(params)
                    
                    results[category].append({
                        "name": platform["name"],
                        "link": google_search_url
                    })

            # Menambahkan fitur Pencarian Universal (Bebas di seluruh internet)
            universal_dork = f'"{query}" OR {query}'
            results["Jejak Publik & Dokumen"].insert(0, {
                "name": "Pencarian Universal Internet",
                "link": "https://www.google.com/search?" + urllib.parse.urlencode({'q': universal_dork})
            })

    return render_template("index.html", results=results, query=query, query_type=query_type, wa_link=wa_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
