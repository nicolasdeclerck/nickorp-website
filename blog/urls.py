from django.urls import path

from blog.views import ArticleDetailView, ArticleListView

app_name = 'blog'

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
]
