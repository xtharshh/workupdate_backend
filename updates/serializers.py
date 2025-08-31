from rest_framework import serializers
from .models import Team, TeamMember, Task, Update, CustomUser

class UserSerializer(serializers.ModelSerializer):
    is_manager = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_manager']
    def get_is_manager(self, obj):
        return obj.role == "manager"

class TeamSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True, source="manager"
    )
    class Meta:
        model = Team
        fields = ['id', 'name', 'manager', 'manager_id']

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), write_only=True, source="user"
    )
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), write_only=True, source="team"
    )
    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'user_id', 'team', 'team_id']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), write_only=True, source="team", required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'team', 'team_id', 'created_at']

class UpdateSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), write_only=True, source="task"
    )
    user = UserSerializer(read_only=True)

    class Meta:
        model = Update
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        user = self.context["request"].user
        # Only manager/admin can mark completion
        if data.get("is_completion") and user.role not in ["manager", "admin"]:
            raise serializers.ValidationError("Only managers or admins can complete a task.")
        return data
