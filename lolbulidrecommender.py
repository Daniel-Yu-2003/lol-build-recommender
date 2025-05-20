from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_build(champion):
    url = f"https://www.metasrc.com/lol/build/{champion.lower()}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract info
    infos = []
    for info in soup.select('.white-text-underline'):
        infos.append(info.text)

    return {
        "champion": champion,
        "items": infos[:6],
        "runes": infos[6:9],
        "sums": infos[9:11]
    }

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        champion = request.form.get("champion")
        build = get_build(champion)
        return render_template("output.html", build=build)
    return render_template("index.html")

if __name__ == "__main__":
    app.run()