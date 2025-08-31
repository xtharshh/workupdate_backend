from rest_framework import generics, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, Team, TeamMember, Task, Update
from .serializers import (
    UserSerializer, TeamSerializer, TeamMemberSerializer, TaskSerializer, UpdateSerializer
)
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


User = get_user_model()

# ------------ User List View for Dropdowns on Manager Screen ------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    role = request.GET.get('role')
    users = CustomUser.objects.all()
    if role:
        users = users.filter(role=role)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# For getting team members of a specific team (needed by frontend)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_members_by_team(request, team_id):
    members = TeamMember.objects.filter(team_id=team_id)
    serializer = TeamMemberSerializer(members, many=True)
    return Response(serializer.data)

class TeamListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMember.objects.filter(user=self.request.user)

# ------------ Tasks ------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    role = request.GET.get('role')
    users = CustomUser.objects.all()
    if role:
        users = users.filter(role=role)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# ------------ Auth & Signup ------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_200_OK)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    Token.objects.filter(user=request.user).delete()
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'employee')
        )

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "username": user.username,
            "role": user.role,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    role = request.query_params.get('role')
    users = User.objects.all()
    if role:
        users = users.filter(role=role)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "manager":
            return Team.objects.filter(manager=user)
        return Team.objects.none()

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_members_view(request, team_id):
    members = TeamMember.objects.filter(team_id=team_id)
    serializer = TeamMemberSerializer(members, many=True)
    return Response(serializer.data)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Task.objects.filter(team__manager=user)
        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        if self.request.user.role not in ['manager', 'admin']:
            raise PermissionError("You do not have permission to create tasks.")
        serializer.save()

class UpdateListCreateView(generics.ListCreateAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['task']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['manager', 'admin']:
            return Update.objects.filter(task__team__manager=user)
        return Update.objects.filter(user=user)

    def perform_create(self, serializer):
        # Validate permissions are handled in serializer.validate
        serializer.save(user=self.request.user)


class UpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Update.objects.filter(user=self.request.user)

class UpdateViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateSerializer
    queryset = Update.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['task']

    def get_queryset(self):
        queryset = super().get_queryset()
        task_id = self.request.query_params.get('task')
        if task_id is not None:
            queryset = queryset.filter(task_id=task_id)
        return queryset
