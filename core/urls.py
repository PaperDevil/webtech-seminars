from django.urls import path, re_path
from django.views.generic import DetailView

from core.views import IndexView, AuthView, logout_view, CreateQuestionView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_question/', CreateQuestionView.as_view(), name='create_question'),
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]