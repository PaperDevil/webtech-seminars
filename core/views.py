import math

from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from core.models import Question, Tag
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
