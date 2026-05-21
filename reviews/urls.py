from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_review, name='add_review'),
    path('stats/', views.stats, name='stats'),
    path('enterprise/<int:enterprise_id>/', views.enterprise_detail, name='enterprise_detail'),
    path('ya-map/', views.map_view, name='ya_map'),
    path('get-enterprises/', views.get_enterprises_by_category, name='get_enterprises_by_category'),
]