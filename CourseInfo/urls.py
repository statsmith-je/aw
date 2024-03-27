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
    path('db/courselist', views.db_course_list, name = 'dbcourselist'),
    path('automation/slidetitles', views.slide_titles, name = 'slidetitles'),
    path('automation/', views.automation_home, name = 'autohome'),
    path('ceh', views.backend, name = 'backend'),
    path('insights', views.insights, name = 'insights'),
    path('blog', views.blog, name = 'blog'),

]
