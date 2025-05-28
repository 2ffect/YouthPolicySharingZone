from django.urls import path
from . import views 

urlpatterns = [
  # API 호출로 예금 상품 정보 가져오기 + 저장 
  path('deposit-products/save/', views.save_deposit_data),
  # DB에 있는 예금 상품 리스트 호출
  path('deposit-products/', views.deposit_products),
  
  # API 호출로 적금 상품 정보 가져오기 + 저장 
  path('saving-products/save/', views.save_saving_data),
  # DB에 있는 예금 상품 리스트 호출
  path('saving-products/', views.saving_products),

  # API 호출로 환율 데이터 가져오기 + 저장
  path('exchange/save/', views.save_exchange_data),
  # DB에 있는 환율 데이터 호출
  path('exchange/', views.exchange_rates),

  # 예금 상품 가져오기
  path('deposit-products/', views.deposit_products),
  # 적금 상품 가져오기
  path('saving-products/', views.saving_products),
  # 은행명 가져오기
  path('banks/', views.bank_list),

  # 유브 영상 검색
  path('youtube/', views.youtube_search),
]
