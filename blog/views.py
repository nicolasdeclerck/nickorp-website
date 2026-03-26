from django.views.generic import DetailView, ListView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status='published')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(status='published')
