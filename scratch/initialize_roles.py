import os
import sys
import django

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from accounts.models import User, Role

def initialize_roles_and_admins():
    print("Initializing roles...")
    roles_to_create = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    
    for name, display in roles_to_create:
        role, created = Role.objects.get_or_create(name=name)
        if created:
            print(f"Created role: {name}")
    
    admin_role = Role.objects.get(name='admin')
    
    print("Assigning admin role to superusers...")
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        if not user.has_role('admin'):
            user.roles.add(admin_role)
            print(f"Assigned 'admin' role to: {user.email}")
        else:
            print(f"User {user.email} already has 'admin' role.")

if __name__ == "__main__":
    initialize_roles_and_admins()
    print("Done!")
