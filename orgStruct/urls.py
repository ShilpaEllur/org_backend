from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),            # Refers to admin site urls
    path('api/', include('apiLayer.urls'))      # Refers to apiLayer urls
]
