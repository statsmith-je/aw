
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name = 'home'),
    path('insights', insights, name = 'insights'),
    path('blog', blog, name = 'blog'),
    path('about', about, name = 'about'),
    path('contact', contact, name = 'contact'),
    path('learninganalytics', learninganalytics, name = 'learninganalytics'),
    path('ai', ai, name = 'ai'),
    path('data_analytics', data_analytics, name = 'data'),
    path('secure_tech', secure_tech, name = 'secure_tech'),
    path('consulting', consulting, name = 'consulting'),
    path('capability', capability, name = 'capability'),
    path('article/<int:pk>', InsightsView.as_view(), name = 'blogposts'),
    path('services/', services, name = 'services'),
]


