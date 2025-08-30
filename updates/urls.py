from django.urls import path
from .views import (
    UpdateListCreateView, UpdateDetailView, TaskListCreateView, TeamListView,
    login_view, logout_view, SignupView
)
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('updates/', UpdateListCreateView.as_view(), name='updates'),
    path('updates/<int:pk>/', UpdateDetailView.as_view(), name='update-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='tasks'),
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

