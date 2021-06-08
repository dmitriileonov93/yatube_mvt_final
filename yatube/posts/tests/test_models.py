from django.test import TestCase

from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create()
        cls.post = Post.objects.create(text='Тест' * 10,
                                       author=cls.user,)

    def test_str(self):
        """Отображение поля __str__ в Post."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name,
                         str(post),
                         'Ошибка отображения __str__ в Post')

    def test_post_labels(self):
        """Проверка verbose_name."""
        post = PostModelTest.post
        labels = {'text': 'Текст поста',
                  'group': 'Группа'}
        for attr, verbose_name in labels.items():
            with self.subTest(attr=attr):
                verbose = post._meta.get_field(attr).verbose_name
                self.assertEqual(verbose, verbose_name)

    def test_post_helps(self):
        """Проверка help_text."""
        post = PostModelTest.post
        helps = {'text': 'О чем хочешь всем рассказать?',
                 'group': 'Группа, к которой прикрепится твой пост'}
        for attr, help_text in helps.items():
            with self.subTest(attr=attr):
                verbose = post._meta.get_field(attr).help_text
                self.assertEqual(verbose, help_text)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тест' * 51,
            description='Тестовое описание группы')

    def test_str(self):
        """Отображение поля __str__ в Group."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name,
                         str(group),
                         'Ошибка отображения __str__ в Group')
