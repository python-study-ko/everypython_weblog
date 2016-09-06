#!/usr/bin/env bash

SYSTEM=$(uname)

# pgsql requierments 설치
# 운영체제가 리눅스일 경우
if [ $SYSTEM = 'Linux' ]; then
	SYSTEM_TYPE=$SYSTEM
	sudo apt-get install libpq-dev
# 운영체제가 맥일 경우
elif [ $SYSTEM = 'Darwin' ]; then
	SYSTEM_TYPE='Mac OS X'
	INSTALL_COMMAND="brew -y "
else
	SYSTEM_TYPE='NOT VALID'
fi

sudo apt-get install libpq-dev

echo "-------파이썬 가상환경 생성기-------"
if [ -d .venv ]
then
    echo " 이전의 가상환경을 삭제하겠습니다.";
    sudo rm -rf .venv
fi

echo "-------파이썬 가상환경 생성기-------"
virtualenv -p python3.5 .venv

. .venv/bin/activate

echo "-------필수 모듈을 설치합니다-------"
pip install -r requirments.txt

deactivate

echo "모든 작업이 완료 되었습니다. 모든 작업은 가상환경에서 실행하세"
echo "source .venv/bin/activate 로 가상환경을 실행하고"
echo "deactivate로 가상환경을 종료하면 됩니다"
