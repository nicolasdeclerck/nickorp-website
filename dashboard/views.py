import markdown
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.models import Article
from dashboard.mixins import SuperuserRequiredMixin


class DashboardListView(SuperuserRequiredMixin, ListView):
    model = Article
    template_name = 'dashboard/article_list.html'
    context_object_name = 'articles'


class DashboardCreateView(SuperuserRequiredMixin, CreateView):
    model = Article
    template_name = 'dashboard/article_form.html'
    fields = ['title', 'slug', 'content', 'cover_image', 'tags', 'status']
    success_url = reverse_lazy('dashboard:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['slug'].required = False
        return form


class DashboardUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Article
    template_name = 'dashboard/article_form.html'
    fields = ['title', 'slug', 'content', 'cover_image', 'tags', 'status']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['slug'].required = False
        return form
    success_url = reverse_lazy('dashboard:list')

    def form_valid(self, form):
        if self.request.POST.get('clear_cover_image'):
            form.instance.cover_image.delete(save=False)
            form.instance.cover_image = None
        return super().form_valid(form)


class DashboardDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Article
    template_name = 'dashboard/article_confirm_delete.html'
    success_url = reverse_lazy('dashboard:list')


class MarkdownPreviewView(SuperuserRequiredMixin, View):
    def post(self, request):
        content = request.POST.get('content', '')
        html = markdown.markdown(content, extensions=['fenced_code', 'codehilite', 'tables'])
        return JsonResponse({'html': html})
