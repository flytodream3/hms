from django.urls import path
from django.contrib.auth.views import LoginView

from . import views


app_name = 'users'
urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='users/login.html',
            extra_context = {
                'title': 'log in'
            }
        ),
        name='login'
    ),
    path('logout/', views.logout_view, name='logout'),
]