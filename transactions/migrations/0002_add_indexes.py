# transactions/migrations/0002_add_indexes.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('transactions', '0001_initial'),
    ]
    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', 'date'], name='transactio_user_id_ea37bd_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', 'type'], name='transactio_user_id_1f1cb9_idx'),
        ),
    ]