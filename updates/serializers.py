from rest_framework import serializers
from .models import Team, TeamMember, Task, Update
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'manager']

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'team']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'team', 'created_at', 'completed']

class UpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # user will be set from the request
    # No task field since Flutter sends title/details
    class Meta:
        model = Update
        fields = ['id', 'title', 'details', 'user', 'created_at']
