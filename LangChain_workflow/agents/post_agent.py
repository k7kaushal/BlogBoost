import os
from dataclasses import asdict
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from langchain_core.tools import tool
from agents.base import BlogPost

load_dotenv()

LOGIN = {
    "email": os.getenv("DEVTO_EMAIL"),
    "password": os.getenv("DEVTO_PASSWORD")
}

@tool("post_to_devto")
async def post_to_devto(post: BlogPost) -> str:
    """
    Automate posting a blog to dev.to using Playwright.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Step 1: Login
            await page.goto("https://dev.to/enter")
            await page.fill("input#user_email", LOGIN["email"])
            await page.fill("input#user_password", LOGIN["password"])
            await page.click("input[name='commit']")
            await page.wait_for_timeout(3000)

            # Step 2: Go to new post page
            await page.goto("https://dev.to/new")
            await page.wait_for_selector("textarea#article-form-title", timeout=10000)

            # Step 3: Fill title and content
            await page.fill("textarea#article-form-title", post.title)
            await page.fill("textarea#article_body_markdown", post.content)

            # Step 4: Fill tags
            for tag in post.tags:
                await page.fill("input#tag-input", tag)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(300)

            # Step 5: Publish
            await page.locator("button.c-btn--primary", has_text="Publish").click()
            await page.wait_for_timeout(2000)

            return "Post published successfully on dev.to"

        except Exception as e:
            await page.screenshot(path="post_error.png")
            return f"Failed to post: {str(e)}"
        finally:
            await browser.close()
