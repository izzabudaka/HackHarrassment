from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'classify', views.index),
    url(r'^test/', views.create_user),
    url(r'^connections/', views.get_relations),
    url(r'^users/', views.get_users),
    url(r'^latest/', views.get_latest_messages),
<<<<<<< HEAD
    url(r'^post/', views.post_message)
=======
    url(r'^post', views.post_message),
    url(r'^create_user', views.create_user),
    url(r'^last_messages', views.last_messages),
    url(r'^sms', views.on_incoming_sms)
>>>>>>> b5970a934dc8d0d99095f59a8364dfe10ccdc9d6
]