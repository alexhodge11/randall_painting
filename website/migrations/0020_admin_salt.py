# Generated by Django 4.0.4 on 2022-05-26 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_customer_business_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='salt',
            field=models.TextField(blank=True),
        ),
    ]