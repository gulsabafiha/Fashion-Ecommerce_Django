# Generated by Django 3.2.8 on 2021-11-20 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_billing_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Single_Product_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_img', models.ImageField(null=True, upload_to='product-img')),
                ('side_img1', models.ImageField(null=True, upload_to='product-img')),
                ('side_img2', models.ImageField(null=True, upload_to='product-img')),
                ('side_img3', models.ImageField(null=True, upload_to='product-img')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='OrderPlaced',
        ),
    ]
