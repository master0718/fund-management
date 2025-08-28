from django.urls import path
from . import views

urlpatterns = [
    path('', views.fund_list, name='fund_list'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('api/funds/', views.api_fund_list, name='api_fund_list'),
    path('api/funds/<int:fund_id>/', views.api_fund_detail, name='api_fund_detail'),
]