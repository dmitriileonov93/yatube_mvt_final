import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.post = Post.objects.create(
            text='Текст первого тестового поста',
            author=User.objects.create_user(username='Dima'))
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='Dima')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись Post."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B')
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif')
        form_data = {
            'text': 'Текст второго тестового поста',
            'author': User.objects.get(username='Dima'),
            'image': uploaded, }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True)
        new_post = Post.objects.first()
        asserts_equal = {
            response.status_code: 200,
            Post.objects.count(): posts_count + 1,
            new_post.text: 'Текст второго тестового поста',
            new_post.author: User.objects.get(username='Dima'),
            new_post.group: None,
        }
        for test, result in asserts_equal.items():
            with self.subTest(test=test):
                self.assertEqual(test, result)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(
            Post.objects.filter(
                text='Текст второго тестового поста',
                author=User.objects.get(username='Dima'),
                image='posts/small.gif'
            ).exists()
        )

    def test_guest_can_not_create_post(self):
        """Неавторизованный пользователь не может опубликовать пост."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст второго тестового поста',
            'author': User.objects.get(username='Dima')}
        response = self.guest_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse('login') + '?next=' + reverse('new_post'))
        self.assertEqual(Post.objects.count(), posts_count)

    def test_edit_post(self):
        """Валидная форма изменяет запись Post."""
        posts_count = Post.objects.count()
        test_post = PostCreateFormTests.post
        test_author_username = test_post.author.username
        form_data = {'text': 'Новый текст первого тестового поста'}
        response = self.authorized_client.post(
            reverse('post_edit',
                    kwargs={'username': test_author_username,
                            'post_id': test_post.id}),
            data=form_data,
            follow=True)
        self.assertRedirects(response,
                             reverse('post',
                                     kwargs={'username': test_author_username,
                                             'post_id': test_post.id}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Новый текст первого тестового поста',
                author=User.objects.get(username='Dima'),
            ).exists())


# class CommentCreateFormTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.post = Post.objects.create(
#             text='Текст первого тестового поста',
#             author=User.objects.create_user(username='Dima'))
#         cls.comment = Comment.objects.create(
#             text='Текст комментария',
#             post=Post.objects.get(text='Текст первого тестового поста')
#         )
#         cls.form = CommentForm()

#     def setUp(self):
#         self.guest_client = Client()
#         self.user = User.objects.get(username='Dima')
#         self.authorized_client = Client()
#         self.authorized_client.force_login(self.user)

#     def test_create_comment(self):
#         """Валидная форма создает запись Comment."""
#         comment_count = Comment.objects.count()
#         test_post = CommentCreateFormTests.post
#         test_author_username = test_post.author.username
#         form_data = {
#             'text': 'Текст тестового комментария',
#         }
#         response = self.authorized_client.post(
#             reverse('post',
#                     kwargs={'username': test_author_username,
#                     'post_id': test_post.id}),
#             data=form_data,
#             follow=True)
#         new_comment = Comment.objects.first()
#         print(comment_count)
#         print(test_post.comment.all())
#         print(new_comment)
#         print(Comment.objects.count())
