# Generated by Django 3.1.5 on 2021-01-14 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20210114_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.budget'),
        ),
    ]
