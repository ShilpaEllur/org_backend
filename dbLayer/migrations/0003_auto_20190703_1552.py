# Generated by Django 2.1.5 on 2019-07-03 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbLayer', '0002_auto_20190603_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgusers',
            name='map_id',
            field=models.CharField(max_length=8, null=True),
        ),
    ]