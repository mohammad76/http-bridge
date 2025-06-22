from . import views
from django.urls import path

urlpatterns = [
    path('', views.proxy_view),
    path('send-mail', views.send_mail_view),
]
