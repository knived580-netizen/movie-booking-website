import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviebooking.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@gmail.com", "admin123")