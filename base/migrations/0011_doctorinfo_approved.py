# Generated by Django 5.0.2 on 2024-03-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_doctorinfo_lorem'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorinfo',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
