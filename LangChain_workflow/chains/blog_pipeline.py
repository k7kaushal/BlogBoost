from langchain_core.runnables import RunnableLambda
from agents.content_creator import generate_blog_post
from agents.style_agent import rewrite_in_style, generate_seo_metadata
from agents.post_agent import post_to_devto
from agents.base import BlogPost

# Initialize agents
# creator = ContentCreatorAgent()
# styler = StyleAgent()
# poster = PostAgent()

def generate_content_from_topic(inputs):
    topic = inputs["topic"]
    style = inputs.get("style", "informative")
    word_count = inputs.get("word_count", 300)

    content = generate_blog_post.invoke({
    "topic": topic,
    "style": style,
    "word_count": word_count
})

    return {**inputs, "generated_content": content}

def rewrite_content_with_style(inputs):
    styled = rewrite_in_style.invoke({
        "content": inputs["generated_content"],
        "keyword_str": inputs.get("keywords", ""),
        "style": inputs.get("target_style", "conversational")
    })

    return {**inputs, "styled_content": styled}

def add_metadata(inputs):
    metadata = generate_seo_metadata.invoke({
        "content": inputs["styled_content"]
    })

    title_line = [line for line in metadata.splitlines() if line.startswith("Title:")]
    title = title_line[0].replace("Title:", "").strip() if title_line else "AI Blog"

    return {**inputs, "final_title": title}

async def post(inputs):
    blog = BlogPost(
        title=inputs["final_title"],
        content=inputs["styled_content"],
        tags=inputs.get("tags", ["ai", "automation", "buildinpublic"])
    )
    result = await post_to_devto.ainvoke({"post": blog})
    return result

# === Blog Generation Pipeline === #
pipeline = (
    RunnableLambda(generate_content_from_topic)
    | RunnableLambda(rewrite_content_with_style)
    | RunnableLambda(add_metadata)
    | RunnableLambda(post)
)
