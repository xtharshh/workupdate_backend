from django.contrib import admin
from .models import Update, TeamMember, Task

# Custom admin for Update
@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'feedback', 'created_at')  # only existing fields
    list_filter = ('user', 'task', 'created_at')
    search_fields = ('feedback', 'user__username', 'task__title')

# Register the rest normally
admin.site.register(TeamMember)
admin.site.register(Task)
