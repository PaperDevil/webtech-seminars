from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

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
