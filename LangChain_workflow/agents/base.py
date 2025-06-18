from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class BlogPost:
    title: str
    content: str
    tags: List[str]
    canonical_url: str = None

class PosterAgentBase(ABC):
    @abstractmethod
    def post(self, post: BlogPost):
        pass
