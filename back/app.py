import requests
from bs4 import BeautifulSoup, NavigableString
from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm
from urllib.parse import urljoin
from unidecode import unidecode
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import json





model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}

BASE_URLS = {
    "public": "https://public.fr",
    "vsd": "https://vsd.fr"
}

def generate_slug(title):
    title = unidecode(title)
    title = re.sub(r"[^\w\s-]", "", title) 
    slug = "-".join(title.lower().split())
    return slug

def extract_text_from_url(url):
    try: 
        response = requests.get(url, headers=HEADERS)
        time.sleep(5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content_list = []

        title = soup.title.string if soup.title else "no title found"
        if title:
  
            slug = generate_slug(title)
            full_url = urljoin(url, slug)
            content_list.append({"type": "Title", "text": title, "url": full_url})

        for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
            if isinstance(element, NavigableString):
                continue
            text = element.text.strip()
            if element.name in ['h1', 'h2', 'h3'] and len(text) > 10:
                slug = generate_slug(text)
                full_url = urljoin(url, slug)
                content_list.append({"type": element.name.upper(), "text": text, "url": full_url})
            elif element.name == 'p' and len(text) > 10:
                content_list.append({"type": "Paragraph", "text": text, "url": url})

        return content_list
    except Exception as e:
        print(f"error fetching {url}: {e}")
        return []

def generate_embeddings_and_query(all_content, query):
    print("generating embeddings for the extracted content...")

    texts = [item['text'] for item in all_content]
    embeddings = model.encode(texts)

    query_embedding = model.encode([query])[0]

    similarities = []
    for i, embedding in enumerate(embeddings):
        similarity = dot(query_embedding, embedding) / (norm(query_embedding) * norm(embedding))
        similarities.append((similarity, all_content[i]))

    similarities = sorted(similarities, key=lambda x: x[0], reverse=True)

    return similarities[:5]


def save_to_file(content_list, filename="content_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(content_list, file, ensure_ascii=False, indent=4)


def load_from_file(filename="content_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "backend is running.", 200


@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "query is required"}), 400

   
    all_content = load_from_file()
    if not all_content:
       
        for site, url in BASE_URLS.items():
            print(f"Scraping {url}...")
            content = extract_text_from_url(url)
            if content:
                all_content.extend(content)
        save_to_file(all_content)

    if not all_content:
        return jsonify({"error": "no articles found"}), 500

  
    query_embedding = model.encode([query])[0]
    similarities = []


    for content in all_content:
        content_text = content["text"]
        content_embedding = model.encode([content_text])[0]
        similarity = dot(query_embedding, content_embedding) / (norm(query_embedding) * norm(content_embedding))
        similarities.append({
            "type": content["type"],
            "text": content["text"],
            "url": content["url"],
            "similarity": float(similarity)
        })

    similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)
    return jsonify(similarities[:5])

if __name__ == '__main__':
    app.run(debug=True)
