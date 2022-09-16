"""sofent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from home.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls', namespace='home')),
    path('', include('research.urls', namespace='research')),
    path('', include('farms.urls', namespace='farms')),
    path('', include('donate.urls', namespace='donate')),
    path('', include('shop.urls', namespace='store')),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('', include('templated_email.urls', namespace='templated_email')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "accounts.views.error_404_page"
# handler500 = "accounts.views.error_500_page"
