import os
import sys
import django
from django.db import connection

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

with connection.cursor() as cursor:
    print("Checking accounts tables...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'accounts_user_%'")
    tables = cursor.fetchall()
    print("Join tables found:", tables)
    
    cursor.execute("PRAGMA table_info(accounts_user)")
    columns = cursor.fetchall()
    print("Columns in accounts_user:", [c[1] for c in columns])
