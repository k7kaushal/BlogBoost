from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class BlogPost:
    title: str
    content: str
    tags: list[str]
    canonical_url: str = None

class PosterAgentBase(ABC):
    @abstractmethod
    def post(self, post: BlogPost):
        pass
