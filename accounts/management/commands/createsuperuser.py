from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with admin role'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Superuser username')
        parser.add_argument('--email', type=str, required=True, help='Superuser email')
        parser.add_argument('--password', type=str, required=True, help='Superuser password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Create the admin role if it doesn't exist
        admin_role, created = Role.objects.get_or_create(
            name='Admin',
            slug='admin',
            defaults={'description': 'System administrator'}
        )

        # Create the superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        # Add admin role
        user.roles.add(admin_role)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {username} with admin role'))
