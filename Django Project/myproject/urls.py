
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('supply_chain/', include('supply_chain.urls')),
    path('admin/', admin.site.urls),
]
