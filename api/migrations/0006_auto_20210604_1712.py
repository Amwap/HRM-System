# Generated by Django 3.2.2 on 2021-06-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210604_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='admin',
            field=models.CharField(blank=True, choices=[(1, 'да'), (0, 'нет')], default='нет', max_length=3, verbose_name='Статус администратора'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='specialist',
            field=models.CharField(blank=True, choices=[(1, 'да'), (0, 'нет')], default='нет', max_length=3, verbose_name='Специалист УО'),
        ),
    ]
