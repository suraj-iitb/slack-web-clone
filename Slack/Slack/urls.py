"""Slack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from workspace.views import create, show_workspace, create_channel, invite_workspace, show_channel
from django.contrib.auth import views as authview
from users.views import login_user, register_user, log_out, send_data
urlpatterns = [
    path('workspace/create/channel/workspace/channel/<room_name>', show_channel, name='room'),
    path('invite/workspace/workspace/channel/<room_name>', show_channel, name='room'),
    path(r'login/workspace/workspace/channel/<room_name>', show_channel, name='room'),
    path(r'invite/workspace/<workid>', invite_workspace, name='invite_workspace'),
    path(r'workspace/create/workspace/<workspace_id>', show_workspace, name='showworkspace'),
    path(r'login/workspace/<workspace_id>', show_workspace, name='show_workspace'),
    path('workspace/create/channel/<work_id>', create_channel, name='create_channel'),
    path('register/', register_user, name='register'),
    path('logout/', log_out, name='logout'),
    path('login/', login_user, name='login'),
    path('workspace/create/', create, name='create'),
    path('admin/', admin.site.urls),
    path('accounts/profile/', login_user, name='user'),
    path('', login_user, name='homepage'),
    
]