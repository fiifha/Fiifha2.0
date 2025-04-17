from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            results = perform_search(query)
    return render_template('index.html', results=results, query=query)

def perform_search(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.bing.com/search?q={query}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select('.b_algo'):
        title = item.select_one('h2')
        link = title.find('a')['href'] if title and title.find('a') else ''
        snippet = item.select_one('.b_caption p')
        snippet_text = snippet.text if snippet else ''
        if title:
            results.append({
                'title': title.text,
                'link': link,
                'snippet': snippet_text
            })
    return results

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
