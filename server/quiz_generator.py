import prompts
from BaseProcessor import BaseProcessor
import asyncio
import json


class QuizGenerator(BaseProcessor):
    def __init__(self, max_chunk_tokens=1500):
        super().__init__(max_chunk_tokens=max_chunk_tokens, endpoint="completions")

    def prompt(self):
        return prompts.QUIZ

    def process_results(self, results):
        contents = []
        for response in results:
            try:
                contents += json.loads(response["choices"][0]["text"])
            except Exception as e:
                print(e)
                print("response: ", response)

        return contents


if __name__ == "__main__":
    quiz_generator = QuizGenerator()
    quiz_generator.load_text_from_file("./sample_text_chemistry.txt")
    print(asyncio.run(quiz_generator.get_results()))
