# Generated by Django 3.2 on 2021-05-22 16:37

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_delete_contactus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('query', models.TextField()),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'contact us',
            },
        ),
    ]