# Generated by Django 3.2.8 on 2021-11-21 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_orderplaced'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='product',
        ),
    ]