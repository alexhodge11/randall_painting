# Generated by Django 4.0.4 on 2022-05-31 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_invoice_invoice_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_label',
            field=models.ImageField(upload_to='invoices_folder'),
        ),
    ]