from flask import Flask, render_template, request
import urllib.parse
import re

app = Flask(__name__)

# Database Platform dengan URL Google (Domain) dan URL Direct (Langsung ke Platform)
PLATFORMS = {
    "Media Sosial Utama": [
        {"name": "Facebook", "domain": "facebook.com", "direct": "https://www.facebook.com/search/top/?q={}"},
        {"name": "Instagram", "domain": "instagram.com", "direct": "https://www.instagram.com/{username}"},
        {"name": "TikTok", "domain": "tiktok.com", "direct": "https://www.tiktok.com/search/user?q={}"},
        {"name": "Threads", "domain": "threads.net", "direct": "https://www.threads.net/@{username}"},
        {"name": "Twitter / X", "domain": "twitter.com", "direct": "https://x.com/search?q={}&src=typed_query"},
        {"name": "Pinterest", "domain": "pinterest.com", "direct": "https://www.pinterest.com/search/users/?q={}"},
        {"name": "YouTube", "domain": "youtube.com", "direct": "https://www.youtube.com/results?search_query={}"}
    ],
    "Forum & Komunitas": [
        {"name": "Kaskus", "domain": "kaskus.co.id", "direct": "https://www.kaskus.co.id/search?q={}"},
        {"name": "Reddit", "domain": "reddit.com", "direct": "https://www.reddit.com/search/?q={}"},
        {"name": "Medium", "domain": "medium.com", "direct": "https://medium.com/search?q={}"},
        {"name": "GitHub (IT)", "domain": "github.com", "direct": "https://github.com/search?q={}&type=users"}
    ],
    "Jejak Karir & Profesional": [
        {"name": "LinkedIn", "domain": "linkedin.com/in", "direct": "https://www.linkedin.com/search/results/all/?keywords={}"},
        {"name": "JobStreet", "domain": "jobstreet.co.id", "direct": "https://www.jobstreet.co.id/id/job-search/{}-jobs/"},
        {"name": "Glints", "domain": "glints.com/id", "direct": "https://glints.com/id/opportunities/jobs/explore?keyword={}"},
        {"name": "Fastwork (Freelance)", "domain": "fastwork.id", "direct": "https://fastwork.id/search?q={}"},
        {"name": "Sribulancer", "domain": "sribulancer.com", "direct": "https://www.sribulancer.com/id/freelancers?q={}"}
    ],
    "Marketplace & Transaksi": [
        {"name": "Shopee", "domain": "shopee.co.id", "direct": "https://shopee.co.id/search?keyword={}"},
        {"name": "Tokopedia", "domain": "tokopedia.com", "direct": "https://www.tokopedia.com/search?q={}"},
        {"name": "Bukalapak", "domain": "bukalapak.com", "direct": "https://www.bukalapak.com/products?search%5Bkeywords%5D={}"},
        {"name": "Blibli", "domain": "blibli.com", "direct": "https://www.blibli.com/cari/{}"},
        {"name": "Carousell", "domain": "carousell.co.id", "direct": "https://www.carousell.co.id/search/{}?addRecent=true"},
        {"name": "OLX Indonesia", "domain": "olx.co.id", "direct": "https://www.olx.co.id/items/q-{}"},
        {"name": "Lazada", "domain": "lazada.co.id", "direct": "https://www.lazada.co.id/catalog/?q={}"}
    ],
    "Kreator & Donasi (Identitas)": [
        {"name": "Trakteer", "domain": "trakteer.id", "direct": "https://trakteer.id/{username}"},
        {"name": "Saweria", "domain": "saweria.co", "direct": "https://saweria.co/{username}"},
        {"name": "Sociabuzz", "domain": "sociabuzz.com", "direct": "https://sociabuzz.com/{username}"}
    ],
    "Jejak Publik & Hukum": [
        {"name": "Putusan Mahkamah Agung", "domain": "putusan3.mahkamahagung.go.id", "direct": "https://putusan3.mahkamahagung.go.id/search.html?q={}"},
        {"name": "Scribd (Dokumen)", "domain": "scribd.com", "direct": "https://www.scribd.com/search?query={}"},
        {"name": "Blogspot / WordPress", "domain": "blogspot.com OR site:wordpress.com", "direct": "https://www.google.com/search?q=site:blogspot.com+OR+site:wordpress.com+{}"},
        {"name": "GetContact", "domain": "getcontact.com", "direct": "https://www.getcontact.com/en/search"}
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
            # Menghapus spasi dan mengubah ke huruf kecil untuk URL tipe username (seperti Instagram/Threads)
            username_query = query.lower().replace(" ", "")

            if query_type == "phone":
                phone_num = re.sub(r'\D', '', query)
                if phone_num.startswith('0'):
                    phone_num = '62' + phone_num[1:]
                elif phone_num.startswith('+'):
                    phone_num = phone_num[1:]
                if phone_num:
                    wa_link = f"https://wa.me/{phone_num}"

            for category, platforms in PLATFORMS.items():
                results[category] = []
                for platform in platforms:
                    # 1. Bikin Link Via Google Dork (Selalu Dibuat)
                    dork_query = f'site:{platform["domain"]} "{query}" OR {query}'
                    params = {'q': dork_query}
                    google_search_url = "https://www.google.com/search?" + urllib.parse.urlencode(params)
                    
                    # 2. Bikin Link Direct Platform
                    direct_url = platform.get("direct", "")
                    if "{username}" in direct_url:
                        direct_url = direct_url.format(username=username_query)
                    elif "{}" in direct_url:
                        direct_url = direct_url.format(clean_query)

                    results[category].append({
                        "name": platform["name"],
                        "link_google": google_search_url,
                        "link_direct": direct_url
                    })

            # Tambahkan Pencarian Universal ke kategori Jejak Publik
            universal_dork = f'"{query}" OR {query}'
            results["Jejak Publik & Hukum"].insert(0, {
                "name": "Universal (Seluruh Internet)",
                "link_google": "https://www.google.com/search?" + urllib.parse.urlencode({'q': universal_dork}),
                "link_direct": ""
            })

    return render_template("index.html", results=results, query=query, query_type=query_type, wa_link=wa_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
