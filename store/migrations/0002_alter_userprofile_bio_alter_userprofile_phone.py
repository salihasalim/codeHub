# Generated by Django 5.1.2 on 2024-10-17 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
