# Generated by Django 2.0.13 on 2019-04-08 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='material',
            fields=[
                ('_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('code_material', models.CharField(max_length=100)),
                ('img', models.CharField(max_length=1000)),
                ('balance', models.IntegerField()),
            ],
        ),
    ]
