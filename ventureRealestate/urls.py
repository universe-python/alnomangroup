
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import auth_login, auth_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('indexApp.urls')),
    path('', include('useraccount.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('auth-login/',auth_login,name='auth_login'),
    path('auth-logout/',auth_logout,name='auth_logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('i18n/', include('django.conf.urls.i18n')),

    # path('captcha/', include('captcha.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


