from rest_framework import serializers
from .models import Policy, PolicyScrap


class PolicySerializer(serializers.ModelSerializer):
    schoolCd = serializers.StringRelatedField()
    jobCd = serializers.StringRelatedField()
    mrgSttsCd = serializers.StringRelatedField()
    regions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Policy
        fields = '__all__'

class PolicyScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyScrap
        fields = ('id', 'user', 'policy')
        read_only_fields = ('user',)