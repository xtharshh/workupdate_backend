from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('teams/', views.TeamListCreateView.as_view(), name='teams'),
    path('tasks/', views.TaskListCreateView.as_view(), name='tasks'),
    path('updates/', views.UpdateListCreateView.as_view(), name='updates'),
    path('updates/<int:pk>/', views.UpdateDetailView.as_view(), name='update-detail'),
    path('team-members/<int:team_id>/', views.team_members_view, name='team-members'),
    path('users/', views.user_list, name='users'),
]
