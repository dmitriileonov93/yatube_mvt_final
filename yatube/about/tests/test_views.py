from django.test import Client, TestCase
from django.urls import reverse


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_pages_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:author, доступен."""
        views_names = ('about:author', 'about:tech')
        for name in views_names:
            with self.subTest(name=name):
                response = self.guest_client.get(reverse(name))
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """При запросе к about применяются шаблоны about/."""
        templates_url_names = {
            'about/author.html': reverse('about:author'),
            'about/tech.html': reverse('about:tech'),
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
