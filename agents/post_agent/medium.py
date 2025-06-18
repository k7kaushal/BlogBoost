from .base import PosterAgentBase, BlogPost
from feedgen.feed import FeedGenerator
import os

class MediumPoster(PosterAgentBase):
    def __init__(self, feed_dir="rss_feeds"):
        self.feed_dir = feed_dir
        os.makedirs(feed_dir, exist_ok=True)

    def post(self, post: BlogPost):
        fg = FeedGenerator()
        fe = fg.add_entry()
        fe.title(post.title)
        fe.link(href=post.canonical_url or "http://example.com/temp")
        fe.description(post.content)

        feed_path = os.path.join(self.feed_dir, f"{post.title.replace(' ', '_')}.xml")
        fg.rss_file(feed_path)

        print(f"RSS feed created for Medium import: {feed_path}")
        return feed_path
