import os
import sys

sys.path.insert(0, r'C:\Users\DELL Technologies\Desktop\nsikay nante\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nsikay.settings')

import django
django.setup()

exec(open(r'C:\Users\DELL Technologies\Desktop\nsikay nante\backend\scripts\test_gift_resellers_stage4c.py', encoding='utf-8').read())