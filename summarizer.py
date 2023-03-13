"""
Class that summarizes a large body of text. It does this by loading a large body of text 
over the CDN, and then breaks it up into 'decently' sized chunks that can be encoded by ChatGPT,
and then combining those summaries together.
"""
import tiktoken
import prompts
from OpenAIRequestClient import OpenAIRequestClient
import asyncio


class Summarizer:
    def __init__(self, max_encoding_length=2000):
        self.max_encoding_length = max_encoding_length
        self.token_encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
        self.request_client = OpenAIRequestClient()

    def load_text_from_file(self, file_name):
        """
        Loads the contents of ${file_name} in-memory (assuming this is small enough to load into memory).
        The paragraphs are determined by \n\n delimiters.
        """
        text = open(file_name, "r")
        paragraphs = [r.replace("\n", " ") for r in text.read().split("\n\n")]
        self.paragraphs = paragraphs

    async def summarize(self):
        if not self.paragraphs:
            raise Exception("No paragraphs to summarize!")

        contexts = self.__group_paragraphs()
        requests = []
        for context in contexts:
            requests.append(
                {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": prompts.SUMMARIZE,
                        },
                        {"role": "user", "content": context},
                    ],
                }
            )

        responses = await self.request_client.make_concurrent_requests(requests)
        contents = []
        for response in responses:
            contents.append(response["choices"][0]["message"]["content"])

        complete_summary = "\n\n".join(contents)
        return complete_summary

    def __group_paragraphs(self):
        """
        Groups the paragraphs so they can be formed as context for the summary. We want
        to pass as much information as possible.
        """
        groups = [[]]
        current_group = groups[0]
        current_group_tokens = 0
        for paragraph in self.paragraphs:
            # get encoding length
            encodings = self.token_encoder.encode(paragraph)
            num_tokens = len(encodings)
            if num_tokens + current_group_tokens <= self.max_encoding_length:
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


if __name__ == "__main__":
    summarizer = Summarizer()
    summarizer.load_text_from_file("./sample_text_history.txt")
    asyncio.run(summarizer.summarize())
