from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Article


class DashboardAccessTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123'
        )
        self.regular_user = User.objects.create_user(
            username='user', password='user123'
        )

    def test_anonymous_redirected_to_login(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/login/?next=/dashboard/', fetch_redirect_response=False)

    def test_regular_user_forbidden(self):
        self.client.login(username='user', password='user123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_access(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)


class DashboardCRUDTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_create_article(self):
        response = self.client.post('/dashboard/create/', {
            'title': 'Nouvel article',
            'content': 'Contenu test',
            'tags': 'test',
            'status': 'draft',
        })
        self.assertRedirects(response, '/dashboard/', fetch_redirect_response=False)
        self.assertTrue(Article.objects.filter(title='Nouvel article').exists())

    def test_create_article_auto_slug(self):
        self.client.post('/dashboard/create/', {
            'title': 'Article sans slug',
            'content': 'Test',
            'status': 'draft',
        })
        article = Article.objects.get(title='Article sans slug')
        self.assertEqual(article.slug, 'article-sans-slug')

    def test_edit_article(self):
        article = Article.objects.create(title='Original', content='Contenu')
        response = self.client.post(f'/dashboard/edit/{article.slug}/', {
            'title': 'Modifié',
            'slug': article.slug,
            'content': 'Nouveau contenu',
            'status': 'published',
        })
        self.assertRedirects(response, '/dashboard/', fetch_redirect_response=False)
        article.refresh_from_db()
        self.assertEqual(article.title, 'Modifié')
        self.assertEqual(article.status, 'published')

    def test_delete_article(self):
        article = Article.objects.create(title='A supprimer', content='Test')
        response = self.client.post(f'/dashboard/delete/{article.slug}/')
        self.assertRedirects(response, '/dashboard/', fetch_redirect_response=False)
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())

    def test_dashboard_shows_drafts(self):
        Article.objects.create(title='Brouillon', content='Test', status='draft')
        response = self.client.get('/dashboard/')
        self.assertContains(response, 'Brouillon')


class MarkdownPreviewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_preview_returns_html(self):
        response = self.client.post('/dashboard/preview/', {'content': '## Titre'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('<h2>', data['html'])

    def test_preview_anonymous_redirected(self):
        self.client.logout()
        response = self.client.post('/dashboard/preview/', {'content': 'test'})
        self.assertEqual(response.status_code, 302)
