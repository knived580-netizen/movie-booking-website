"""
URL configuration for moviebooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from booking import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('book/<int:movie_id>/theatres/', views.theatre_list, name='theatre_list'),
    path('book/show/<int:show_id>/quantity/', views.ticket_quantity, name='ticket_quantity'),
    path('book/show/<int:show_id>/seats/<int:quantity>/', views.seat_selection, name='seat_selection'),
    path('payment/<uuid:booking_id>/', views.payment_gateway, name='payment_gateway'),
    path('payment/<uuid:booking_id>/process/', views.process_payment, name='process_payment'),
    path('payment/<uuid:booking_id>/confirm/', views.confirm_payment, name='confirm_payment'),
    path('ticket/<uuid:booking_id>/', views.ticket_detail, name='ticket_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)