from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article

class ArticleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.article = Article.objects.create(
            title='Test Article',
            content='This is a test article.',
            author=self.user
        )
        self.client.login(username='testuser', password='12345')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
        self.assertContains(response, 'This is a test article.')

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test article.')

    def test_article_create_view(self):
        response = self.client.post(reverse('article_create'), {
            'title': 'New Article',
            'content': 'Content of the new article.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_article_edit_view(self):
        response = self.client.post(reverse('article_edit', args=[self.article.pk]), {
            'title': 'Updated Title',
            'content': 'Updated content.',
        })
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Title')

    def test_article_delete_view(self):
        response = self.client.post(reverse('article_delete', args=[self.article.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())
