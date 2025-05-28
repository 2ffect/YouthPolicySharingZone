from django.db import models
from django.conf import settings

# 자격학력 코드 모델
class SchoolCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)  # 예: "대학 졸업"

    def __str__(self):
        return self.name

# 취업 상태 코드 모델
class JobCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)  # 예: "재직자"

    def __str__(self):
        return self.name


# 결혼 상태 코드 모델
class MaritalStatusCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)  # 예: "미혼"

    def __str__(self):
        return self.name


# 지역 (zipCd 앞 두자리 기준)
class Region(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# 정책 모델
class Policy(models.Model):
    plcyNo = models.CharField(max_length=255)
    plcyNm = models.CharField(max_length=255)
    plcyKywdNm = models.CharField(max_length=255)
    plcyExplnCn = models.TextField()
    plcySprtCn = models.TextField()
    aplyYmD = models.CharField(max_length=255)

    schoolCd = models.ForeignKey(SchoolCode, on_delete=models.SET_NULL, null=True)
    jobCd = models.ForeignKey(JobCode, on_delete=models.SET_NULL, null=True)
    mrgSttsCd = models.ForeignKey(MaritalStatusCode, on_delete=models.SET_NULL, null=True)

    regions = models.ManyToManyField(Region, blank=True)

    def __str__(self):
        return self.plcyNm


# 스크랩 기능
class PolicyScrap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
