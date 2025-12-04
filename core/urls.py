from django.urls import path, re_path
from django.views.generic import DetailView

from core.views import (
    IndexView, AuthView,
    logout_view, CreateQuestionView,
    QuestionLikeAPIView, AnswerLikeAPIView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_question/', CreateQuestionView.as_view(), name='create_question'),
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('api/question/<int:pk>/toggle_like', QuestionLikeAPIView.as_view(), name='like_question'),
    path('api/answer/<int:pk>/like', AnswerLikeAPIView.as_view(), name='like'),
    # path('api/answer/<int:pk>/dislike', QuestionLike.as_view(), name='unlike'),
]