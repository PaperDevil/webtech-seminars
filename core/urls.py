from django.urls import path, re_path
from django.views.generic import DetailView

from core.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
]