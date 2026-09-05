from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("apps.dashboard.urls")),
    path("youtube/", include("apps.youtube.urls")),
    path("access-keys/", include("apps.access_keys.urls")),
    path("search-keywords/", include("apps.search_keywords.urls")),
    path("countries/", include("apps.countries.urls")),
    path("relevance-keywords/", include("apps.relevance_keywords.urls")),
    path("posting-criteria/", include("apps.posting_criteria.urls")),
    path("results/", include("apps.results.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )