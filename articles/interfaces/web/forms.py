# interfaces/web/forms.py
from django import forms

from articles.infrastructure.repositories.article.models import DjangoArticle
  # Your Django model

class ArticleForm(forms.ModelForm):
    class Meta:
        model = DjangoArticle
        fields = ['title', 'content', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Title too short")
        return title