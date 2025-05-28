from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime, timedelta
import requests, pytz, certifi

from .models import DepositProduct, DepositOption, SavingProduct, SavingOption, Exchange
from .serializers import DepositProductWithOptionsSerializer, SavingProductWithOptionsSerializer, ExchangeSerializer

from django.conf import settings
# Create your views here.
import certifi
print(certifi.where())


FINANCE_API_KEY = settings.FINANCE_API_KEY
EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

DEPOSIT_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SAVING_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
EXCHANGE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3/search'

# 예금 저장
@api_view(['GET'])
def save_deposit_data(request):
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(DEPOSIT_URL, params=params).json()
    base_list = response['result']['baseList']
    option_list = response['result']['optionList']

    for item in base_list:
        if DepositProduct.objects.filter(fin_prdt_cd=item['fin_prdt_cd']).exists():
            continue
        DepositProduct.objects.create(
            fin_prdt_cd=item['fin_prdt_cd'],
            fin_prdt_nm=item['fin_prdt_nm'],
            fin_co_no=item['fin_co_no'],
            kor_co_nm=item['kor_co_nm'],
        )

    for opt in option_list:
        try:
            product = DepositProduct.objects.get(fin_prdt_cd=opt['fin_prdt_cd'])
            DepositOption.objects.create(
                deposit_product=product,
                fin_prdt_cd=opt['fin_prdt_cd'],
                fin_co_no=opt['fin_co_no'],
                save_trm=int(opt['save_trm']),
                intr_rate2=float(opt['intr_rate2']) if opt.get('intr_rate2') else -1
            )
        except DepositProduct.DoesNotExist:
            continue

    return Response({'message': '정기예금 데이터 저장 완료'}, status=status.HTTP_200_OK)


# 적금 저장
@api_view(['GET'])
def save_saving_data(request):
    params = {
        'auth': FINANCE_API_KEY,
        'topFinGrpNo': '020000',
        'pageNo': 1
    }
    response = requests.get(SAVING_URL, params=params).json()
    base_list = response['result']['baseList']
    option_list = response['result']['optionList']

    for item in base_list:
        if SavingProduct.objects.filter(fin_prdt_cd=item['fin_prdt_cd']).exists():
            continue
        SavingProduct.objects.create(
            fin_prdt_cd=item['fin_prdt_cd'],
            fin_prdt_nm=item['fin_prdt_nm'],
            fin_co_no=item['fin_co_no'],
            kor_co_nm=item['kor_co_nm'],
        )

    for opt in option_list:
        try:
            product = SavingProduct.objects.get(fin_prdt_cd=opt['fin_prdt_cd'])
            SavingOption.objects.create(
                saving_product=product,
                fin_prdt_cd=opt['fin_prdt_cd'],
                fin_co_no=opt['fin_co_no'],
                rsrv_type=opt.get('rsrv_type', ''),
                rsrv_type_nm=opt.get('rsrv_type_nm', ''),
                save_trm=int(opt['save_trm']),
                intr_rate2=float(opt['intr_rate2']) if opt.get('intr_rate2') else -1
            )
        except SavingProduct.DoesNotExist:
            continue

    return Response({'message': '정기적금 데이터 저장 완료'}, status=status.HTTP_200_OK)

# 환율 저장
def get_search_date():
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    # 오전 11시 이전이면 하루 전 날짜
    target_date = now if now.hour >= 11 else now - timedelta(days=1)

    # 주말 보정: 토요일 또는 일요일의 경우, 직전 금요일 4로 맞춤
    while target_date.weekday() >= 5:  # 5: 토요일, 6: 일요일
        target_date -= timedelta(days=1)

    return target_date.strftime('%Y%m%d')


