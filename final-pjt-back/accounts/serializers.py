# accounts/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from django.contrib.auth import authenticate


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    birthdate = serializers.DateField(required=True)
    phonenum = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)

    def get_cleaned_data(self):
        data =  super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname')
        data['birthdate'] = self.validated_data.get('birthdate')
        data['phonenum'] = self.validated_data.get('phonenum')
        data['gender'] = self.validated_data.get('gender')
        return data
    

    def save(self,request):
        
        adapter = get_adapter()
        user = adapter.new_user(request)
        # user = super().save(request)
        self.cleaned_data = self.get_cleaned_data()
        print(self.cleaned_data)
        

        user.nickname = self.cleaned_data.get('nickname')
        user.birthdate = self.cleaned_data.get('birthdate')
        user.phonenum = self.cleaned_data.get('phonenum')
        user.gender = self.cleaned_data.get('gender')
        adapter.save_user(request, user, self)
        return user

# username 대신 email을 사용하여 로그인하기 위해 serializer 커스텀
class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            
            
            # authenticate()는 기본적으로 username을 가지고 로그인함
            # 이메일로 로그인 시키고 싶음 -> email로 해당 user의 username을 찾아서 넘겨와서 로그인
            
            
            if not user:
                raise serializers.ValidationError("이메일 또는 비밀번호가 올바르지 않습니다.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해주세요")

# user페이지 - 회원정보 출력, 수정용 시리얼라이저

class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'email', 'username', 'birthdate','gender')
