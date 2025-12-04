from django.db import models

class QuestionManager(models.Manager):
    def create_like(self, question_id, author_id):
        from core.models import QuestionLike, Question
        q = Question.objects.get(pk=question_id)

        like, created = QuestionLike.objects.get_or_create(author_id=author_id, question_id=question_id)
        q.rating += 1
        q.save(update_fields=['rating'])
        return like
