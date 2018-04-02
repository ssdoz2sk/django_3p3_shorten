from django.urls import path

from shortener import views

urlpatterns = [
    path('<code>', views.shorten_redirect, name='shorten_redirect'),
    path('', views.landingPage, name='landingPage'),
    path('api/shorten', views.shorten, name='shorten'),
    path('api/history', views.history, name='history'),
    # path('api/report', name='report'),
    # path('api/remove', name='remove'),
]
