from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_review, name='add_review'),
    path('stats/', views.stats, name='stats'),
    path('enterprise/<int:enterprise_id>/', views.enterprise_detail, name='enterprise_detail'),
    path('get-enterprises/', views.get_enterprises_by_category, name='get_enterprises_by_category'),
    path('ya-map-consent/', views.map_consent, name='map_consent'),
    path('ya-map-consent/confirm/', views.confirm_map_consent, name='confirm_map_consent'),
    path('ya-map/', views.map_view, name='ya_map'),
]