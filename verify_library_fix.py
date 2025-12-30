
import os
import django
from django.conf import settings

# Configure minimal Django settings
if not settings.configured:
    settings.configure(TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates'}])
    django.setup()

from django.template.context import BaseContext, Context
from copy import copy

try:
    print("Testing BaseContext copy...")
    bc = BaseContext({'a': 1})
    bc_copy = copy(bc)
    print(f"BaseContext copy result: {bc_copy.dicts}")

    print("Testing Context copy...")
    c = Context({'b': 2})
    c_copy = copy(c)
    print(f"Context copy result: {c_copy.dicts}")
    
    print("SUCCESS: Copy operations worked.")

except Exception as e:
    print(f"FAILURE: {e}")
