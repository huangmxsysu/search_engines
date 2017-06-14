from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.shouye),
    url(r'^search/$', views.search),

]