# Generated by Django 4.0.4 on 2022-05-23 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_about_profile_pic_alter_project_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='profile_pic',
            field=models.FileField(upload_to='static/profile_pic/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='photo',
            field=models.FileField(upload_to='static/projects/'),
        ),
    ]
