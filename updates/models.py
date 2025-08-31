from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    @property
    def is_manager(self):
        return self.role == "manager"

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(
        CustomUser,
        related_name="managed_teams",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="team_memberships"
    )

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Update(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="updates"
    )
    feedback = models.TextField()
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="updates"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_completion = models.BooleanField(default=False)

    def __str__(self):
        return f"Update by {self.user.username} on {self.task.title}"
