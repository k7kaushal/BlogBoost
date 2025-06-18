from .base import PosterAgentBase, BlogPost
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

POST_DATA = {
    "title": " My First Agentic AI Venture: Leveraging agentic AI for business",
    "body_html": '''
    Imagine a convenience store that runs itself. No staff, no manager yelling across aisles, no checkout lines. Just a well-oiled system where every shelf knows what’s missing, the posters update themselves weekly, and something — **someone** — silently optimizes what goes where, when, and why.

    That’s what agentic AI feels like. It’s not just **automation**. It’s **autonomy**. A network of purpose-driven bots, each with a specific job, coordinating like ants — or threads in a system kernel.

    Think of one agent that writes product flyers with just a keyword brief. Another that figures out which flyers get the most eyeballs. Another that digitally sticks them on community boards. And another one? It spies on how folks respond — tweaking the next set based on that feedback.

    Under the hood, it’s a lot like building a **mini operating system**. Each agent is a process: stateless or stateful, reactive or proactive. There’s messaging between them, memory management (**context limits are real pain**), and resource orchestration. You’re not just writing code — you’re designing a **society of bots**.

    There’s a weird joy in watching these things interact. You write a spec for one agent and suddenly two others start behaving differently — like a butterfly flapped its wings in the optimizer and the publisher decided to post at midnight instead.

    To make this even possible, we lean into **open models**, **prompt engineering** that sometimes feels like dark arts, and orchestration logic that makes **Unix pipes jealous**. All stitched together with a lot of duct tape, retries, and printed logs.

    It's clunky at times, magical at others. But every glitch feels like **debugging the future**.

    **Development is in full swing.** I’ll be sharing updates right here. If you’ve got ideas, critiques, or just want to nerd out about agent societies — drop in. **Stay tuned.**

    '''
    ,
    "tags": [
            "ai",
            "startup",
            "buildinpublic"
        ]
}
LOGIN = {
   "email": os.getenv("DEVTO_EMAIL"),
    "password": os.getenv("DEVTO_PASSWORD")
}

class DevtoPoster:
    # devto_playwright_bot
    async def post_to_devto():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            try:
                # Step 1: Navigate to login page
                await page.goto("https://dev.to/enter")
                await page.wait_for_selector("input#user_email", timeout=10000)

                # Step 2: Fill in login credentials
                await page.fill("input#user_email", LOGIN["email"])
                await page.fill("input#user_password", LOGIN["password"])
                await page.click("input[name='commit']")

                # Step 3: Wait for navigation to feed page
                await page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure page is fully loaded

                # Step 4: Navigate to new post editor
                await page.goto("https://dev.to/new")
                await page.wait_for_selector("textarea#article-form-title", timeout=10000)

                # Step 5: Fill in post details
                await page.fill("textarea#article-form-title", POST_DATA["title"])
                await page.fill("textarea#article_body_markdown", POST_DATA["body_html"])

                tag_input_selector = "input#tag-input"
                for tag in POST_DATA["tags"]:
                    await page.fill(tag_input_selector, tag)
                    await page.keyboard.press("Enter")
                    await page.wait_for_timeout(500)

                # Optional: Wait before publishing
                await page.wait_for_timeout(1000)  # Wait for 1 second

                # Step 6: Click publish
                await page.locator("button.c-btn--primary", has_text="Publish").click()

                print("Post submitted successfully!")

            except TimeoutError as e:
                print("Timeout occurred:", e)
                await page.screenshot(path="timeout_error.png")
            except Exception as e:
                print("Unexpected error:", e)
                await page.screenshot(path="unexpected_error.png")
            finally:
                await browser.close()


