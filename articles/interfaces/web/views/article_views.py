from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from domain.models.article import Article
from application.use_cases.article_management.create_article import CreateArticleUseCase
from application.use_cases.article_management.update_article import UpdateArticleUseCase
from application.use_cases.article_management.publish_article import PublishArticleUseCase
from application.use_cases.article_management.archive_article import ArchiveArticleUseCase
from interfaces.web.forms import ArticleForm

class ArticleListView(ListView):
    """نمایش لیست مقالات"""
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 9
    ordering = ['-published_at']
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(status='published')
        
        # فیلتر بر اساس تگ
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name=tag)
            
        # فیلتر بر اساس دسته‌بندی
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__id=category)
            
        return queryset.select_related('author').prefetch_related('tags', 'categories')

class ArticleDetailView(DetailView):
    """نمایش جزئیات مقاله"""
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return super().get_queryset().select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # افزایش تعداد بازدیدها
        if not self.request.user.is_authenticated or self.request.user != self.object.author:
            self.object.increment_view_count()
            self.object.save()
        
        # مقالات مرتبط
        context['related_articles'] = Article.objects.filter(
            tags__in=self.object.tags.all()
        ).exclude(
            id=self.object.id
        ).distinct()[:3]
        
        return context

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """ایجاد مقاله جدید"""
    form_class = ArticleForm
    template_name = 'articles/edit.html'
    success_url = reverse_lazy('article_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        use_case = CreateArticleUseCase()
        try:
            article = use_case.execute({
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
                'author': self.request.user,
                'tags': form.cleaned_data['tags'],
                'categories': form.cleaned_data['categories'],
                'status': form.cleaned_data['status']
            })
            messages.success(self.request, 'مقاله با موفقیت ایجاد شد.')
            return redirect('article_detail', slug=article.slug)
        except Exception as e:
            messages.error(self.request, f'خطا در ایجاد مقاله: {str(e)}')
            return self.form_invalid(form)

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """ویرایش مقاله"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'article'
    
    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})
    
    def dispatch(self, request, *args, **kwargs):
        # بررسی مجوز ویرایش
        article = self.get_object()
        if not request.user.is_authenticated or (request.user != article.author and not request.user.is_staff):
            messages.error(request, 'شما مجوز ویرایش این مقاله را ندارید.')
            return redirect('article_detail', slug=article.slug)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        use_case = UpdateArticleUseCase()
        try:
            article = use_case.execute({
                'article_id': str(self.object.id),
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
                'tags': form.cleaned_data['tags'],
                'categories': form.cleaned_data['categories'],
                'status': form.cleaned_data['status'],
                'editor': self.request.user
            })
            messages.success(self.request, 'مقاله با موفقیت به‌روزرسانی شد.')
            return redirect('article_detail', slug=article.slug)
        except Exception as e:
            messages.error(self.request, f'خطا در به‌روزرسانی مقاله: {str(e)}')
            return self.form_invalid(form)

def publish_article(request, slug):
    """انتشار مقاله"""
    article = get_object_or_404(Article, slug=slug)
    
    if not request.user.is_authenticated or (request.user != article.author and not request.user.is_staff):
        messages.error(request, 'شما مجوز انتشار این مقاله را ندارید.')
        return redirect('article_detail', slug=slug)
    
    use_case = PublishArticleUseCase()
    try:
        use_case.execute({
            'article_id': str(article.id),
            'publisher': request.user
        })
        messages.success(request, 'مقاله با موفقیت منتشر شد.')
    except Exception as e:
        messages.error(request, f'خطا در انتشار مقاله: {str(e)}')
    
    return redirect('article_detail', slug=slug)