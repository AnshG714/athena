from OpenAIRequestClient import OpenAIRequestClient
from redis import Redis
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, VectorField
import numpy as np


class EmbeddingManager:
    def __init__(self, redis_client: Redis, index_name: str):
        self.redis_client = redis_client
        self.request_client = OpenAIRequestClient(endpoint="embeddings")
        self.index_name = index_name
        self.vector_dims = 1536
        self.distance_metric = "COSINE"

    def is_index_initialized(self):
        try:
            self.redis_client.ft(self.index_name).info()
            print("This index already exists")
            return True
        except:
            return False

    def __initialize_redis_index(self, number_of_vectors):
        content = TextField(name="content")
        content_embeddings = VectorField(
            "content_embeddings",
            "FLAT",
            {
                "TYPE": "FLOAT32",
                "DIM": self.vector_dims,
                "DISTANCE_METRIC": self.distance_metric,
                "INITIAL_CAP": number_of_vectors,
            },
        )

        fields = [content, content_embeddings]

        if not self.is_index_initialized():
            # Create RediSearch Index
            self.redis_client.ft(self.index_name).create_index(
                fields=fields,
                definition=IndexDefinition(index_type=IndexType.HASH),
            )
            print("Created new index.")

    async def load_embeddings(self, paragraphs):
        number_of_vectors = len(paragraphs)
        self.__initialize_redis_index(number_of_vectors)

        batch_requests = [
            {"input": p, "model": "text-embedding-ada-002"} for p in paragraphs
        ]
        responses = await self.request_client.make_concurrent_requests(batch_requests)
        index = 0
        for index, (p, embedding_response) in enumerate(zip(paragraphs, responses)):
            if "data" not in embedding_response:
                raise Exception("failure while getting embeddings")

            embedding = embedding_response["data"][0]["embedding"]
            key = f"{self.index_name}_{index}"
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            doc = {"content": p, "content_embeddings": embedding_bytes}
            self.redis_client.hset(key, mapping=doc)

    async def search_redis(
        self,
        user_query,
        vector_field="content_embeddings",
        return_fields=["content", "vector_score"],
        hybrid_fields="*",
        k: int = 3,
    ):
        if not self.is_index_initialized():
            raise Exception("Can't call search without inititalizing indices first!")

        query_embedding = (
            await self.request_client.make_request(
                {"input": user_query, "model": "text-embedding-ada-002"}
            )
        )["data"][0]["embedding"]

        base_query = (
            f"{hybrid_fields}=>[KNN {k} @{vector_field} $vector as vector_score]"
        )

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

        results = self.redis_client.ft(self.index_name).search(query, params_dict)
        ret_list = [res.content for res in results.docs]
        return "\n\n".join(ret_list)


if __name__ == "__main__":
    import asyncio

    redis = redis_client = Redis(host="localhost", port=6379, password="")
    embedding_manager = EmbeddingManager(redis, "history_embeddings")
    text = open("./sample_text_history.txt", "r")
    paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]

    async def main():
        await embedding_manager.load_embeddings(paragraphs)
        print(await embedding_manager.search_redis("What was the T4 program about?"))

    asyncio.run(main())
