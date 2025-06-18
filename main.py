import requests
from agents.content_creator import ContentCreatorAgent
from agents.style_agent import StyleAgent
from agents.post_agent.base import BlogPost
from agents.post_agent.medium import MediumPoster
from agents.post_agent.devto import DevtoPoster
import asyncio

if __name__ == "__main__":
    creator = ContentCreatorAgent()
    raw_post = creator.generate_blog_post(
        topic="Benefits of a bamboo-made gym towel",
        style="conversational",
        word_count=350
    )
    print(raw_post)

    # styles = ["conversational", "storytelling", "inspirational", "professional", "casual and friendly", "for fitness enthusiasts", "like a Reddit post"]
    # keyword_str = ["bamboo towel", "eco-friendly gym gear", "sustainable fitness"]
    # style_agent = StyleAgent()
    # styled_post = style_agent.rewrite_in_style(
    #     keyword_str, 
    #     raw_post, 
    #     style="storytelling"
    # )
    # print("Styled Blog Post:\n", styled_post)
    
    # meta_data = style_agent.generate_seo_metadata(styled_post)
    # print("\n\n meta data: ", meta_data)

    # post = BlogPost(
    # title="Gym Towels That Change the Game",
    # content= f"<p>{styled_post}</p>",
    # tags=["fitness", "eco", "bamboo"]
    
    # )

    # Post to Dev.to
    # asyncio.run(DevtoPoster.post_to_devto())
    # devto = DevtoPoster(api_key="your_devto_api_key")
    # dev_url = devto.post(post)

    # Use that URL for Medium's RSS mirror
    # if dev_url:
    #     post.canonical_url = dev_url
    #     medium = MediumPoster()
    #     medium.post(post)


