# from django.core.management.base import BaseCommand
# from policies.views import fetch_all_keywords, get_or_create_code, SCHOOL_CD_MAP, JOB_CD_MAP, MRG_STTS_CD_MAP, REGION_MAP
# from policies.models import Policy, SchoolCode, JobCode, MaritalStatusCode, Region

# class Command(BaseCommand):
#     help = '외부 API로부터 전체 청년정책 데이터를 받아 DB에 저장합니다.'

#     def handle(self, *args, **kwargs):
#         policies = fetch_all_keywords()

#         if not policies:
#             self.stdout.write(self.style.ERROR('API 응답 실패'))
#             return

#         for p in policies:
#             school_code = p.get('schoolCd')
#             job_code = p.get('jobCd')
#             mrg_code = p.get('mrgSttsCd')

#             school_obj = get_or_create_code(SchoolCode, school_code, SCHOOL_CD_MAP.get(school_code, '기타'))
#             job_obj = get_or_create_code(JobCode, job_code, JOB_CD_MAP.get(job_code, '기타'))
#             mrg_obj = get_or_create_code(MaritalStatusCode, mrg_code, MRG_STTS_CD_MAP.get(mrg_code, '제한없음'))

#             policy, created = Policy.objects.get_or_create(
#                 plcyNo=p.get('plcyNo'),
#                 defaults={
#                     'plcyNm': p.get('plcyNm'),
#                     'plcyKywdNm': p.get('plcyKywdNm', ''),
#                     'plcyExplnCn': p.get('plcyExplnCn', ''),
#                     'plcySprtCn': p.get('plcySprtCn', ''),
#                     'aplyYmD': p.get('aplyYmd', ''),
#                     'schoolCd': school_obj,
#                     'jobCd': job_obj,
#                     'mrgSttsCd': mrg_obj,
#                 }
#             )

#             if created:
#                 zip_codes = p.get('zipCd', '')
#                 seen_regions = set()
#                 for code in zip_codes.split(','):
#                     prefix = code.strip()[:2]
#                     region_name = REGION_MAP.get(prefix)
#                     if region_name and region_name not in seen_regions:
#                         region_obj, _ = Region.objects.get_or_create(name=region_name)
#                         policy.regions.add(region_obj)
#                         seen_regions.add(region_name)

#         self.stdout.write(self.style.SUCCESS('정책 데이터 저장 완료'))


from django.core.management.base import BaseCommand
from policies.views import (
    fetch_all_keywords, get_or_create_code,
    SCHOOL_CD_MAP, JOB_CD_MAP, MRG_STTS_CD_MAP, REGION_MAP
)
from policies.models import Policy, SchoolCode, JobCode, MaritalStatusCode, Region


class Command(BaseCommand):
    help = '외부 API로부터 전체 청년정책 데이터를 받아 DB에 저장합니다.'

    def handle(self, *args, **kwargs):
        # 코드 사전 정규화
        for code, name in SCHOOL_CD_MAP.items():
            SchoolCode.objects.update_or_create(code=code, defaults={'name': name})

        for code, name in JOB_CD_MAP.items():
            JobCode.objects.update_or_create(code=code, defaults={'name': name})

        for code, name in MRG_STTS_CD_MAP.items():
            MaritalStatusCode.objects.update_or_create(code=code, defaults={'name': name})

        for code, name in REGION_MAP.items():
            Region.objects.update_or_create(code=code, defaults={'name': name})

        self.stdout.write(self.style.SUCCESS('✔ 모델 별 코드 사전 정규화 완료'))

        # 정책 데이터 fetch
        policies = fetch_all_keywords()
        if not policies:
            self.stdout.write(self.style.ERROR('API 응답 실패'))
            return

        # 정책 데이터 삽입
        for p in policies:
            # 복수 코드 처리 (쉼표로 들어올 수 있음 → 첫 번째 코드만 사용)
            school_code = (p.get('schoolCd') or '').split(',')[0].strip()
            job_code = (p.get('jobCd') or '').split(',')[0].strip()
            mrg_code = (p.get('mrgSttsCd') or '').split(',')[0].strip()

            school_obj = get_or_create_code(SchoolCode, school_code, SCHOOL_CD_MAP.get(school_code, '기타'))
            job_obj = get_or_create_code(JobCode, job_code, JOB_CD_MAP.get(job_code, '기타'))
            mrg_obj = get_or_create_code(MaritalStatusCode, mrg_code, MRG_STTS_CD_MAP.get(mrg_code, '제한없음'))

            policy, created = Policy.objects.get_or_create(
                plcyNo=p.get('plcyNo'),
                defaults={
                    'plcyNm': p.get('plcyNm'),
                    'plcyKywdNm': p.get('plcyKywdNm', ''),
                    'plcyExplnCn': p.get('plcyExplnCn', ''),
                    'plcySprtCn': p.get('plcySprtCn', ''),
                    'aplyYmD': p.get('aplyYmd', ''),
                    'schoolCd': school_obj,
                    'jobCd': job_obj,
                    'mrgSttsCd': mrg_obj,
                }
            )

            # zipCd 기준 region 연결
            if created:
                zip_codes = p.get('zipCd', '')
                seen_regions = set()
                for code in zip_codes.split(','):
                    prefix = code.strip()[:2]
                    region_name = REGION_MAP.get(prefix)
                    if region_name and region_name not in seen_regions:
                        region_obj = Region.objects.get(name=region_name)
                        policy.regions.add(region_obj)
                        seen_regions.add(region_name)

        self.stdout.write(self.style.SUCCESS('✔ 정책 데이터 저장 완료'))
