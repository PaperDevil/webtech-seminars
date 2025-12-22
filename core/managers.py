from django.db import models

from core.search import SearchManagerMixin


class QuestionManager(SearchManagerMixin, models.Manager):
    psql_field_weights = {'title': 'A', 'detailed': 'B'}
