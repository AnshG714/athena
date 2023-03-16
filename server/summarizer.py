import prompts
from BaseProcessor import BaseProcessor
import asyncio


class Summarizer(BaseProcessor):
    def __init__(self, max_chunk_tokens=2000):
        super().__init__(max_chunk_tokens=max_chunk_tokens, endpoint="completions")

    def prompt(self):
        return prompts.SUMMARIZE

    def process_results(self, results):
        contents = []
        for response in results:
            try:
                contents.append(response["choices"][0]["text"])
            except Exception as e:
                print(e)
                print("response: ", response)

        complete_summary = "\n\n".join(contents)
        return complete_summary


if __name__ == "__main__":
    summarizer = Summarizer()
    summarizer.load_text_from_file("./sample_text_chemistry.txt")
    print(asyncio.run(summarizer.get_results()))
