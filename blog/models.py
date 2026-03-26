import markdown
from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def content_html(self):
        return markdown.markdown(self.content, extensions=['fenced_code', 'codehilite', 'tables'])

    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
