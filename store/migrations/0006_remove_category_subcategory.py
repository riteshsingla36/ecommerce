# Generated by Django 3.2 on 2021-05-21 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_category_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory',
        ),
    ]
