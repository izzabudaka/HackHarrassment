from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^test/', views.create_user),
    url(r'^connections/', views.get_relations),
    url(r'^users/', views.get_users),
    url(r'^latest/', views.get_latest_messages)
]