# chatbot/admin.py

from django.contrib import admin
from .models import ChatLog, UserProfileData

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'short_message', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__email', 'message')
    ordering = ('-created_at',)

    def short_message(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'


@admin.register(UserProfileData)
class UserProfileDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'region', 'education', 'employment_status', 'marital_status', 'is_complete')
    list_filter = ('region', 'education', 'employment_status', 'marital_status')
    search_fields = ('user__email', 'region', 'education', 'employment_status', 'marital_status')
