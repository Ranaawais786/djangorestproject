# Generated by Django 4.0 on 2021-12-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='NAME',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
