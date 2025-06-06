# Generated by Django 5.1.4 on 2024-12-13 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyBill', '0003_remove_invoiceline_invoice_invoice_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('paid', 'PAID'), ('unpaid', 'UNPAID'), ('pending', 'PENDING')], default='pending', max_length=20),
        ),
    ]
