from django.urls import path

from . import views

app_name = 'supply_chain'

urlpatterns = [
    path('', views.all_projects, name='projects'),
    path('councils', views.all_councils, name='councils'),
    path('projects/<int:project_id>/<', views.project_detail, name='project_detail'),
    path('councils/<slug:slug>', views.council_detail, name='council_detail')
]
