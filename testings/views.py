from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from core.models import Question, QuestionLike, Answer, AnswerLike
from testings.forms import LoginForm


class TestAuthView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'testings/test_auth_template.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')

        context = super(TestAuthView, self).get_context_data(**kwargs)
        form = LoginForm()
        context['form'] = form
        return context


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.user
            login(request, user)  # Создаем сессию
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)

        return render(request, self.template_name, {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('login')


@method_decorator(login_required, name='dispatch')
class LikeQuestionAPIView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        question_pk = kwargs.get('id')
        question = get_object_or_404(Question, pk=question_pk)
        if question.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором этого вопроса!"
            }, status=400)

        exists_like = QuestionLike.objects.filter(question=question, author=request.user).first()
        if exists_like:
            return JsonResponse({
                'success': True,
                'id': exists_like.id,
            }, status=200)

        question_like = QuestionLike.objects.create(question=question, author=request.user)
        question.likes_count += 1
        question.save(update_fields=['likes_count'])
        return JsonResponse({
            'success': True,
            'id': question_like.id,
        }, status=201)


@method_decorator(login_required, name='dispatch')
class LikeAnswerAPIView(TemplateView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        answer_pk = kwargs.get('id')
        answer = Answer.objects.filter(pk=answer_pk).first()
        if not answer:
            raise Http404()

        if answer.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором этого ответа!"
            })

        answer_like, created = AnswerLike.objects.get_or_create(answer=answer, author=request.user)
        answer.likes_count += 1
        answer.save(update_fields=['likes_count'])
        return JsonResponse({
            'success': True,
            'id': answer_like.id,
        }, status=201 if created else 200)
