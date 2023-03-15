from flask import Flask, request
from flask_cors import CORS
import asyncio
from redis import Redis

from summarizer import Summarizer
from timeline_extractor import TimelineExtractor
from embedding_manager import EmbeddingManager
from user_query_answerer import UserQueryAnswerer


app = Flask(__name__)
redis_client = Redis(host="localhost", port=6379, password="")
CORS(app)

# Pre-emptively create embedding managers for now. Need to change this up later.
embedding_manager_history = EmbeddingManager(redis_client, "history_embeddings")


@app.get("/")
def index():
    return "Hello!!"


@app.post("/api/v1/history/")
async def gen_history_content():
    body = request.json

    if not body:
        return {"error": "Missing request body"}, 400

    file_source = body.get("source", None)
    if not file_source:
        return {"error": "Missing file source"}, 400

    text = open("./sample_text_history.txt", "r")
    paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]

    summarizer = Summarizer()
    summarizer.load_text_from_file(f"./{file_source}")

    timeline_extractor = TimelineExtractor()
    timeline_extractor.load_text_from_file(f"./{file_source}")

    results = await asyncio.gather(
        *[
            summarizer.get_results(),
            timeline_extractor.get_results(),
            embedding_manager_history.load_embeddings(paragraphs),
        ]
    )

    summary = results[0]
    timeline = results[1]
    return {"summary": summary, "timeline": timeline}


@app.post("/api/v1/history/qa")
async def gen_query_response():
    body = request.json
    if not body:
        return {"error": "Missing request body"}, 400

    query = body.get("query", None)
    if not query:
        return {"error": "Missing user query"}, 400

    if not embedding_manager_history.is_index_initialized():
        return {"error": "Embeddings are not initialized"}, 500

    context = await embedding_manager_history.search_redis(query)
    context += f"\nQuestion: {query}"
    user_query_answerer = UserQueryAnswerer()
    user_query_answerer.set_context(context)

    answer = await user_query_answerer.get_results()
    return {"answer": answer}
