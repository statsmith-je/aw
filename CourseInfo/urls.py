from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('db/search', views.search, name = 'search'),
    path('db/course/<int:pk>', views.course, name = 'course'),
    path('db/edit/<int:pk>', views.edit_course, name = 'edit_course'),
    path('db/module/<int:pk>', views.module, name = 'modules'),
    path('db/upload', views.upload_file, name = 'upload'),
    path('elo', views.elo_search, name = 'elo_search'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('db/courseadd', views.add_course, name = 'add_course'),
    path('db', views.db_home, name = 'db_home'),
    path('automation/slidetitles', views.slide_titles, name = 'slidetitles'),
    path('automation/home', views.auto_home, name = 'autohome')
]
