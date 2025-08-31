from rest_framework import serializers
from .models import CustomUser, Team, TeamMember, Task, Update
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_manager']

    def get_is_manager(self, obj):
        return obj.role == "manager"

class TeamSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'manager']

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), write_only=True)

    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'user_id', 'team', 'team_id']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(many=True, read_only=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='assigned_to'
    )
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), write_only=True, source='team'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'assigned_to_ids', 'team', 'team_id']

class UpdateSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        write_only=True,
        source='task'
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Update
        fields = ['id', 'task', 'task_id', 'feedback', 'user', 'is_completion', 'is_manager_feedback']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user if request else None
        if data.get('is_completion') and user and user.role not in ['manager', 'admin']:
            raise serializers.ValidationError('Only managers or admins can mark completion.')
        if data.get('is_manager_feedback') and user and user.role not in ['manager', 'admin']:
            raise serializers.ValidationError('Only managers or admins can post manager feedback.')
        return data

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
