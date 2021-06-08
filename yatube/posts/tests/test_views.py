import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.group = Group.objects.create(
            title='test_name',
            description='Тестовое описание группы')
        cls.post = Post.objects.create(
            text='Текст тестового поста',
            author=User.objects.create_user(
                username='Dima',
                first_name='Дима',
                last_name='Леонов'),
            group=Group.objects.get(title='test_name'),
            image=uploaded
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='Dima')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        group = PostsPagesTests.group
        group_slug = group.slug
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': (reverse(
                'group', kwargs={'slug': group_slug})),
            'new_post.html': reverse('new_post'), }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        test_post = PostsPagesTests.post
        response = self.authorized_client.get(reverse('index'))
        first_post = response.context['page'].object_list[0]
        attrs = {first_post.text: test_post.text,
                 first_post.pub_date: test_post.pub_date,
                 first_post.author: test_post.author,
                 first_post.group: test_post.group}
        for first_attr, test_attr in attrs.items():
            with self.subTest(first_attr=first_attr):
                self.assertEqual(first_attr, test_attr)
        self.assertTrue(first_post.image)

    def test_index_page_cache(self):
        """Проверка кэша index"""
        response_first = self.authorized_client.get(reverse('index'))
        Post.objects.create(
            text='Текст тестового поста',
            author=User.objects.get(
                username='Dima'))
        response_second = self.authorized_client.get(reverse('index'))
        self.assertEqual(response_first.content, response_second.content)

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        test_group = PostsPagesTests.group
        test_post = test_group.group_posts.last()
        response = self.authorized_client.get(reverse(
            'group', kwargs={'slug': test_group.slug}))
        page_group = response.context['group']
        page_post = response.context['page'].object_list[0]
        attrs = {page_group.title: test_group.title,
                 page_group.description: test_group.description,
                 page_post.text: test_post.text,
                 page_post.pub_date: test_post.pub_date,
                 page_post.author: test_post.author}
        for page_attr, test_attr in attrs.items():
            with self.subTest(page_attr=page_attr):
                self.assertEqual(page_attr, test_attr)
        self.assertTrue(page_post.image)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        test_author = User.objects.get(username='Dima')
        test_post = test_author.posts.last()
        response = self.authorized_client.get(reverse(
            'profile', kwargs={'username': test_author.username}))
        page_author = response.context['author']
        page_post = response.context['page'].object_list[0]
        attrs = {page_author.get_full_name(): test_author.get_full_name(),
                 page_author.username: test_author.username,
                 page_author.posts.count(): test_author.posts.count(),
                 page_post.text: test_post.text,
                 page_post.pub_date: test_post.pub_date,
                 page_post.author: test_post.author}
        for page_attr, test_attr in attrs.items():
            with self.subTest(page_attr=page_attr):
                self.assertEqual(page_attr, test_attr)
        self.assertTrue(page_post.image)

    def test_post_page_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        test_post = PostsPagesTests.post
        test_author = test_post.author
        response = self.authorized_client.get(reverse(
            'post', kwargs={'username': test_author.username,
                            'post_id': test_post.id}))
        page_post = response.context['post']
        page_author = response.context['author']
        attrs = {page_author.get_full_name(): test_author.get_full_name(),
                 page_author.username: test_author.username,
                 page_author.posts.count(): test_author.posts.count(),
                 page_post.text: test_post.text,
                 page_post.pub_date: test_post.pub_date,
                 page_post.author: test_post.author}
        for page_attr, test_attr in attrs.items():
            with self.subTest(page_attr=page_attr):
                self.assertEqual(page_attr, test_attr)
        self.assertTrue(page_post.image)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post edit сформирован с правильным контекстом."""
        test_post = PostsPagesTests.post
        test_author_username = test_post.author.username
        response = self.authorized_client.get(reverse(
            'post_edit', kwargs={'username': test_author_username,
                                 'post_id': test_post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_new_page_show_correct_context(self):
        """Шаблон new сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Dima')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for new_post in range(0, 13):
            Post.objects.create(
                text='Текст тестового поста',
                author=self.user)

    def test_first_page_contains_ten_records(self):
        """Тестирование первой страницы паджинатора"""
        response = self.guest_client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_contains_three_records(self):
        """Тестирование второй страницы паджинатора"""
        response = self.guest_client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)


class PostWithGroupTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test_name',
            description='Тестовое описание группы')
        cls.post = Post.objects.create(
            text='Текст тестового поста',
            author=User.objects.create_user(username='Dima'),
            group=Group.objects.get(title='test_name')
        )

    def setUp(self):
        self.guest_client = Client()

    def test_post_with_group_on_index_page(self):
        """Пост с группой есть на главной странице index"""
        response = self.guest_client.get(reverse('index'))
        post = PostWithGroupTests.post
        container = response.context.get('page')
        self.assertIn(post, container)

    def test_post_with_group_on_group_page(self):
        """Пост с группой есть на странице group"""
        test_group = PostWithGroupTests.group
        response = self.guest_client.get(reverse(
            'group', kwargs={'slug': test_group.slug}))
        post = PostWithGroupTests.post
        container = response.context.get('page')
        self.assertIn(post, container)
