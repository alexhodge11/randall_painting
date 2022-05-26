# Generated by Django 4.0.4 on 2022-05-23 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_customer_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='profile_pic',
            field=models.ImageField(upload_to='static/profile_pic/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.ImageField(upload_to='static/projects/'),
        ),
    ]