# 환율 정보 저장
@api_view(['GET'])
def save_exchange_data(request):
    params = {
        'authkey': EXCHANGE_API_KEY,
        # 'searchdate': get_search_date(),
        'searchdate': '20250526',
        'data': 'AP01',
    }
    # 전
    # 개발 환경에서 테스트를 위해 SSL 인증 해제하여 테스트 
    # response = requests.get(EXCHANGE_URL, params=params, verify=False)
    
    # 후
    # full_chain.pem 생성 후 이식 

    response = requests.get(EXCHANGE_URL, params=params, verify=settings.EXCHANGE_CERT_PATH)


    data = response.json()

    print("API 응답 데이터:", data)  # 실제 데이터 확인

    if not isinstance(data, list):
        return Response({'message': 'API 오류 또는 환율 정보 없음', 'raw': data}, status=status.HTTP_400_BAD_REQUEST)

    Exchange.objects.all().delete()

    success_count = 0
    for item in data:
        try:
            Exchange.objects.create(
                cur_unit=item.get('cur_unit', ''),
                cur_nm=item.get('cur_nm', ''),
                ttb=item.get('ttb', ''),
                tts=item.get('tts', ''),
                deal_bas_r=item.get('deal_bas_r', ''),
                bkpr=item.get('bkpr', ''),
                yy_efee_r=item.get('yy_efee_r', ''),
                ten_dd_efee_r=item.get('ten_dd_efee_r', ''),
                kftc_deal_bas_r=item.get('kftc_deal_bas_r', ''),
                kftc_bkpr=item.get('kftc_bkpr', ''),
            )
            success_count += 1
        except Exception as e:
            print(f"저장 에러: {e}, 데이터: {item}")

    return Response({'message': f'환율 데이터 저장 완료 ({success_count}건 저장됨)'}, status=status.HTTP_200_OK)


# 예금 데이터 가져오기 (상품명 + 옵션)
@api_view(['GET'])
def deposit_products(request):
    products = DepositProduct.objects.all()
    serializer = DepositProductWithOptionsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 적금 데이터 가져오기 (상품명 + 옵션)
@api_view(['GET'])
def saving_products(request):
    products = SavingProduct.objects.all()
    serializer = SavingProductWithOptionsSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 환율 정보 전체 조회
@api_view(['GET'])
def exchange_rates(request):
    exchanges = Exchange.objects.all()
    serializer = ExchangeSerializer(exchanges, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


###
# 예금 상품 리스트 조회 (은행 필터링 가능)
@api_view(['GET'])
def deposit_products(request):
    bank = request.GET.get('bank')
    if bank:
        products = DepositProduct.objects.filter(kor_co_nm=bank)
    else:
        products = DepositProduct.objects.all()
    serializer = DepositProductWithOptionsSerializer(products, many=True)
    return Response(serializer.data)

# 적금 상품 리스트 조회 (은행 필터링 가능)
@api_view(['GET'])
def saving_products(request):
    bank = request.GET.get('bank')
    if bank:
        products = SavingProduct.objects.filter(kor_co_nm=bank)
    else:
        products = SavingProduct.objects.all()
    serializer = SavingProductWithOptionsSerializer(products, many=True)
    return Response(serializer.data)

# 예금 + 적금 전체 은행 목록 조회
@api_view(['GET'])
def bank_list(request):
    deposit_banks = DepositProduct.objects.values_list('kor_co_nm', flat=True)
    saving_banks = SavingProduct.objects.values_list('kor_co_nm', flat=True)
    all_banks = sorted(set(deposit_banks).union(saving_banks))
    return Response({"banks": all_banks})

# 유튜브 영상 검색결과 가져오기
@api_view(['GET'])
def youtube_search(request):
    keyword = request.GET.get('q')
    if not keyword:
        return Response({'error': 'Missing keyword parameter'}, status=400)

    params = {
        'key': settings.YOUTUBE_API_KEY,  # 안전하게 관리됨
        'part': 'snippet',
        'type': 'video',
        'q': keyword,
        'maxResults': 15
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    return Response(response.json())