from django.contrib import admin
from django.urls import path, include

from django.views.static import serve
from django.conf.urls import url
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('', include('accounts.urls')),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
]
