from django.urls import path

from . import views

urlpatterns = [
    # ex: /update/
    path('', views.updater, name='updater'),
]