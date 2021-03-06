# Generated by Django 3.2.2 on 2021-06-04 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210603_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='note',
            field=models.TextField(max_length=255, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='parent',
            name='verify',
            field=models.CharField(default=None, max_length=45, null=True, verbose_name='Верификация'),
        ),
        migrations.AlterField(
            model_name='student',
            name='cityOfRegistration',
            field=models.CharField(max_length=45, verbose_name='Город прописки'),
        ),
        migrations.AlterField(
            model_name='student',
            name='juvenileAffairsUnit',
            field=models.CharField(choices=[(1, 'да'), (0, 'нет')], default=0, max_length=45, verbose_name='Отдел по делам несовершеннолетних'),
        ),
        migrations.AlterField(
            model_name='student',
            name='note',
            field=models.TextField(max_length=255, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='student',
            name='sportsSections',
            field=models.CharField(max_length=45, verbose_name='Спортивные секции'),
        ),
        migrations.AlterField(
            model_name='student',
            name='verify',
            field=models.CharField(default=None, max_length=45, null=True, verbose_name='Верификация'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='note',
            field=models.TextField(max_length=255, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='verify',
            field=models.CharField(default=None, max_length=45, null=True, verbose_name='Верификация'),
        ),
    ]
