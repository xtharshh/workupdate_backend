from django.contrib import admin
from .models import CustomUser, Team, TeamMember, Task, Update

# Register CustomUser with default admin
admin.site.register(CustomUser)

# Register Team with default admin
admin.site.register(Team)

# Register TeamMember with default admin
admin.site.register(TeamMember)

# Register Task with default admin
admin.site.register(Task)

# Custom admin registration for Update model
@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'feedback', 'created_at')
    list_filter = ('user', 'task', 'created_at')
    search_fields = ('feedback', 'user__username', 'task__title')
