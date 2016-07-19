# everypython_weblog
에브리파이썬용 블로그 제작

### 시작하기전에
이 프로젝트를 클론하셨다면 제일먼저
`chmod +x run.sh`
`./run.sh`
위에 두 명령어를 실행하셔서 개발환경을 구축하면 됩니다.
정적 파일을 모으는 과정에서 yes,no를 물으면 yes를 입력하시면 됩니다.
자동으로 작업을 위한 가상환경을 만들어주고 필요한 파일들을 설치가 될것입니다.
가상환경은 최상위 폴더에 생성될것이며 `source .venv/bin/activate`로 실행하시면 됩니다.

### 설정하기
개발 구축이 완료되면 아래단계를 진행하셔야 정상적으로 모든 기능을 사용하실수 있습니다.
1. settings.py에 있는 s3파일 업로드를 위한 AWS정보를 입력하세요
2. `cd everypython` -> `python manage.py createuser`로 amdin에서 사용할 최고관리자 계정을 생성하세요

### 외부 프로그램 연동
#### 1. ckeditor에서 파일 업로드를 위한 s3 연동
settings.py에 아래 항목을 채워넣으시면 됩니다

`
# s3 설정
AWS_S3_HOST = 's3-ap-northeast-2.amazonaws.com' # 서울 리전(자신이 만든 버킷의 지역을 입력하세요)
AWS_QUERYSTRING_AUTH = False    # 수정하면 업로드 안됩니다.
AWS_ACCESS_KEY_ID = 'xxxxxxxxxxxxxxxxxx'    # 필수
AWS_SECRET_ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # 필수
AWS_STORAGE_BUCKET_NAME = 'xxxxxxxxxxxxxxxxxxxxx'   # 벗킷
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
`

#### 2. 구글 웹로그 대쉬보드 연동

> 다른도메인으로 연결된것으로 연동 확인은 했으나 실제 블로그 연결을 테스트해볼수 없었습니다.
 추후 테스트후 업데이트 하겠습니다.

어드민 대쉬보드에서 블로그 방문자를 확인하려면 아래 과정이 필요합니다.
1. 제일먼저 자신의 블로그 도메인명으로 웹로그에 회원가입후 홈페이지와 연동합니다.
2. 구글 api에서 outh2.0 api를 웹용으로 발급받아 json파일을 다운받습니다.
3. 파일명을 'client_secrets.json'으로 바꾸고 dashboard.py와 같은 위치에 넣어둡니다.
4. 대쉬보드 위젯 추가에서 구글api위젯을 추가합니다.
5. 위젯 수정을 눌러 'grrant-access'를 누른후 인증을 합니다.
6. 대쉬보드에서 자신의 블로그 방문자를 확인할수 있습니다


