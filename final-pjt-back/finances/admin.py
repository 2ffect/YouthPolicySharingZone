from django.contrib import admin
from .models import (
    DepositProduct,
    DepositOption,
    SavingProduct,
    SavingOption,
    Exchange
)

@admin.register(DepositProduct)
class DepositProductAdmin(admin.ModelAdmin):
    list_display = ('fin_prdt_nm', 'fin_prdt_cd', 'fin_co_no', 'kor_co_nm')
    search_fields = ('fin_prdt_nm', 'fin_co_no', 'kor_co_nm')


@admin.register(DepositOption)
class DepositOptionAdmin(admin.ModelAdmin):
    list_display = ('deposit_product', 'fin_co_no', 'save_trm', 'intr_rate2')
    search_fields = ('fin_co_no', 'deposit_product__fin_prdt_nm')
    list_filter = ('save_trm',)


@admin.register(SavingProduct)
class SavingProductAdmin(admin.ModelAdmin):
    list_display = ('fin_prdt_nm', 'fin_prdt_cd', 'fin_co_no', 'kor_co_nm')
    search_fields = ('fin_prdt_nm', 'fin_co_no', 'kor_co_nm')


@admin.register(SavingOption)
class SavingOptionAdmin(admin.ModelAdmin):
    list_display = ('saving_product', 'fin_co_no', 'rsrv_type_nm', 'save_trm', 'intr_rate2')
    search_fields = ('fin_co_no', 'saving_product__fin_prdt_nm', 'rsrv_type_nm')
    list_filter = ('save_trm', 'rsrv_type')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('cur_unit', 'cur_nm', 'deal_bas_r', 'ttb', 'tts', 'bkpr')
    search_fields = ('cur_unit', 'cur_nm')
