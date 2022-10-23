# Generated by Django 4.1.1 on 2022-10-01 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_itemorder_customer_itemorder_order_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kititem',
            name='kit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kititems', to='dashboard.kit'),
        ),
        migrations.CreateModel(
            name='KitDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateTimeField(auto_now=True)),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.kit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.item')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
