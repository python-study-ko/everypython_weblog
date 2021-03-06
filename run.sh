#!/usr/bin/env bash

echo "-------Virtualenv-------"
virtualenv -p python3.5 .venv
. .venv/bin/activate

echo "-------Requirements-------"
pip install -r requirments.txt

echo "-------migrate django-------"
cd webproject
cp everpython/settings.samples everpython/settings.py
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
echo "-------collect static-------"
python manage.py collectstatic

echo " "
echo "-------create superuser--------"
python manage.py createsuperuser
echo "please check everypython/settings.py AWS information"
echo "please make superuser : python manage.py createsuperuser"