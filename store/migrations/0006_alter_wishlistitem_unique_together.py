# Generated by Django 5.1.2 on 2024-11-01 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_customer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlistitem',
            unique_together={('wishlist_object', 'project_object', 'is_order_placed')},
        ),
    ]
