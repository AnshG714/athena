"""
Base functionality for different extractors and processors.
"""
from OpenAIRequestClient import OpenAIRequestClient
import tiktoken


class BaseProcessor:
    def __init__(self, max_chunk_tokens=2000):
        """
        Initializes the base processor instance.
        ### Params
        - max_chunk_tokens. Represents the maximum number of tokens in a chunk that will be
        sent to the LLM for batch processing. Defaults to 2000.
        """
        self.max_chunk_tokens = max_chunk_tokens
        self.token_encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.request_client = OpenAIRequestClient()

    def load_text_from_file(self, file_name):
        """
        Loads the contents `file_name` in-memory (assuming this is small enough to load into memory).
        The paragraphs are determined by \n\n delimiters.

        ### Params
        - file_name: The path of the file to load.
        """
        text = open(file_name, "r")
        paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]
        self.__contexts = self.__group_paragraphs(paragraphs)

    def prompt(self):
        raise NotImplementedError("Please implement prompt")

    def process_results(self, results):
        raise NotImplementedError("Please implement process_results")

    async def get_results(self):
        if not self.__contexts:
            raise Exception("No paragraphs to summarize!")

        requests = []
        for context in self.__contexts:
            requests.append(
                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": self.prompt(),
                        },
                        {"role": "user", "content": context},
                    ],
                }
            )

        raw_results = await self.request_client.make_concurrent_requests(requests)
        return self.process_results(raw_results)

    def __group_paragraphs(self, paragraphs):
        """
        Groups the paragraphs so they can be formed as context for the summary. We want
        to pass as much information as possible.
        """
        groups = [[]]
        current_group = groups[0]
        current_group_tokens = 0
        for paragraph in paragraphs:
            # get encoding length
            encodings = self.token_encoder.encode(paragraph)
            num_tokens = len(encodings)
            if num_tokens + current_group_tokens <= self.max_chunk_tokens:
                current_group.append(paragraph)
                current_group_tokens += num_tokens
            else:
                groups.append([])
                current_group = groups[-1]
                current_group.append(paragraph)
                current_group_tokens = num_tokens

        contexts = []
        for group in groups:
            contexts.append(" ".join(group))

        return contexts
