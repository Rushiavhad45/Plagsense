from django.urls import path
from .views import DashboardView, analyze_api, report_detail

app_name = 'analyzer'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/analyze/', analyze_api, name='analyze_api'),
    path('report/<int:report_id>/', report_detail, name='report_detail'),
]