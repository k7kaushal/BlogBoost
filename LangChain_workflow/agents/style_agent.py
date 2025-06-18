import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

class StyleAgent:
    """
    This agent rewrites blog posts in a given style and generates SEO metadata using Hugging Face chat models.
    """

    def __init__(self):
        self.api_url = "https://router.huggingface.co/novita/v3/openai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        self.model = "mistralai/mistral-7b-instruct"

    def _call_model(self, user_prompt: str, max_tokens: int = 700, temperature: float = 0.6) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        with open("LangChain_workflow/outputs/styler.md", "w", encoding="utf-8") as f:
            f.write(response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"].strip()

# === LangChain-compatible tools === #

agent = StyleAgent()

@tool("rewrite_in_style")
def rewrite_in_style(keyword_str: str, content: str, style: str = "conversational") -> str:
    """
    Rewrite a blog post in a specified tone and include the given SEO keywords.
    """
    prompt = (
        f"Rewrite the following blog post in a {style} tone.\n"
        f"Retain the core message and structure.\n"
        f"Naturally include these keywords for SEO: {keyword_str}.\n\n"
        f"Content:\n{content}\n\nRewritten:"
    )
    return agent._call_model(prompt, max_tokens=len(content.split()) * 2, temperature=0.6)


@tool("generate_seo_metadata")
def generate_seo_metadata(content: str) -> str:
    """
    Generate an SEO-friendly title and meta description for a blog post.
    """
    prompt = (
        f"Generate an SEO-friendly blog title and meta description for the following blog post.\n"
        f"Return in this format:\nTitle: ...\nMeta Description: ...\n\nContent:\n{content}"
    )
    return agent._call_model(prompt, max_tokens=700, temperature=0.4)
