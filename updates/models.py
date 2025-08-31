from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(CustomUser, related_name="managed_teams", on_delete=models.CASCADE)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(CustomUser, related_name="tasks")
    team = models.ForeignKey(Team, related_name="tasks", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    team = models.ForeignKey(Team, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="team_memberships", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"

class Update(models.Model):
    task = models.ForeignKey(Task, related_name="updates", on_delete=models.CASCADE)
    feedback = models.TextField()
    user = models.ForeignKey(CustomUser, related_name="updates", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completion = models.BooleanField(default=False)
    is_manager_feedback = models.BooleanField(default=False)

    def __str__(self):
        return f"Update by {self.user.username} on {self.task.title}"
