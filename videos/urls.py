from django.conf.urls import url, include
from . import views

app_name = 'videos'


urlpatterns = [
    #login
    url(r'^$', views.LoginFormView.as_view() , name='login'),
    #logout
    url(r'^logout/$', views.logout , name='logout'),
    #signup page
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    #IndexView
    url(r'^index/$', views.IndexView, name='index'),
    #yuploads
    url(r'^yuploads/$', views.yuploadView, name='yuploads'),
    #uploadView
    url(r'^add/', views.upload, name='add'),
    #delete_object
    url(r'^yuploads/(?P<video_id>(.*?))$', views.delete, name='delete'),
    #search
    url(r'^search/', views.search, name='search'),
]
