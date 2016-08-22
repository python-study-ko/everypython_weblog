#!/usr/bin/env bash

echo "-------파이썬 가상환경 생성기-------"
if [ -d .venv ]
then
    echo " 이전의 가상환경을 삭제하겠습니다."
    rm -rf .venv
fi

echo "------가상환경을 만들고 있습니다-------"
virtualenv -p python3.5 .venv

. .venv/bin/activate

echo "-------필수 모듈을 설치합니다-------"
pip install -r requirments.txt

if [ ! -f weproject/settings.ini ]
then
    echo "설정 파일이 없어 샘플 설정을 복사했습니다"
    cp webproject/settings.ini.sample webproject/settings.ini
fi

deactivate
echo "모든 작업이 완료 되었습니다. settings.ini에서 설정을 바꾸세요"
echo "source .venv/bin/activate 로 가상환경을 실행하고"
echo "deactivate로 가상환경을 종료하면 됩니다"
