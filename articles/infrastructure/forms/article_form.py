# infrastructure/forms/article_form.py
from typing import Any, Dict
from interfaces.web.forms import ArticleForm  # Your Django form
from domain.interfaces.form_service import ArticleFormInterface
from domain.models.article import Article

class DjangoArticleFormAdapter(ArticleFormInterface):
    """Adapts Django's ArticleForm to domain interface"""
    
    def __init__(self, form_data: Dict = None):
        self.form = ArticleForm(data=form_data)
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate the form data"""
        self.form = ArticleForm(data=data)
        return self.form.is_valid()
    
    def save_to_article(self, article: Article) -> None:
        """Transfer validated data to article entity"""
        if not self.form.is_valid():
            raise ValueError("Cannot save invalid form data")
        
        article.title = self.form.cleaned_data['title']
        article.content = self.form.cleaned_data['content']
        article.status = self.form.cleaned_data.get('status', 'draft')
    
    def load_from_article(self, article: Article) -> None:
        """Populate form from article entity"""
        initial_data = {
            'title': article.title,
            'content': article.content,
            'status': article.status
        }
        self.form = ArticleForm(initial=initial_data)