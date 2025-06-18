import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

class ContentCreatorAgent:
    """
    This agent generates a full blog post using a chat-style prompt and the HuggingFace Router API with Mistral model.
    """

    def __init__(self):
        self.api_url = "https://router.huggingface.co/novita/v3/openai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}",
            "Content-Type": "application/json"
        }

    def build_prompt(self, topic: str, style: str, word_count: int) -> str:
        return (
            f"Write a {word_count}-word blog post in a {style} tone. "
            f"The topic is: {topic}.\n\n"
            f"Structure it with a short intro, a body with 2-3 paragraphs, and a conclusion.\n"
            f"Do not include the prompt in the blog post."
        )

    def call_model(self, prompt: str, word_count: int) -> str:
        payload = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": word_count * 2
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        with open("LangChain_workflow/outputs/content_creator.md", "w", encoding="utf-8") as f:
            f.write(response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]

# === LangChain-compatible tool === #

creator = ContentCreatorAgent()

@tool("generate_blog_post")
def generate_blog_post(topic: str, style: str = "informative", word_count: int = 300) -> str:
    """
    Generate a full blog post on a given topic with a specific tone and word count.
    """
    prompt = creator.build_prompt(topic, style, word_count)
    return creator.call_model(prompt, word_count)
