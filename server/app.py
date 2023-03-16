from flask import Flask, request
from flask_cors import CORS
import asyncio
from redis import Redis

from summarizer import Summarizer
from timeline_extractor import TimelineExtractor
from embedding_manager import EmbeddingManager
from user_query_answerer import UserQueryAnswerer
from key_molecule_extractor import KeyMoleculeExtractor
from quiz_generator import QuizGenerator

app = Flask(__name__)
redis_client = Redis(host="localhost", port=6379, password="")
CORS(app)

# Pre-emptively create embedding managers for now. Need to change this up later.
embedding_manager_history = EmbeddingManager(redis_client, "history_embeddings")
embedding_manager_chemistry = EmbeddingManager(redis_client, "chemistry_embeddings")


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

    text = open(f"./{file_source}", "r")
    paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]

    summarizer = Summarizer()
    summarizer.set_paragraphs(paragraphs)

    timeline_extractor = TimelineExtractor()
    timeline_extractor.set_paragraphs(paragraphs)

    quiz_generator = QuizGenerator()
    quiz_generator.set_paragraphs(paragraphs)

    results = await asyncio.gather(
        *[
            summarizer.get_results(),
            timeline_extractor.get_results(),
            quiz_generator.get_results(),
            embedding_manager_history.load_embeddings(paragraphs),
        ]
    )

    summary = results[0]
    timeline = results[1]
    quiz = results[2]
    return {"summary": summary, "timeline": timeline, "quiz": quiz}


@app.post("/api/v1/<string:subject>/qa")
async def gen_query_response(subject):
    body = request.json
    if not body:
        return {"error": "Missing request body"}, 400

    query = body.get("query", None)
    if not query:
        return {"error": "Missing user query"}, 400

    if subject == "history":
        embedding_manager = embedding_manager_history
    elif subject == "chemistry":
        embedding_manager = embedding_manager_chemistry
    else:
        return {"error": "Unsupported subject"}, 400

    if not embedding_manager.is_index_initialized():
        return {"error": "Embeddings are not initialized"}, 500

    context = await embedding_manager.search_redis(query)
    context += f"\nQuestion: {query}"
    user_query_answerer = UserQueryAnswerer()
    user_query_answerer.set_context(context)

    answer = await user_query_answerer.get_results()
    return {"answer": answer}


@app.post("/api/v1/chemistry/")
async def gen_chemistry_content():
    body = request.json

    if not body:
        return {"error": "Missing request body"}, 400

    file_source = body.get("source", None)
    if not file_source:
        return {"error": "Missing file source"}, 400

    text = open(f"./{file_source}", "r")
    paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]

    summarizer = Summarizer()
    summarizer.set_paragraphs(paragraphs)

    key_molecule_extractor = KeyMoleculeExtractor()
    key_molecule_extractor.set_paragraphs(paragraphs)

    quiz_generator = QuizGenerator()
    quiz_generator.set_paragraphs(paragraphs)

    results = await asyncio.gather(
        *[
            summarizer.get_results(),
            key_molecule_extractor.get_results(),
            quiz_generator.get_results(),
            embedding_manager_chemistry.load_embeddings(paragraphs),
        ]
    )

    summary = results[0]
    timeline = results[1]
    quiz = results[2]

    return {"summary": summary, "molecules": timeline, "quiz": quiz}
