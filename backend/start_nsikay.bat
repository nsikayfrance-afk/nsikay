@echo off

echo ==========================
echo DEMARRAGE NSIKAY
echo ==========================

call venv\Scripts\activate

python manage.py migrate

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

