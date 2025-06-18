from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', include('main.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Include the admin URL only if DISABLE_ADMIN is False
if not settings.DISABLE_ADMIN:
    urlpatterns += [
        path('ch_no_my_ad/', admin.site.urls),
    ]
