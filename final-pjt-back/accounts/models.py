from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('F', '여성'),
    ]
    # 추가 항목
    # nickname
    # phonenum
    # birthdate
    # 성별
    nickname = models.CharField(max_length=20, unique=True) # 중복허용x
    birthdate = models.DateField()
    phonenum = models.CharField(max_length=11)  
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )
    # 기본 항목
    # username(이름) -> 중복 허용
    username = models.CharField(('username'), max_length=150)
    # password1
    # password2
    # email -> 중복 불가
    email = models.EmailField(('email address'), unique=True)
    
    USERNAME_FIELD = 'email'    # email로 로그인 할 것
    REQUIRED_FIELDS = ['username', 'nickname', 'birthdate', 'phonenum', 'gender']
    
    def __str__(self):
        return self.email