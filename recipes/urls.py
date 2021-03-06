from django.conf.urls import url
from . import views

app_name = 'recipes'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_recipe/$', views.RecipeCreate.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.RecipeDetail.as_view(), name='detail'),
    url(r'update/(?P<pk>[0-9]+)/$', views.RecipeUpdateView.as_view(), name='update'),
    url(r'^like/$', views.like_recipe, name='like'),
    url(r'^rate/$', views.rate_recipe, name='rate'),
]