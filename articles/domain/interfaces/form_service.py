# domain/interfaces/form_service.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from articles.domain.models.article import Article

class ArticleFormInterface(ABC):
    """Interface for article form handling"""
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate form data"""
        pass
    
    @abstractmethod
    def save_to_article(self, article: Article) -> None:
        """Transfer form data to article entity"""
        pass
    
    @abstractmethod
    def load_from_article(self, article: Article) -> None:
        """Populate form from article entity"""
        pass