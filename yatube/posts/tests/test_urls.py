from django.test import Client, TestCase

from posts.models import Group, Post, User


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test_name',
            description='Тестовое описание группы')
        cls.user = User.objects.create_user(username='dima_not_author')
        cls.post = Post.objects.create(
            text='Текст тестового поста',
            author=User.objects.create_user(username='dima_author'),
            group=Group.objects.get(title='test_name')
        )

    def setUp(self):
        self.guest_client = Client()
        self.user_not_author = User.objects.get(username='dima_not_author')
        self.authorized_client_not_author = Client()
        self.authorized_client_not_author.force_login(PostsURLTests.user)
        self.user_author = User.objects.get(username='dima_author')
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user_author)

    def test_homepage(self):
        """Проверка доступности главной страницы."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_page(self):
        """Проверка доступности страницы группы."""
        group = PostsURLTests.group
        group_slug = f'/group/{group.slug}/'
        response = self.guest_client.get(group_slug)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        """Проверка доступности страницы профайла."""
        user = PostsURLTests.user
        profile_slug = f'/{user.username}/'
        response = self.guest_client.get(profile_slug)
        self.assertEqual(response.status_code, 200)

    def test_post_page(self):
        """Проверка доступности страницы поста."""
        post = PostsURLTests.post
        author = post.author
        post_slug = f'/{author}/{post.id}/'
        response = self.guest_client.get(post_slug)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_anonymous(self):
        """
        Страница редактирования поста перенаправляет анонимного пользователя.
        """
        post = PostsURLTests.post
        author = post.author
        post_edit_slug = f'/{author}/{post.id}/edit/'
        response = self.guest_client.get(post_edit_slug, follow=True)
        self.assertRedirects(
            response, f'/auth/login/?next=%2F{author}%2F{post.id}%2Fedit%2F')

    def test_edit_post_author(self):
        """
        Страница редактирования поста доступна автору.
        """
        post = PostsURLTests.post
        author = post.author
        post_edit_slug = f'/{author}/{post.id}/edit/'
        response = self.authorized_client_author.get(post_edit_slug)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_redirect_not_author(self):
        """
        Страница редактирования поста перенапраляет не автора.
        """
        post = PostsURLTests.post
        author = post.author
        post_edit_slug = f'/{author}/{post.id}/edit/'
        response = self.authorized_client_not_author.get(post_edit_slug)
        self.assertRedirects(
            response, f'/{author}/{post.id}/')

    def test_new_page_authorized(self):
        """
        Проверка доступности страницы /new/ авторизированному пользователю.
        """
        response = self.authorized_client_author.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_new_page_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        group = PostsURLTests.group
        group_slug = f'/group/{group.slug}/'
        post = PostsURLTests.post
        post_edit_slug = f'/{post.author}/{post.id}/edit/'
        templates_url_names = {
            '/': 'index.html',
            group_slug: 'group.html',
            '/new/': 'new_post.html',
            post_edit_slug: 'new_post.html', }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)


class ErrorsURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_server_return_404(self):
        """Cервер возвращает код 404, если страница не найдена."""
        response = self.guest_client.get('/12345678/')
        self.assertEqual(response.status_code, 404)
