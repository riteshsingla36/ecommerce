# Generated by Django 3.2 on 2021-05-21 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_customer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subcategory',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
