# Generated by Django 5.0.6 on 2024-05-08 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userransom',
            name='CertsLocation',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='file',
            name='Content',
            field=models.TextField(max_length=9999999999999),
        ),
        migrations.AlterField(
            model_name='userransom',
            name='Files',
            field=models.ManyToManyField(to='web.file'),
        ),
    ]
