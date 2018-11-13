from django.urls import path
from . import views
urlpatterns = [
    path('workspace/', views.show_workspaces),
    path('createworkspace/', views.create_workspace),
    path('workspace/<workspace_id>/create/', views.create_channel),
    path('workspace/<workspace_id>/channel/<channel_id>', views.show_messages),
    path('workspace/message/<message_id>', views.show_thread),
    path('user/<userid>',views.oneonerender),
    path('remove/<workid>/channel/<channelid>', views.remove_channel),
    path('workspace/<workspace_id>', views.show_channels),
    path('remove/user/<work_id>/<user_id>', views.remove_user),
    path('workspace/<workspace_id>/invite/', views.invite_user),
    path('workspace/accept/<workspace_id>/<email>/<password>', views.accept_invite),
]
