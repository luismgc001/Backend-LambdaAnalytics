from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users(apps, schema_editor):
    User = apps.get_model('usuarios', 'User')
    
    # Crear usuario administrador
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
    print("Usuario administrador de ejemplo creado:", admin_user.email)
    print("contraseña: ", "admin123")
    
    # Crear usuario de ejemplo
    example_user = User.objects.create(
        email='user@example.com',
        first_name='Example',
        last_name='User',
        phone='987654321',
        gender='F',
        role='user',  # Cambia 'user' por el rol adecuado en tu modelo
        is_active=True,
        password=make_password('user123'),  # Encripta la contraseña
    )
    print("Usuario de ejemplo creado:", example_user.email)
    print("Contraseña: ", "user123")

class Migration(migrations.Migration):
    dependencies = [
        ('usuarios', '0001_initial'),  # Cambia esto por el nombre de tu migración inicial
    ]

    operations = [
        migrations.RunPython(create_users),
    ]
