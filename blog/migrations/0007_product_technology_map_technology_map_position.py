# Generated by Django 2.0.13 on 2019-04-08 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190408_2108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('balance', models.IntegerField()),
                ('code', models.IntegerField()),
                ('img', models.CharField(max_length=900)),
            ],
        ),
        migrations.CreateModel(
            name='Technology_map',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.IntegerField()),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Technology_map_position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('technology_map_id', models.IntegerField()),
                ('material_id', models.IntegerField()),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
