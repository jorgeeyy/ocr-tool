from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_redirect, name='index'),
    path('upload/', views.DocumentUploadView.as_view(), name='upload_document'),
    path('documents/', views.DocumentListView.as_view(), name='document_list'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document_delete'),
    path('documents/<int:pk>/download/', views.download_text, name='download_text'),
]
