import typing as t

from django.core.management.base import BaseCommand

from core.models import Question, User


FAKE_QUESTION_DETAILED = """
Maecenas aliquet tortor lorem, quis blandit odio pellentesque eu. In luctus neque at elit dapibus efficitur. Maecenas semper, quam eget congue interdum, nunc leo dignissim metus, eu hendrerit ipsum nibh vel erat. 
Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas pharetra velit dui, nec dignissim nisl mollis quis. Curabitur ac elementum nulla, vel fringilla massa. Phasellus maximus 
eget enim id dignissim. Aliquam hendrerit quis orci ut lacinia. Pellentesque lacus nulla, dignissim nec velit non, maximus hendrerit erat. Pellentesque laoreet lorem vitae nibh finibus, et congue diam malesuada. 
Donec turpis velit, placerat sed tincidunt ornare, tincidunt sit amet diam. Vestibulum tortor lorem, euismod quis auctor eget, dignissim et tortor. Vivamus tincidunt mauris aliquet pretium tincidunt.
"""

class Command(BaseCommand):
    help = 'Генерация сущностей по модели Вопроса'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100)

    def get_exist_user(self) -> t.Optional[User]:
        return User.objects.filter(is_superuser=True).first()

    def handle(self, *args, **options):
        count = options.get('count')
        count_exists_questions = Question.objects.all().count()
        questions_to_create = []
        for n in range(count):
            questions_to_create.append(Question(
                title=f"Вопрос под номером #{count_exists_questions + n + 1}",
                detailed=FAKE_QUESTION_DETAILED,
                author=self.get_exist_user()
            ))

        Question.objects.bulk_create(questions_to_create, batch_size=100)
        print("Было создано {} вопрос в БД".format(len(questions_to_create)))
