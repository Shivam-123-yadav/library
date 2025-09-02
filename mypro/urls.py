from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from library import views
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),   # 👈 home ko sabse upar rakho
    path("", include("library.urls")),

    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)