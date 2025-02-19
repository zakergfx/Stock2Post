"""
URL configuration for autoscoutapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    # Vue pour obtenir un token JWT
    TokenRefreshView,       # Vue pour rafraîchir le token JWT
)
urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Pour obtenir le token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Pour rafraîchir le token
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)