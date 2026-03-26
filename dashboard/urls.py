from django.urls import path

from dashboard.views import (
    DashboardCreateView,
    DashboardDeleteView,
    DashboardListView,
    DashboardUpdateView,
    MarkdownPreviewView,
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardListView.as_view(), name='list'),
    path('create/', DashboardCreateView.as_view(), name='create'),
    path('edit/<slug:slug>/', DashboardUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>/', DashboardDeleteView.as_view(), name='delete'),
    path('preview/', MarkdownPreviewView.as_view(), name='preview'),
]
