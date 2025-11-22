
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('supply_chain/', include('supply_chain.urls', namespace='supply_chain')),

    path('admin/', admin.site.urls),

    path('', include('pages.urls', namespace='pages')),
]
