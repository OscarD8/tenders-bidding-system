from django.urls import path

from . import views

app_name = 'supply_chain'

urlpatterns = [
    path('projects', views.all_projects, name='projects'),
    path('councils', views.all_councils, name='councils'),
    path('councils/<slug:council_slug>/<slug:project_slug>', views.project_detail, name='project_detail'),
    path('councils/<slug:slug>', views.council_detail, name='council_detail'),
    path('councils/<slug:council_slug>/<slug:project_slug>/<slug:requirement_slug>/bid', views.place_bid,
         name='place_bid'),
]
