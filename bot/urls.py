from django.conf.urls import url

from bot.views import CommandReceiveView

urlpatterns = [
    url(r'^(?P<bot_token>.+)$', CommandReceiveView.as_view(), name='command'),
]