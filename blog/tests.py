from django.test import TestCase

from blog.models import Article


class ArticleModelTest(TestCase):
    def test_slug_auto_generated(self):
        article = Article.objects.create(title='Mon premier article', content='Test')
        self.assertEqual(article.slug, 'mon-premier-article')

    def test_slug_preserved_if_set(self):
        article = Article.objects.create(title='Test', slug='custom-slug', content='Test')
        self.assertEqual(article.slug, 'custom-slug')

    def test_content_html(self):
        article = Article.objects.create(title='Test', content='## Titre\n\nParagraphe')
        html = article.content_html()
        self.assertIn('<h2>', html)
        self.assertIn('Paragraphe', html)

    def test_tag_list(self):
        article = Article.objects.create(title='Test', content='t', tags='python, django, IA')
        self.assertEqual(article.tag_list(), ['python', 'django', 'IA'])

    def test_tag_list_empty(self):
        article = Article.objects.create(title='Test', content='t')
        self.assertEqual(article.tag_list(), [])


class BlogPublicViewsTest(TestCase):
    def setUp(self):
        self.published = Article.objects.create(
            title='Publié', content='Contenu', status='published'
        )
        self.draft = Article.objects.create(
            title='Brouillon', content='Contenu', status='draft'
        )

    def test_article_list_shows_published(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publié')
        self.assertNotContains(response, 'Brouillon')

    def test_article_detail_published(self):
        response = self.client.get(f'/blog/{self.published.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Publié')

    def test_article_detail_draft_404(self):
        response = self.client.get(f'/blog/{self.draft.slug}/')
        self.assertEqual(response.status_code, 404)
