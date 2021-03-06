# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
    url(r'^ws/chat/delete/(?P<room_name>[^/]+)/$', consumers.RemoveChatConsumer),
    url(r'^ws/chat/one/(?P<room_name>[^/]+)/$', consumers.OneChatConsumer),
    url(r'^ws/chat/thread/(?P<room_name>[^/]+)/$', consumers.ThreadChatConsumer),
]
