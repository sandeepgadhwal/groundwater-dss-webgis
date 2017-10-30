from django.conf.urls import url
from gistool import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
