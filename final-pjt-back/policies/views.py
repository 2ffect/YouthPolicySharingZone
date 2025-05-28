from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import json
import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SchoolCode, JobCode, MaritalStatusCode, Policy, Region, PolicyScrap
from .serializers import PolicySerializer, PolicyScrapSerializer
# Create your views here.
SCHOOL_CD_MAP = {
    "0049001": "고졸 미만",
    "0049002": "고교 재학",
    "0049003": "고졸 예정",
    "0049004": "고교 졸업",
    "0049005": "대학 재학",
    "0049006": "대졸 예정",
    "0049007": "대학 졸업",
    "0049008": "석·박사",
    "0049009": "기타",
    "0049010": "제한없음",
}

JOB_CD_MAP = {
    "0013001": "재직자",
    "0013002": "자영업자",
    "0013003": "미취업자",
    "0013004": "프리랜서",
    "0013005": "일용근로자",
    "0013006": "(예비)창업자",
    "0013007": "단기근로자",
    "0013008": "영농종사자",
    "0013009": "기타",
    "0013010": "제한없음",
}

MRG_STTS_CD_MAP = {
    "0055001": "기혼",
    "0055002": "미혼",
    "0055003": "제한없음",
}

REGION_MAP = {
    '11': '서울특별시',
    '26': '부산광역시',
    '27': '대구광역시',
    '28': '인천광역시',
    '29': '광주광역시',
    '30': '대전광역시',
    '31': '울산광역시',
    '36': '세종특별자치시',
    '41': '경기도',
    '51': '강원도',
    '43': '충청북도',
    '44': '충청남도',
    '52': '전라북도',
    '46': '전라남도',
    '47': '경상북도',
    '48': '경상남도',
    '50': '제주특별자치도',
}

KEYWORD_MAP = {
    'finance': '금리',
    'global': '해외',
    'job': '취업',
}

# 외부 api요청 -> 데이터 가져오기
def fetch_policy_data(keyword):
    url = "https://www.youthcenter.go.kr/go/ythip/getPlcy"
    params = {
        'apiKeyNm': settings.POLICY_API_KEY,
        'plcyKywdNm': keyword,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'API 호출 실패 ({keyword})')
        return None

# 여러 키워드 한번에 요청
def fetch_all_keywords():
    keyword_list = ['금리', '해외', '취업']
    all_policies = []

    for kw in keyword_list:
        res = fetch_policy_data(kw)
        if res:
            all_policies.extend(res.get('result', {}).get('youthPolicyList', []))

    return all_policies

def get_or_create_code(model, code, name):
    return model.objects.get_or_create(code=code, defaults={"name": name})[0]


# 키워드 별로 필터링해서 조회
@api_view(['GET'])
def filter_policies(request, keyword):
    keyword = KEYWORD_MAP.get(keyword.strip().lower())
    filtered = Policy.objects.filter(plcyKywdNm__icontains=keyword)
    serializer = PolicySerializer(filtered, many=True)
    return Response(serializer.data)

# 단일 정책 조회 -> get 요청은 비로그인 사용자도 가능하게 하려고 분리
@api_view(['GET'])
def policy_detail(request,policy_id):
    # policy = Policy.objects.get(plcyNo=policy_id)
    policy = Policy.objects.get(id=policy_id)
    serializer = PolicySerializer(policy)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

# 단일 정책 스크랩, 스크랩취소
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def scrap_policy(request, policy_id):
    if request.method == 'POST':
        serializer = PolicyScrapSerializer(data={'policy': policy_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        policy = PolicyScrap.objects.filter(user=request.user, policy=policy_id)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# isScrapped 확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_policy_scrapped(request, policy_id):
    exists = PolicyScrap.objects.filter(user=request.user, policy_id=policy_id).exists()
    return Response({'is_scrapped': exists}, status=status.HTTP_200_OK)

