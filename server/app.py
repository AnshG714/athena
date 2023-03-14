from flask import Flask, request
from flask_cors import CORS
from summarizer import Summarizer
from timeline_extractor import TimelineExtractor
import asyncio

app = Flask(__name__)
CORS(app)


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

    summarizer = Summarizer()
    summarizer.load_text_from_file(f"./{file_source}")

    timeline_extractor = TimelineExtractor()
    timeline_extractor.load_text_from_file(f"./{file_source}")

    results = await asyncio.gather(
        *[summarizer.get_results(), timeline_extractor.get_results()]
    )

    summary = results[0]
    timeline = results[1]
    return {"summary": summary, "timeline": timeline}
