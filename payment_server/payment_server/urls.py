from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from payments.classic_site import classic_admin_site
from payments.unfold_site import unfold_admin_site

urlpatterns = [
    path("admin/", classic_admin_site.urls),
    path("dashboard/", unfold_admin_site.urls),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()
