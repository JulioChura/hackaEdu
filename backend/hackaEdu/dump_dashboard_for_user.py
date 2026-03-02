"""
Dump the dashboard full payload for a given user email
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hackaEdu.settings')
django.setup()

from auth_custom.models import CustomUser
from usuarios.dashboard_service import DashboardService

email = 'admin@admin.com'
user = CustomUser.objects.filter(email=email).first()
if not user:
    print('User not found:', email)
else:
    data = DashboardService.get_full_dashboard(user)
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))
