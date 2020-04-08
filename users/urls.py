from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='register'),
    url(r'^log_in/$', auth_views.LoginView.as_view(template_name="users/log_in.html"), name='login'),
    url(r'^log_out/$', auth_views.LogoutView.as_view(template_name="users/log_out.html"), name='logout')
]