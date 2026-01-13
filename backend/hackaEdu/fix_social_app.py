#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Obtener la Social App de Google
google_app = SocialApp.objects.get(provider='google')

# Obtener el Site localhost:8000
site = Site.objects.get(domain='localhost:8000')

# Agregar el site
google_app.sites.add(site)

print("✅ Site 'localhost:8000' agregado a Google OAuth")
print(f"   Sites asociados ahora: {[s.domain for s in google_app.sites.all()]}")
