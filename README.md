
<!-- no toc -->
# <img src="./readme_img/favicon.png" alt="logo" width="100" style="vertical-align: middle;" /> <span style="font-size: 2.5rem; vertical-align: middle;">청정구역</span>

청년을 위한 정책, 금융 정보, 커뮤니티 서비스를 통합한 웹 플랫폼입니다.  
Vue 3와 Django를 기반으로 제작되었으며, 실제 외부 API와 챗봇 기능을 통합하여 실질적인 금융/정책 정보를 제공합니다.

---
<!-- no toc -->
### 목차
1. [팀원 정보 및 업무 분담 내역](#팀원-정보-및-업무-분담-내역)
2. [프로젝트 기술 정보](#프로젝트-기술-정보)
3. [디자인 목업 및 데이터 베이스 모델링(ERD)](#디자인-목업-및-데이터-베이스-모델링erd)
4. [정책 추천 알고리즘에 대한 기술적 설명](#정책-추천-알고리즘에-대한-기술적-설명)
5. [서비스 대표 기능들에 대한 설명](#서비스-대표-기능들에-대한-설명)
6. [생성형 AI를 활용한 부분](#생성형-ai를-활용한-부분)
7. [프로젝트 개요](#프로젝트-개요)
8. [기타](#기타)

<br>

## 팀원 정보 및 업무 분담 내역
- 프로젝트 기간 : 2025/5/22 ~ 2025/5/27 (약 6일)

| 이름         | 역할 및 구현 기능                                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 오승연 (팀장) | **Back-end** - 회원가입 / 로그인아웃 / 마이페이지 <br> **Front-end** - 커뮤니티 CRUD / 청년정책 / 환율 <br> **Full-stack** - 게시글 스크랩 / 정책 스크랩 / 청년센터찾기(카카오 MAP API) |
| 김재희 (팀원) | **Back-end** - 커뮤니티 CRUD / 청년정책(청년정책API) / 환율 <br> **Front-end** - 회원가입 / 로그인아웃 / 마이페이지 <br> **Full-stack** - 댓글 / 금융상품(금융감독원 예금/적금 API) / 챗봇(OPENAI API)               |
<br>

## 프로젝트 기술 정보
<!-- no toc -->
### 💻 Frontend
- JavaScript                    - Language
- Vue 3
- Vue Router                    - 페이지 라우팅
- Pinia                         - 상태관리
- Pinia Plugin Persisted State  - 로컬스토리지 상태 유지
- Axios                         - 비동기 HTTP 통신
- Vite                          - 고속 빌드/개발 서버
- Vite Plugin Vue / Devtools
<!-- no toc -->
### 🖥 Backend
- Python                        - Language
- Django 4.2
- Django REST Framework         - API 구축
- Django 기본 인증                -  TokenAuthentication 기반 커스텀
- drf-yasg                      - Swagger 기반 API 문서 자동화
- django-cors-headers           - CORS 정책 설정
- django-environ                - `.env` 기반 환경설정 관리
<!-- no toc -->
### 🧪 기타
- requests / PyYAML

<!-- no toc -->
### 🌐 사용된 외부 API

| API 이름                | 설명                                 | 환경변수 키           |
|-------------------------|--------------------------------------|------------------------|
| 금융감독원 예금/적금 API | 금융 상품(정기예금, 적금 등) 정보 제공 | `FINANCE_API_KEY`      |
| 한국수출입은행 환율 API  | 실시간 환율 정보 조회                 | `EXCHANGE_API_KEY`     |
| 청년정책 API             | 청년 대상 정책 정보 검색              | `POLICY_API_KEY`       |
| YouTube 검색 API        | 영상 콘텐츠 검색 및 출력              | `YOUTUBE_API_KEY`      |
| OpenAI GPT API          | 챗봇 응답 생성                        | `CHATBOT_API_KEY`      |
<!-- no toc -->
### ⚙️ 로컬 실행 방법
<!-- no toc -->
#### 🔹 Frontend (Vue 3)
```bash
cd front
npm install
npm run dev
```
<!-- no toc -->
#### 🔹 Backend (Django)
```bash
cd back
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py fetch_policies # policy data crawling + normalization
python manage.py loaddata accounts.json articles.json comments.json # 필요시 더미데이터 삽입
python manage.py runserver
```
<!-- no toc -->
### 📁 프로젝트 구조
<details>
<summary>프로젝트 구조 트리</summary>

<pre>
project/
├── back/                       # Django Backend
│   ├── accounts/               # 회원가입 및 사용자 인증 처리
│   ├── articles/               # 커뮤니티 데이터 처리
│   ├── chatbot/                # 챗봇 대화 및 추천 시스템
│   ├── finances/               # 금융 상품 데이터 처리
│   ├── policies/               # 정책 데이터 처리
│   ├── finproject/             # 프로젝트 루트
│   ├── settings.py             # 기타 설정 파일
│   └── manage.py
│
├── front/                      # Vue 3 Frontend
│   ├── public/                 # 정적 자산
│   ├── src/
│   │   ├── components/         # UI 컴포넌트
│   │   ├── router/             # Vue Router 설정
│   │   ├── stores/             # Pinia 상태 관리 모듈
│   │   ├── views/
│   │   │   ├── Chatbot/        # 챗봇 UI 및 프로필
│   │   │   ├── Community/      # 게시글 생성/조회/수정/상세 페이지
│   │   │   ├── Policy/         # 정책 관련 페이지 및 하위 금융 상품
│   │   │   │   ├── Finance/    # 예금, 적금, 환율 등 금융 정보
│   │   │   └── UserPage/       # 로그인, 회원가입, 마이페이지 관련
│   │   ├── App.vue             # 루트 컴포넌트
│   │   └── main.js
│
├── .env.example                # 환경 변수 예시 파일
└── README.md                   # 프로젝트 설명 문서
</pre>

</details>
<br>

## 디자인 목업 및 데이터 베이스 모델링(ERD)
<!-- no toc -->
### 🎨 디자인 목업
<img src="./readme_img/figma.png" alt="figma" style="vertical-align: middle;" />

<!-- no toc -->
### 📊 ERD
[**ERD dbdiagram.io Link**](https://dbdiagram.io/d/청정구역-ERD-683480c96980ade2eb720192)
<img src="./readme_img/erd.png" alt="figma" style="vertical-align: middle;" />

<!-- no toc -->
### API 명세서

<details>
<summary>accounts 명세서</summary>
<img src="./readme_img/accounts_api.png" alt="figma" style="vertical-align: middle;" />
</details>

<br>

<details>
<summary>chatbot 명세서</summary>
<img src="./readme_img/chatbot_api.png" alt="figma" style="vertical-align: middle;" />
</details>

<br>

<details>
<summary>community 명세서</summary>
<img src="./readme_img/community_api.png" alt="figma" style="vertical-align: middle;" />
</details>

<br>

<details>
<summary>finances 명세서</summary>
<img src="./readme_img/finances_api.png" alt="figma" style="vertical-align: middle;" />
</details>

<br>

<details>
<summary>policy 명세서</summary>
<img src="./readme_img/policy_api.png" alt="figma" style="vertical-align: middle;" />
</details>

## 정책 추천 알고리즘에 대한 기술적 설명
사용자 신상정보 기반 정책 필터링(DB 쿼리)과 GPT의 자연어 분기(정책 추천 vs 일반 대화)를 결합합니다.
정책 추천의 정밀도는 DB의 코드값 매칭(AND/OR 조합)과 금리혜택 우선 순위, 그리고 GPT의 대화 의도 분류에 의해 결정됩니다.

1. 사용자 프로필 정보 확인 및 검증
  - 로그인한 사용자의 신상정보(나이, 지역, 학력, 취업상태, 결혼상태)를 가져옵니다.
  - 프로필이 없거나 필수 정보가 모두 입력되지 않은 경우, 정책 추천을 진행하지 않고 정보 입력을 유도합니다.

2. 정책 추천을 위한 조건 필터링
  - 정책 추천은 다음과 같은 OR/AND 조건으로 필터링됩니다.
    - 사용자의 학력 코드 또는 '전체 학력'(SCHOOL_ANY)
    - 사용자의 직업 코드 또는 '전체 직업'(JOB_ANY)
    - 사용자의 결혼상태 코드 또는 '전체 결혼상태'(MARRIAGE_ANY)
    - 이 조건을 Q 객체로 조합하여, 사용자에게 적용 가능한 정책만 필터링합니다.

3. 금리혜택 정책 우선 추천
  - 정책 중 plcyKywdNm(정책 키워드명)에 "금리혜택"이 포함된 정책을 우선적으로 추천합니다.
  - 금리혜택 정책이 없으면, 기타 정책을 추천 대상으로 합니다.

4. 추천 정책 후보 선정 
  - 필터링한 정책 중, 금리혜택 정책 2개를 우선 추천합니다.
  - 부족할 경우 기타 정책에서 최대 2개까지 보충합니다.
  - 정책명만 리스트로 추출하여 응답에 포함시킵니다.

5. 시스템 프롬프트 및 GPT 분기
  - 시스템 프롬프트에 사용자 프로필과 정책 추천 가능 여부를 요약해서 사용자의 입력 메시지와 함께 GPT에게 전달합니다.
  - 추천이 필요한 상황인지(예: "내게 맞는 정책 알려줘") 판단하도록 합니다.
  - GPT의 응답은 반드시 { "is_recommend": true/false, "text": "..." }의 JSON 형식이 되도록 강제합니다.

6. 최종 응답 분기 및 반환
  - is_recommend: true로 판단하고, 실제 추천 정책이 존재하면 추천 정책명 리스트와 GPT 보조 설명을 함께 반환합니다.
  - is_recommend: false로 판단한다면 일반 대화 응답으로 반환합니다.


## 서비스 대표 기능들에 대한 설명


### 1. 메인 페이지
<details>
<summary>메인페이지 화면 보기</summary>


- **비로그인 사용자**
  - 챗봇 안내 및 간편한 서비스 소개 제공  
  - 인증된 사용자에게만 챗봇의 정책 추천 기능을 제공하고자 로그인 완료 여부에 따라 다른 챗봇 화면을 제공하였습니다.
    ![비로그인 메인](./readme_img/mainpage/unloginmain_widechatbot.png)

- **로그인 사용자**
  - 챗봇 기능과 사용자 맞춤 서비스 활성화  
    ![로그인 메인](./readme_img/mainpage/login_mainpage.png)

- **챗봇**
  - 사용자 신상 정보 및 정책 DB 기반 추천
  - 사용자에 적합한 정책을 추천하고자 사용자의 신상정보를 입력받아 DB에 저장하였습니다. 해당 선택지를 기반으로 추천 서비스를 제공하였습니다.
    ![챗봇 신상정보](./readme_img/mainpage/chatbot_startpage.png)
    ![챗봇 메인](./readme_img/mainpage/mainpage_chatbot.png)
</details>

### 2. 회원가입 및 로그인
<details>
<summary>회원가입 및 로그인 화면 보기</summary>

- **회원가입 화면**  
  - dj-rest-auth에서 제공하는 기본 로그인의 경우, username을 사용하지만, 
  username에 실명을 사용하고자 중복을 허용하고, 이메일을 활용하여 로그인 할 수 있도록 User 모델을 수정하였습니다.
  - 이메일 형식(@)을 만족하는가, 비밀번호의 경우 최소 8자 이상을 만족하는가, 전화번호가 11자리를 넘기지 않는가 등 유효성 검사를 진행하였습니다.
  ![회원가입](./readme_img/authpage/signup_wo_navbar.png)

- **로그인 화면**  
  ![로그인](./readme_img/authpage/login.png)
</details>

### 3. 마이페이지
<details>
<summary>마이페이지 화면 보기</summary>

- **회원정보 수정**  
  - disabled를 사용하여 이메일, 이름, 생년월일, 성별을 제외한 닉네임, 전화번호에 대한 수정만 가능하도록 하였습니다.
  ![회원정보 수정](./readme_img/mypage/mypage_updateuserinfo.png)

- **비밀번호 변경**  
  ![비밀번호 변경](./readme_img/mypage/password_update.png)

- ManyToMany 필드 관계를 통해 사용자가 스크랩한 정책/게시글을 마이페이지에서 확인하고, 스크랩한 정책/게시글 클릭 시 해당 정책 디테일로 이동가능하도록 하였습니다.
- **스크랩한 정책 확인**  
  ![스크랩 정책](./readme_img/mypage/mypage_scrappedpolicy.png)

- **스크랩한 게시글 확인**  
  ![스크랩 게시글](./readme_img/mypage/mypage_scrappedarticle.png)
</details>

### 4. 청년 정책 및 금융 정보
<details>
<summary>청년 정책 및 금융 정보 화면 보기</summary>

- 외부 API 요청을 통해 청년 대상 다양한 정책들에 대한 데이터를 수집하였습니다. 시행 정책명, 정책 번호, 대상(학력, 재직, 결혼 여부), 신청 기간, 상세내용을 제공합니다.

- **우대 금융 정책 메인**  
  ![정책 메인](./readme_img/policy/policymain.png)

- **예/적금 정보**
  - 실시간 정보를 제공합니다. 
  요청과 응답에 걸리는 시간에 대해 사용자 경험을 개선하고자 스피너를 제공하였습니다.  
    ![로딩 화면](./readme_img/policy/deposit_loading.png)

  - 예금 리스트 및 상세 페이지  
    - 필터링을 통해 각 은행 별 상세 정보를 제공합니다.
    ![예금 리스트](./readme_img/policy/depositlist.png)  
    ![예금 상세](./readme_img/policy/deposit_detail.png)

  - 적금 상세 페이지  
    - 예금 상품과 마찬가지로 각 은행에 대한 필터링 기능을 제공하며, 정액정립식, 자유적립식의 카테고리 별로 정보를 구분하여 확인할 수 있습니다.
    ![적금 상세1](./readme_img/policy/saving_detail.png)  
    ![적금 상세2](./readme_img/policy/saving_detail2.png)

- **관심 종목 검색 (유튜브 연동)**  
  - 관심 종목 검색 시, 관련 유튜브 영상 목록을 제공하였습니다. 각 목록 클릭 시, 해당 영상 url로 이동가능하도록 설정하였습니다.
  ![관심 종목 검색](./readme_img/policy/stockinfo.png)

- **청년 취업 정책**  
  ![취업 정책](./readme_img/policy/jobpolicymain.png)

- **청년 해외 정책**  
  ![해외 정책](./readme_img/policy/globalpolicymain.png)

- **환율 계산기**  
  - 기준 환율, 송금 받을 때, 송금 보낼 때의 옵션 별 환율 계산 기능을 제공합니다.
  ![환율 계산기](./readme_img/policy/exchangecalculator.png)  
  ![환율 결과1](./readme_img/policy/exchangecal_detail1.png)  
  ![환율 결과2](./readme_img/policy/exchangecal_detail2.png)
</details>

### 5. 청년 센터 검색
<details>
<summary>청년 센터 검색 화면 보기</summary>

- 현 위치 정보를 제공받아, 현 위치로부터 가까운 거리 순으로 정렬하여 위치정보를 제공합니다.
  ![센터 검색](./readme_img/centersearch/centersearch_main.png)  
  ![센터 예시](./readme_img/centersearch/centersearch_example2.png)
</details>


### 6. 커뮤니티 기능
<details>
<summary>커뮤니티 화면 보기</summary>

- 커뮤니티 게시글의 C,R,U,D, 댓글의 C,D 를 구현하였습니다.
  요청 사용자 정보를 확인하여 직접 작성한 게시글의 경우 수정, 삭제 버튼을 제공하고,
  스크랩 유무 여부를 확인하여 스크랩 버튼을 각각 다르게 출력하였습니다.
- 인증된 사용자에게만 제공되는 기능으로, 비로그인 시 해당 경로로 접속하지 못하도록 차단하였습니다.
- **커뮤니티 메인**  
  ![커뮤니티 메인](./readme_img/article/communitymain.png)

- **게시글 작성**  
  ![게시글 작성](./readme_img/article/create_article.png)

- **게시글 수정/삭제**  
  ![게시글 관리](./readme_img/article/my_article_update_delete.png)  
  ![게시글 수정](./readme_img/article/article_update.png)

- **댓글 작성**  
  ![댓글 작성](./readme_img/article/article_comment.png)

- **스크랩 기능**
  - 게시글 스크랩  
    ![스크랩 게시글 상세](./readme_img/mypage/scrapped_article_detail.png)
  - 정책 스크랩  
    ![스크랩 정책 상세](./readme_img/mypage/scrapped_policy_detail.png)
</details>


## 생성형 AI를 활용한 부분
1. **챗봇 - 정책 추천 알고리즘**
    - openAI API 프롬프트 엔지니어링을 GPT는 사용자 프로필 정보와 입력 문장을 바탕으로, 정책 추천 요청인지 일반 대화인지를 판단하고, 정책 추천이 필요한 경우에는 추천 설명 문구를 생성해줍니다.
  모든 응답은 { "is_recommend": true/false, "text": "..." } 형태의 일관된 JSON 포맷으로 반환되어 프론트엔드 또는 후속 처리 로직과의 정확한 인터페이스를 보장합니다.
2. **더미데이터 생성**
    - 개발 및 테스트 편의를 위해 사용자, 게시글, 댓글 등의 더미 데이터를 생성형 AI(GPT)를 활용해 자동 생성하였습니다.
  현실적인 문장 구성과 다양한 패턴의 콘텐츠를 빠르게 확보함으로써,
  UI/UX 테스트 및 기능 검증 과정에서 더 높은 몰입도와 신뢰성을 확보할 수 있었습니다.

## 프로젝트 개요
### 프로젝트 배경
  ![프로젝트 배경](./readme_img/프로젝트%20배경.png)
- 청년정책 예산이 2021년 전체 정부 예산의 4.27%에서 2024년 4.12%로 감소
- 지난 4년 동안 정부 예산은 5.6% 증가한 반면 청년정책 예산은 오히려 1.2% 감소
- 청년 정책의 인지도는 일부 정책에서 40% 이상이지만, 실제 수혜율은 대부분 10% 이하
- 정책의 실질적 효과가 저하되어 국가·지자체의 재정 낭비가 원인

### 프로젝트 목적
1. 청년정책 통합 안내 및 정보 접근성 향상
2. 청년 정책 인지도 및 수혜율 증가
3. 복지 사각지대 해소

### 기대 효과
1. 국가/지자체 재정 효율성 제고
  - 투입된 예산이 실제 수요자에게 효과적으로 전달되어 재정 낭비가 줄어듬
2. 사회적 형평성 강화
  - 정보 취약계층, 지방 거주 청년 등 소외된 집단도 정책 혜택을 받을 수 있어 사회적 형평성이 강화됨
3. 정책 설계 및 개선의 선순환 구조 구축
  - 실제 정책 이용 데이터와 피드백 축적으로 향후 정책 설계와 개선에 반영
  - 청년 중심의 정책 거버넌스가 활성화로 청년 수요에 맞는 정책 개발 촉진

## 기타
### Known Error
- **Exchange.vue** : onMounted로 외부 api 요청, DB 조회 요청 동시 호출 시 watch / computed 를 사용했으나 새로고침을 해야 반영되는 문제

### Unknown Error
- **한국수출입은행 API 호출 시** : SSL 인증서 관련 문제 발생 -> full_chain.pem 생성 하여 setting.py 이식 -> OSError 발생 -> requests 가 신뢰 가능한 certifi\cacert.pem 활용 -> 간헐적 에러 발생중

### 향후 계획
- Known/Unknown Error 처리
- 외부 API 응답 데이터 정규화
- 금융감독원 API 조회 시 마다 호출 -> 적정 시간 간격으로 자동 호출 (DB 기반 데이터 활용)
- 스크랩 된 정책 토큰 분석을 통한 정밀 추천이 가능하도록 챗봇 개선
- 서버 배포!!!


### 느낀점 & 후기

| 이름         | 느낀점 & 후기                                                                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 오승연 (팀장) |  한 학기 동안 공부해온 것들을 활용하여 적용해 볼 수 있어 좋았습니다. 프로젝트 과정에서 기획이 가장 중요하다는 점을 뼈저리게 느낄 수 있었습니다. 기간이 임박해 마음이 급했지만, 찬찬히 요구사항부터 정리해나가며 진행해 갔었기에 진행 과정에서 덜 헤맬 수 있었던 것 같습니다. <br> 짧은 기간이었지만 웹 페이지를 만들어낼 수 있었다는 점이 정말 뿌듯했고, 진행 과정을 명료하게 정리해주었던 팀원에게 감사합니다. 좋은 파트너와 함께하게 되어 운이 아주 좋았던 것 같아요 짱~! |
| 김재희 (팀원) |싸피를 시작하기 전, 프로젝트라고 하면 잔뜩 긴장부터 했었는데 어느덧 이만큼 성장해 좋은 파트너와 함께 구상부터 실제 페이지 구축까지 막힘없이 계획하고 개발했던 모습을 돌아보니 한 학기의 과정이 힘들고 피곤하긴 했지만 엄청나게 체득했다고 느꼈던 아주 값진 경험이었습니다. <br>  프로젝트 기간 중 컨디션이 좋지 않았음에도 내색하지 않고 자기 역할을 끝가지 마쳐준 팀장님 너무 고맙습니다 멋져요! 그리고 팀장 같은 팀원의 의견을 잘 받아주고 믿고 따라와줘서 감사해요 운이 너무 좋았네요 짱 :)               |
