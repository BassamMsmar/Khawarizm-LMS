import os
import sys
import django
from django.db import connection

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

with connection.cursor() as cursor:
    print("Dropping table MainDashboard_unit...")
    cursor.execute('DROP TABLE IF EXISTS MainDashboard_unit')
    print("Deleting migration history for MainDashboard...")
    cursor.execute("DELETE FROM django_migrations WHERE app='MainDashboard'")
    print("Done!")
