from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login_user),
    path('changepass/', views.changepass),
    path('logout/', views.logout)
]
