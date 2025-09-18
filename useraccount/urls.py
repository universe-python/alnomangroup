from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register-view/', RegisterListView.as_view(), name='register_view'),
    path('register-update<str:pk>/', RegisterEditView.as_view(), name='register_edit'),
    path('register-delete<str:pk>/', register_delete, name='register_delete'),
    path('register-change/', ChangePasswordView.as_view(), name='change_password'),
]