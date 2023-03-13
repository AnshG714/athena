import aiohttp
import asyncio
import os
from dotenv import load_dotenv


class OpenAIRequestClient:
    def __init__(self):
        load_dotenv()
        self.request_url = "https://api.openai.com/v1/chat/completions"

    def __get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }

    async def __make_request_impl(self, request_body, session):
        async with session.post(
            self.request_url, headers=self.__get_headers(), json=request_body
        ) as resp:
            return await resp.json()

    async def make_request(self, request_body):
        async with aiohttp.ClientSession() as session:
            return await self.__make_request_impl(request_body, session)

    async def make_concurrent_requests(self, request_bodies):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for request_body in request_bodies:
                tasks.append(
                    asyncio.ensure_future(
                        self.__make_request_impl(request_body, session)
                    )
                )

            responses = await asyncio.gather(*tasks)
            return responses


if __name__ == "__main__":
    request = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {
                "role": "assistant",
                "content": "The Los Angeles Dodgers won the World Series in 2020.",
            },
            {"role": "user", "content": "Where was it played?"},
        ],
    }

    request2 = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 3+3?"},
            {
                "role": "assistant",
                "content": "The answer is 6",
            },
            {"role": "user", "content": "Double it"},
        ],
    }

    api = OpenAIRequestClient()
    print(asyncio.run(api.make_concurrent_requests([request, request2])))
