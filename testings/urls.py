from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from testings.views import TestAuthView

urlpatterns = [
    re_path('^login/$', TestAuthView.as_view(), name='login'),
    re_path('^logout/$', LogoutView.as_view(), name='logout'),
]