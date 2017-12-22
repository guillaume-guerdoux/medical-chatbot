from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from conversation import views

app_name = 'conversation'

urlpatterns = [
    url(r'^init_conversation/(?P<pk>[0-9]+)/$', views.init_conversation, name="init_conversation"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
