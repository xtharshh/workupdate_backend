from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from .models import Update, Task, TeamMember
from .serializers import UpdateSerializer, TaskSerializer, TeamMemberSerializer

# -------------------------
# Authentication APIs
# -------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    user = request.user
    Token.objects.filter(user=user).delete()
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# -------------------------
# Project Management APIs
# -------------------------

class UpdateListCreateView(generics.ListCreateAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Update.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Update.objects.filter(user=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class TeamListView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamMember.objects.filter(team__members=self.request.user)


# -------------------------
# User Signup
# -------------------------
class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


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
            "token": token.key
        }, status=status.HTTP_201_CREATED)
