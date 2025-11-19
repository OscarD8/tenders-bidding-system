from django.urls import path

from . import views

app_name = 'supply_chain'

urlpatterns = [
    path('councils', views.all_councils, name='councils'),
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list')
]
