# Generated by Django 5.1.3 on 2025-01-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_alter_prescription_prescribed_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
