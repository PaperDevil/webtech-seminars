from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

from core.managers import QuestionManager


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления", editable=False, null=True)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Question(DefaultModel):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    detailed = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_questions')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги")
    cover = models.ImageField(upload_to='covers', null=True, blank=True)

    likes = models.ManyToManyField(User, through='QuestionLike', blank=True)
    rating = models.PositiveIntegerField(default=0)
    objects_likes = QuestionManager()

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)


class Answer(DefaultModel):
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_answers')
    answer_text = models.TextField()

    likes = models.ManyToManyField(User, through='AnswerLike', blank=True)
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Ответ на вопрос ID=" + str(self.question_id)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    title = models.CharField(max_length=200, verbose_name="Название тега")

    def __str__(self):
        return self.title


class QuestionLike(DefaultModel):
    class Meta:
        verbose_name = "Лайки вопросов"
        unique_together = ('question', 'author')

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_questions')
    is_like = models.BooleanField(default=True)


class AnswerLike(DefaultModel):
    class Meta:
        verbose_name = "Лайки ответов"
        unique_together = ('answer', 'author')

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_answers')
