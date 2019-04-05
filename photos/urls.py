from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns=[
    url(r'^$',views.photos_today,name='photosToday'),
    url(r'^search/', views.search_results, name='search_results'),   
    url(r'^photo/image$', views.photo_image, name='photo_image'),   
    url(r'^upload/profile', views.upload_profile, name='upload_profile'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^comment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
    #  url(r'^search/',views.search_project,name='search_project'),
    url(r'^project/(\d+)',views.project,name='project'),
    url(r'^api/profiles/$',views.ProfileList.as_view(),name='profile_list'),
    url(r'^api/projects/$',views.ProjectList.as_view(),name='project_list'),

 
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)