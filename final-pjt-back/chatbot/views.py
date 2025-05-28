from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from openai import OpenAI
from django.db.models import Q
import json 

from policies.models import Policy, SchoolCode, JobCode, MaritalStatusCode, Region

from .models import ChatLog, UserProfileData

client = OpenAI(api_key=settings.CHATBOT_API_KEY)

# 신상정보 저장 / 반환
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def save_profile(request):
    user = request.user

    if request.method == 'GET':
        try:
            profile = UserProfileData.objects.get(user=user)
            return Response({
                'age': profile.age,
                'region': profile.region,
                'education': profile.education,
                'employment_status': profile.employment_status,
                'marital_status': profile.marital_status,
                'is_complete': profile.is_complete()  #
            }, status=200)
        except UserProfileData.DoesNotExist:
            return Response({'detail': '신상정보 없음', 'is_complete': False}, status=404)

    # POST 요청 시 신상정보 저장
    data = request.data
    profile, _ = UserProfileData.objects.get_or_create(user=user)
    profile.age = data.get('age')
    profile.region = data.get('region')
    profile.education = data.get('education')
    profile.employment_status = data.get('employment_status')
    profile.marital_status = data.get('marital_status')
    profile.save()

    return Response({'message': '신상정보가 저장되었습니다.'}, status=200)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot(request):
    user = request.user
    messages = request.data.get('messages', [])

    # 사용자 프로필 확인
    try:
        profile = UserProfileData.objects.get(user=user)
    except UserProfileData.DoesNotExist:
        return Response({'error': '신상정보가 등록되지 않았습니다. 먼저 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    if not profile.is_complete():
        return Response({'error': '신상정보가 완전하지 않습니다. 나이, 지역, 학력, 취업상태, 결혼상태를 모두 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    # 메시지 필터링
    filtered_messages = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        if role in ["user", "assistant"] and content:
            if isinstance(content, dict):
                content = json.dumps(content, ensure_ascii=False)
            filtered_messages.append({"role": role, "content": content})

    if not filtered_messages:
        return Response({'error': '메시지가 비어 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user_input = filtered_messages[-1]['content']
    ChatLog.objects.create(user=user, role='user', message=user_input)

    # 이전 assistant 응답 저장
    last_msg = messages[-1]
    if last_msg.get("role") == "assistant" and last_msg.get("content"):
        ChatLog.objects.create(user=user, role='assistant', message=last_msg["content"])

    # 15개 초과 로그 삭제
    logs = ChatLog.objects.filter(user=user).order_by('created_at')
    if logs.count() > 15:
        excess_ids = logs[:logs.count() - 15].values_list('id', flat=True)
        ChatLog.objects.filter(id__in=excess_ids).delete()

    # 코드값 → 사람이 읽을 수 있는 값으로 변환
    region_obj = Region.objects.filter(code=profile.region).first()
    region_display = region_obj.name if region_obj else "미입력"

    education_obj = SchoolCode.objects.filter(code=profile.education).first()
    education_display = education_obj.name if education_obj else "미입력"

    job_obj = JobCode.objects.filter(code=profile.employment_status).first()
    job_display = job_obj.name if job_obj else "미입력"

    marital_obj = MaritalStatusCode.objects.filter(code=profile.marital_status).first()
    marital_display = marital_obj.name if marital_obj else "미입력"

    # 정책 조건 필터 사전 정의
    SCHOOL_ANY = "0049010"
    JOB_ANY = "0013010"
    MARRIAGE_ANY = "0055003"

    base_filter = (
        (Q(schoolCd__code=profile.education) | Q(schoolCd__code=SCHOOL_ANY)) &
        (Q(jobCd__code=profile.employment_status) | Q(jobCd__code=JOB_ANY)) &
        (Q(mrgSttsCd__code=profile.marital_status) | Q(mrgSttsCd__code=MARRIAGE_ANY)) &
        Q(regions__code=profile.region)
    )

    # 금리혜택 우선 정책 필터 정의
    interest_filter = base_filter & Q(plcyKywdNm__icontains="금리혜택")
    other_filter = base_filter & ~Q(plcyKywdNm__icontains="금리혜택")

    interest_policies = Policy.objects.filter(interest_filter).distinct().values_list('plcyNm', flat=True)
    other_policies = Policy.objects.filter(other_filter).distinct().values_list('plcyNm', flat=True)

    has_policy = bool(interest_policies or other_policies)

    # 시스템 프롬프트 구성
    recommend_info = "추천할 정책이 있습니다." if has_policy else "추천할 수 있는 정책이 없습니다."
    profile_prompt = f"""
    당신은 사용자 맞춤형 정책 추천 및 질의 응답을 수행하는 챗봇입니다.
    사용자의 프로필을 참고하여, 정책 추천 또는 간단한 정책 관련 질문에 응답하세요.

    사용자 정보:
    - 나이: {profile.age}
    - 지역: {region_display}
    - 학력: {education_display}
    - 취업상태: {job_display}
    - 결혼여부: {marital_display}

    정책 필터 결과: {recommend_info}
    (이 결과는 추천 가능한 정책이 있는지를 사전에 판단한 것입니다.)

    [응답 규칙]
    당신의 응답은 다음 JSON 형식으로 구성되어야 합니다:

    {{
    "is_recommend": true 또는 false,
    "text": "실제 사용자에게 보여줄 응답 텍스트"
    }}

    응답 판단 기준:
    - 추천 가능한 정책이 있고, 사용자가 추천을 요청하거나 정책 조건에 맞는 질문을 한 경우 → "is_recommend": true
    - 정책 추천 외의 일반 대화(예: 인사, 잡담, 정의 설명, 특정 정책 조건 질문 등)는 → "is_recommend": false

    예시:
    - "내게 맞는 정책 알려줘" → true
    - "청년도약계좌 조건 알려줘" → false
    - "안녕 챗봇아" → false

    ⚠️ 반드시 위 JSON 형식으로만 응답하세요. JSON 이외의 설명은 절대 포함하지 마세요.
    """


    # GPT 응답 요청
    response = client.chat.completions.create(
        # model="gpt-4o-mini",
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": profile_prompt}] + filtered_messages
    )

    # 응답 파싱
    gpt_raw = response.choices[0].message.content
    try:
        parsed = json.loads(gpt_raw)
        is_recommend = parsed.get("is_recommend", False)
        text = parsed.get("text", "")
    except Exception:
        is_recommend = False
        text = gpt_raw

    # 응답 로그 저장
    ChatLog.objects.create(user=user, role='assistant', message=text)

    # 정책 추천 응답
    if has_policy and is_recommend:
        combined = list(interest_policies)[:2]
        if len(combined) < 2:
            combined += list(other_policies)[:2 - len(combined)]

        return Response({
            "type": "recommend",
            "reply": {
                "db_policies": combined,
                "gpt_supplement": text
            }
        }, status=status.HTTP_200_OK)


    # 일반 대화 응답
    return Response({
        "type": "text",
        "reply": text
    }, status=status.HTTP_200_OK)