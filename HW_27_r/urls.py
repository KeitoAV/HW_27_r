
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from HW_27_r import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("ads.urls")),
    path('', include("users.urls")),


]


# images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
