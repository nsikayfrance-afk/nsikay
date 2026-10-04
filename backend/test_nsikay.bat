@echo off

echo === TEST SECURITE NSIKAY ===

python manage.py check

python manage.py test api_nsikay

echo === FIN TEST ===

