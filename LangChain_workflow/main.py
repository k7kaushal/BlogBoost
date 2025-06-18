import asyncio
from chains.blog_pipeline import pipeline

async def main():
    sample_input = {
        "topic": "The Rise of Agentic AI: What it Means for Entrepreneurs",
        "style": "informative",
        "word_count": 350,
        "keywords": "agentic AI, business automation, startup AI tools",
        "target_style": "conversational",
        "tags": ["ai", "automation", "startups"]
    }

    print("Running blog pipeline...")
    result = await pipeline.ainvoke(sample_input)

    # Save output locally
    with open("LangChain_workflow/outputs/blog_output.md", "w", encoding="utf-8") as f:
        f.write(result)

    print("Blog content saved to outputs/blog_output.md")

if __name__ == "__main__":
    asyncio.run(main())
