from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from conversation import views

app_name = 'conversation'

urlpatterns = [
    url(r'^init_conversation/$', views.init_conversation, name="init_conversation"),
    url(r'^converse/$', views.converse, name="converse"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
