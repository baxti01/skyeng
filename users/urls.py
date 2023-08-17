from django.urls import path

from users.views import login_view, logout_view, sign_up

app_name = 'users'

urlpatterns = [
    path('sign-up', sign_up, name='sign_up'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]
