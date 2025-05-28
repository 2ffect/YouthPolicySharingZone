# chatbot/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatLog(models.Model):
    # 사용자별 대화 로그를 저장하며 최대 15개까지만 유지됨
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatlogs')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class UserProfileData(models.Model):
    # 신상정보를 따로 저장하여 사용자 맞춤형 응답에 활용
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_data')
    age = models.PositiveIntegerField(null=True)
    region = models.CharField(max_length=100, null=True)
    education = models.CharField(max_length=100, null=True)
    employment_status = models.CharField(max_length=100, null=True)
    marital_status = models.CharField(max_length=100, null=True)

    def is_complete(self):
        # 필수 신상정보가 모두 입력되었는지 확인
        return all([
            self.age,
            self.region,
            self.education,
            self.employment_status,
            self.marital_status
        ])

# ChatLog
# 유저별로 최대 15개의 대화만 유지되도록 설계 (뷰에서 FIFO 방식으로 삭제 구현 가능)

# UserProfileData 모델
# 필수 신상정보 필드(나이, 지역, 학력, 취업상태, 결혼상태) 저장.
# .is_complete() 메서드를 통해 정보가 모두 입력되었는지 확인 가능.
# 입력되지 않았다면 챗봇은 대화를 시작하지 않고 해당 정보를 먼저 요청.
