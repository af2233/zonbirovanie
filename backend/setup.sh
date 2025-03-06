#!/bin/bash

python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
cd django_app
python manage.py migrate
python manage.py runserver
