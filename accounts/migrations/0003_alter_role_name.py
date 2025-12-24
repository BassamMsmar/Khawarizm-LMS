
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('admin', 'Admin'), ('staff', 'Staff'), ('lecturer', 'Lecturer'), ('student', 'Student')], max_length=100, unique=True),
        ),
    ]
