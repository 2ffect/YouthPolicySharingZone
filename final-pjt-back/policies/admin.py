
from django.contrib import admin
from .models import (
    Policy,
    PolicyScrap,
)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('plcyNm', 'plcyNo', 'aplyYmD', 'schoolCd', 'jobCd')
    search_fields = ('plcyNm', 'plcyKywdNm')


@admin.register(PolicyScrap)
class PolicyScrapAdmin(admin.ModelAdmin):
    list_display = ('user', 'policy', )
    search_fields = ('user__username', 'policy__plcyNm')
