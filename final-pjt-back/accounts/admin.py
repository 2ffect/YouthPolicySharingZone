from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 관리자 페이지에서 보이는 필드
    list_display = ('email', 'username', 'nickname', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'gender')
    search_fields = ('email', 'username', 'nickname')
    ordering = ('email',)

    # 필드 그룹 정의
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'nickname', 'birthdate', 'phonenum', 'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # 유저 생성 시 사용되는 필드
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'nickname', 'birthdate', 'phonenum', 'gender', 'password1', 'password2'),
        }),
    )

