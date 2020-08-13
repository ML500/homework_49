# Generated by Django 2.2 on 2020-08-13 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20200809_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='statuses', to='webapp.Status', verbose_name='Статус'),
        ),
    ]