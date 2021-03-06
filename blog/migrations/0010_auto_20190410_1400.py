# Generated by Django 2.0.7 on 2019-04-10 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190409_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.AlterField(
            model_name='technology_map_position',
            name='technology_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Technology_map'),
        ),
    ]
