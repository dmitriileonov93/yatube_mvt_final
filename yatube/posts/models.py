from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        super().save(*args, **kwargs)


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='О чем хочешь всем рассказать?')
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="group_posts",
        verbose_name='Группа',
        help_text='Группа, к которой прикрепится твой пост')
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Комментарий',
        help_text='Пост, к которому прикрепится твой комментарий')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Напиши комментарий')
    created = models.DateTimeField('date published', auto_now_add=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Тот, кто подписался')
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан',
        help_text='Тот, на кого подписался')

    def __str__(self):
        return f'Подписка {self.user.username}'
