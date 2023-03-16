"""
Used for extracting timelines from a history context. 
"""
import prompts
import asyncio
import json
from BaseProcessor import BaseProcessor


class KeyMoleculeExtractor(BaseProcessor):
    def __init__(self, max_chunk_tokens=1500):
        super().__init__(max_chunk_tokens=max_chunk_tokens, endpoint="completions")

    def prompt(self):
        return prompts.EXTRACT_MOLECULES_2

    def process_results(self, results):
        molecules = []
        for response in results:
            json_str = response["choices"][0]["text"]
            try:
                molecules += json.loads(json_str)
            except Exception as e:
                print(e)
                print(response)

        return molecules


if __name__ == "__main__":
    key_molecule_extractor = KeyMoleculeExtractor()
    key_molecule_extractor.load_text_from_file("./sample_text_chemistry.txt")
    print(asyncio.run(key_molecule_extractor.get_results()))
