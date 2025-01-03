import os
from django.contrib.auth.models import User

# Verifica se o superusuário já existe
username = os.environ.get("SUPERADMINDJANGO")
email = os.environ.get("SUPEREMAILDJANGO")
password = os.environ.get("SUPERSENHADJANGO")

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")