# Generated by Django 4.2 on 2023-05-22 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='id_author',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bd.authors'),
        ),
    ]
