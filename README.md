# Semantic-search-engine

Here's the semantic search engine. 
It's an engine that scrapes the 2 famous websites vsd.fr and public.fr to return to the user links associated with their search sentence.

How did i break the project: 

1. Data Preparation

Dataset Creation:
scrape articles from vsd.fr and public.fr.
metadata: title, URL, and publication date is included for search results.

Embedding Generation:
used pre-trained sentence-transformer model with OpenAI embeddings.
transformed each article into a semantic vector.

for Data Storage:
store article embeddings and metadata in a database (e.g., PostgreSQL, Elasticsearch, or any vector database like Pinecone or Weaviate).

2. Backend Development

queries Transformation:
converted user input into a semantic vector using the same model as above.

Similarity Search:
Use cosine similarity or a specialized vector search library (e.g., FAISS or Pinecone) to find the closest matches.

and result:
return relevant data title, link as "Read more".

3. Frontend Development

Search Interface:
created a very modern and minimalist UI with no animation.
allow users to input queries and display results dynamically.

and for result display:
show 5 article titles and links in an intuitive list.

!!!HOW TO RUN THE SEMANTIC SEARCH ENGINE LOCALLY!!!:
- open one terminal and run the server :python3 -m http.server 8000
- then run app.py

if any issues are encountered running teh server plz let me know !!!
