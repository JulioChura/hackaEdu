#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=" * 60)
print("VERIFICANDO SOCIAL APPLICATION DE GOOGLE")
print("=" * 60)

# Verificar Sites
print("\n📍 SITES DISPONIBLES:")
for site in Site.objects.all():
    print(f"   - ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

# Verificar Social Apps
print("\n🔐 SOCIAL APPLICATIONS:")
social_apps = SocialApp.objects.all()
if not social_apps:
    print("   ❌ NO HAY SOCIAL APPLICATIONS REGISTRADAS")
else:
    for app in social_apps:
        print(f"\n   Provider: {app.provider}")
        print(f"   Name: {app.name}")
        print(f"   Client ID: {app.client_id}")
        print(f"   Secret: {app.secret[:20]}..." if app.secret else "   Secret: (vacío)")
        print(f"   Sites asociados:")
        for site in app.sites.all():
            print(f"      - {site.domain}")

# Verificar específicamente Google
print("\n🔍 BUSCANDO GOOGLE OAUTH:")
try:
    google_app = SocialApp.objects.get(provider='google')
    print(f"   ✅ ENCONTRADO")
    print(f"   - Provider: {google_app.provider}")
    print(f"   - Name: {google_app.name}")
    print(f"   - Client ID: {google_app.client_id}")
    print(f"   - Sites: {[s.domain for s in google_app.sites.all()]}")
except SocialApp.DoesNotExist:
    print(f"   ❌ NO ENCONTRADO - Este es el problema")

print("\n" + "=" * 60)
