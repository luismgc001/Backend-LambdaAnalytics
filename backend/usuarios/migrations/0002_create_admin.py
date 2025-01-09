from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_admin_user(apps, schema_editor):
    User = apps.get_model('usuarios', 'User')
    admin_user = User.objects.create(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        phone='123456789',
        gender='M',
        role='admin',
        is_active=True,
        password=make_password('admin123'),  # Encripta la contraseña
    )
    print("Usuario administrador creado:", admin_user.email)

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),  # Cambia esto por el nombre de tu migración inicial
    ]

    operations = [
        migrations.RunPython(create_admin_user),
    ]
