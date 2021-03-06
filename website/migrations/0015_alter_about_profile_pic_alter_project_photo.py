# Generated by Django 4.0.4 on 2022-05-23 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_alter_about_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='profile_pic',
            field=models.FileField(upload_to='profile_pic'),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.FileField(upload_to='projects'),
        ),
    ]
