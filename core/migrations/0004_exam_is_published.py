# Generated by Django 3.1.2 on 2020-10-28 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_published',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
