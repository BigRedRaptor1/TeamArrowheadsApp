# Generated by Django 3.2.5 on 2021-07-22 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=100)),
                ('payment_description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Diners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='menu_images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.ManyToManyField(related_name='item', to='customer.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.CharField(max_length=100)),
                ('promo_description', models.CharField(blank=True, max_length=100)),
                ('discount_multiplier', models.DecimalField(decimal_places=2, max_digits=7)),
                ('active', models.BooleanField(default=True)),
                ('start_date', models.CharField(blank=True, max_length=100, null=True)),
                ('end_date', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=15)),
                ('hour', models.CharField(max_length=15)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('rating', models.IntegerField(null=True)),
                ('feedback', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(default='preparing', max_length=100)),
                ('items', models.ManyToManyField(blank=True, related_name='order', to='customer.MenuItem')),
                ('mobile_number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.diners')),
                ('payment_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.bill')),
                ('promo_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.promotion')),
            ],
            options={
                'db_table': 'ordermodel',
            },
        ),
    ]
