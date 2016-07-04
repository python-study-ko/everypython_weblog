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

