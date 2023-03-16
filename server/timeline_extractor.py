"""
Used for extracting timelines from a history context. 
"""
import prompts
import asyncio
import json
from BaseProcessor import BaseProcessor


class TimelineExtractor(BaseProcessor):
    def __init__(self, max_chunk_tokens=2000):
        super().__init__(max_chunk_tokens=max_chunk_tokens)

    def prompt(self):
        return prompts.GENERATE_TIMELINE

    def process_results(self, results):
        timeline = []
        for response in results:
            json_str = response["choices"][0]["message"]["content"]
            timeline += json.loads(json_str)

        return timeline


if __name__ == "__main__":
    timeline_generator = TimelineExtractor()
    timeline_generator.load_text_from_file("./sample_text_chemistry.txt")
    print(asyncio.run(timeline_generator.get_results()))
