import json
import math

from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from core.models import Question, Tag, QuestionLike, AnswerLike, Answer
from core.forms import LoginForm, QuestionForm


# Create your views here.
def index(request):
    print(request)

    return render(request, 'core/index.html')

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class IndexView(TemplateView):
    http_method_names = ['get',]
    template_name = 'core/index.html'
    QUESTIONS_PER_PAGE = 4

    def get_questions(self, tag = None):
        if tag is None:
            return Question.objects.all().order_by('-id')

        return Question.objects.filter(tags__title__in=[tag])

    def get_tags(self):
        return Tag.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))
        tag = self.request.GET.get('tag', None)
        context['page'] = page
        questions = self.get_questions(tag)
        context['count_questions'] = questions.count()
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['max_page'] = math.ceil(questions.count() / self.QUESTIONS_PER_PAGE)
        context['pages'] = [i for i in range(1, context['max_page'])]
        if page == 1:
            context['new_questions'] = questions[0:self.QUESTIONS_PER_PAGE]
        else:
            context['new_questions'] = questions[page * self.QUESTIONS_PER_PAGE:(page * self.QUESTIONS_PER_PAGE) + self.QUESTIONS_PER_PAGE]


        context['tags'] = Tag.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class CreateQuestionView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'core/create_question_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuestionForm()
        return context

    def post(self, request, *args, **kwargs):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.cover = request.FILES['image']
            question.save()
            return redirect('index')

        return render(request, 'core/create_question_template.html', {'form': form})

class AuthView(TemplateView):
    http_method_names = ['get', 'post']
    template_name = 'core/login_template.html'

    def get_context_data(self, **kwargs):
        form = LoginForm()
        context = super(AuthView, self).get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.add_message(request, messages.SUCCESS, "Вы успешно авторизованы в вашем аккаунте")
            return redirect('/')

        return render(request, 'core/login_template.html', {
            'form': form
        })

@login_required()
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class QuestionLikeAPIView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('pk')
        is_like = json.loads(request.body.decode('utf-8')).get('is_like', True)
        question = get_object_or_404(Question, pk=question_id)
        if question.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором вопроса."
            }, status=400)

        like_exists = QuestionLike.objects.filter(author=request.user, question_id=question_id).first()
        if like_exists and like_exists.is_like != is_like:
            like_exists.is_like = is_like
            like_exists.save(update_fields=['is_like'])
            question.rating += 1 if is_like else -1
            question.save(update_fields=['rating'])

        if like_exists:
            return JsonResponse({
                'success': True,
                'id': like_exists.id,
                'rating': question.rating,
            }, status=200)

        like = QuestionLike.objects.create(author=request.user, question_id=question_id, is_like=is_like)
        question.rating += 1 if is_like else -1
        question.save(update_fields=['rating', 'updated_at'])
        return JsonResponse({
            'success': True,
            'id': like.id,
            'rating': question.rating,
        }, status=201)


class AnswerLikeAPIView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        answer_id = request.POST.get('pk')
        answer = get_object_or_404(Answer, pk=answer_id)
        if answer.author == request.user:
            return JsonResponse({
                'success': False,
                'error': "Вы являетесь автором ответа."
            }, status=400)

        like, created = AnswerLike.objects.get_or_create(author=request.user, answer_id=answer_id)
        answer.rating += 1
        answer.save(update_fields=['rating'])
        return JsonResponse({
            'success': True,
            'id': like.id,
        }, status=201 if created else 200)
