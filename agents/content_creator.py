import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ContentCreatorAgent:
    def __init__(self):
        self.api_url = "https://router.huggingface.co/novita/v3/openai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.model_id = "mistralai/mistral-7b-instruct"

    def generate_blog_post(self, topic: str, style: str = "informative", word_count: int = 300) -> str:
        prompt = self._build_prompt(topic, style, word_count)
        print("Generating blog post...")

        payload = {
            "model": self.model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": word_count * 2
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    def _build_prompt(self, topic: str, style: str, word_count: int) -> str:
        print("Building prompt...")
        return (
            f"Write a {word_count}-word blog post in a {style} tone. "
            f"The topic is: {topic}.\n\n"
            f"Structure it with a short intro, a body with 2-3 paragraphs, and a conclusion.\n"
            f"Do not include the prompt in the blog post."
        )
