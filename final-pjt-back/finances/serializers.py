from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, Exchange
from rest_framework import serializers

# 예금
# 예금 옵션 정보만 반환 (상품 내부에서 사용)
class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = ('save_trm', 'intr_rate2')

# 예금 상품 + 해당 옵션 목록을 함께 반환 (조회용)
class DepositProductWithOptionsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField() # 커스텀 필드로 옵션 연결

    class Meta:
        model = DepositProduct
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'fin_co_no', 'kor_co_nm', 'options')

    def get_options(self, obj):
        options = DepositOption.objects.filter(deposit_product=obj)
        return DepositOptionSerializer(options, many=True).data

# 적금
# 적금 옵션 정보만 반환 (상품 내부에서 사용)
class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = ('save_trm', 'rsrv_type', 'rsrv_type_nm', 'intr_rate2')

# 적금 상품 + 해당 옵션 목록을 함께 반환 (조회용)
class SavingProductWithOptionsSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = SavingProduct
        fields = ('fin_prdt_cd', 'fin_prdt_nm', 'fin_co_no', 'kor_co_nm', 'options')

    def get_options(self, obj):
        options = SavingOption.objects.filter(saving_product=obj)
        return SavingOptionSerializer(options, many=True).data

# 환율
class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

