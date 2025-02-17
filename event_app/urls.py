from django.urls import path # type: ignore
from . import views

from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView # type: ignore






urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('protected/', views.protected_view, name='protected_view'),
    path('add_event/', views.add_event, name='add_event'),
    path('list_event/', views.list_event, name='list_event'),
    path('edit_event/<int:pk>/',views.edit_event, name='edit_event'),
    path('delete_event/<int:pk>/', views.delete_event, name='delete_event'),
    path('create_session/', views.create_session, name='create_session'),
    path('create_speakers/', views.create_speaker, name='create_speaker'),
    path('view_sessions/', views.view_sessions, name='view_sessions'),
    path('view_speakers/', views.view_speakers, name='view_speakers'),
]