# Generated by Django 5.0.6 on 2024-05-08 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_userransom_creationdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='userransom',
            name='CertsPassword',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='userransom',
            name='CertsLocation',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
