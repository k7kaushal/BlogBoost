import os
import requests
from dotenv import load_dotenv

load_dotenv()

class StyleAgent:
    '''
    This Agent creates content with different writing styles.
    It also add keywords for SEO optimization
    It generate SEO friendly metadata to be used by post agent.

    '''
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
        }

    def rewrite_in_style(self,  keyword_str, content, style: str = "conversational"):
        prompt = (
            f"Rewrite the following blog post in a {style} tone.\n"
            f"Keep the core message and structure the same.\n"
            f"Enhance the following blog post for SEO by naturally including these keywords: {keyword_str}. "
            f"Keep the tone and style intact. Return only the improved blog post:\n\n{content}"
            f"\nRewritten:"
        )

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.6,
                "max_new_tokens": len(content.split()) * 2
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()[0]["generated_text"]

    def generate_seo_metadata(self, content: str):
        prompt = (
            f"Generate an SEO-friendly blog title and meta description for the following content:\n\n{content}\n\n"
            f"Return in this format:\nTitle: ...\nMeta Description: ..."
        )

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.4,
                "max_new_tokens": 200
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()

        return response.json()[0]["generated_text"].strip()