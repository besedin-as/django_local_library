from django.conf.urls import url

from ner import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^add_text/$', views.add_text, name='add_text'),
]
