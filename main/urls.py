# -*- coding: utf-8 -*-
from django.urls import path
from . import apps, views, models

app_name = apps.AppConfig.name
urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('top/<int:page>', views.TopView.as_view(), name='top'),
    path('in/',  views.ToggleView, {'action': models.ACTION_IN},  name='in'),
    path('out/', views.ToggleView, {'action': models.ACTION_OUT}, name='out'),
    path('log/', views.LogView.as_view(), name='log'),
    path('log/<int:page>/', views.LogView.as_view(), name='log'),
]
