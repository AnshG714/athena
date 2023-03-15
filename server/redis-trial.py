from redis import Redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, VectorField

from OpenAIRequestClient import OpenAIRequestClient
import asyncio
import numpy as np

redis_client = Redis(host="localhost", port=6379, password="")
VECTOR_DIM = 1536
VECTOR_NUMBER = 21
DISTANCE_METRIC = "COSINE"
INDEX_NAME = "history_embeddings"

text = open("./sample_text_history.txt", "r")
paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]

content = TextField(name="content")
content_embeddings = VectorField(
    "content_embeddings",
    "FLAT",
    {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": DISTANCE_METRIC,
        "INITIAL_CAP": VECTOR_NUMBER,
    },
)

fields = [content, content_embeddings]

try:
    redis_client.ft(INDEX_NAME).info()
    print("Index already exists")
except:
    # Create RediSearch Index
    redis_client.ft(INDEX_NAME).create_index(
        fields=fields,
        definition=IndexDefinition(index_type=IndexType.HASH),
    )

api = OpenAIRequestClient(endpoint="embeddings")


embeddings_tuple = []


async def get_embeddings_map():
    for p in paragraphs:
        embedding_response = await api.make_request(
            {"input": p, "model": "text-embedding-ada-002"}
        )
        if "data" not in embedding_response:
            print(embedding_response)
        embedding = embedding_response["data"][0]["embedding"]
        embeddings_tuple.append((p, embedding))


# asyncio.run(get_embeddings_map())
# index = 0
# for content, embedding in embeddings_tuple:
#     key = f"history_embeddings_{index}"
#     embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()

#     doc = {"content": content, "content_embeddings": embedding_bytes}
#     redis_client.hset(key, mapping=doc)
#     index += 1

print(
    f"Loaded {redis_client.info()['db0']['keys']} documents in Redis search index with name: {INDEX_NAME}"
)


async def search_redis(
    redis_client: Redis,
    user_query: str,
    index_name: str = "history_embeddings",
    vector_field="content_embeddings",
    return_fields=["content", "vector_score"],
    hybrid_fields="*",
    k: int = 3,
):
    query_embedding = (
        await api.make_request({"input": user_query, "model": "text-embedding-ada-002"})
    )["data"][0]["embedding"]

    base_query = f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector as vector_score]"
    query = (
        Query(base_query)
        .return_fields(*return_fields)
        .sort_by("vector_score")
        .paging(0, k)
        .dialect(2)
    )

    params_dict = {
        "vector": np.array(query_embedding).astype(dtype=np.float32).tobytes()
    }

    results = redis_client.ft(index_name).search(query, params_dict)
    for i, article in enumerate(results.docs):
        score = 1 - float(article.vector_score)
        print(f"{i}. {article.content} (Score: {round(score ,3) })")
        print("\n\n")


asyncio.run(search_redis(redis_client, "What was operation T4?"))
