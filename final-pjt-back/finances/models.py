from django.db import models

# 예금 상품
class DepositProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=255)
    fin_co_no = models.CharField(max_length=255)
    kor_co_nm = models.CharField(max_length=255)

    def __str__(self):
        return self.fin_prdt_nm

# 예금 옵션
class DepositOption(models.Model):
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=50)
    fin_co_no = models.CharField(max_length=255)
    save_trm = models.IntegerField()
    intr_rate2 = models.FloatField()

    def __str__(self):
        return f'{self.fin_co_no} - {self.save_trm}개월'

# 적금 상품
class SavingProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=255)
    fin_co_no = models.CharField(max_length=255)
    kor_co_nm = models.CharField(max_length=255)

    def __str__(self):
        return self.fin_prdt_nm
    
# 적금 옵션
class SavingOption(models.Model):
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=50)
    fin_co_no = models.CharField(max_length=255)
    rsrv_type = models.CharField(max_length=255)
    rsrv_type_nm = models.CharField(max_length=255)
    save_trm = models.IntegerField()
    intr_rate2 = models.FloatField()

    def __str__(self):
        return f'{self.fin_co_no} - {self.save_trm}개월'

# 환율
class Exchange (models.Model):
    cur_unit = models.CharField(max_length=255)
    cur_nm = models.CharField(max_length=255)
    ttb = models.CharField(max_length=255)
    tts = models.CharField(max_length=255)
    deal_bas_r = models.CharField(max_length=255)
    bkpr = models.CharField(max_length=255)
    yy_efee_r = models.CharField(max_length=255)
    ten_dd_efee_r = models.CharField(max_length=255)
    kftc_deal_bas_r = models.CharField(max_length=255)
    kftc_bkpr = models.CharField(max_length=255)