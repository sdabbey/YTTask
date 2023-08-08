# Generated by Django 4.2.3 on 2023-08-08 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_yttasker'),
        ('dashboard', '0007_rename_value_task_point_rename_link_task_prompt'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='YTTasker_payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payout', models.FloatField()),
                ('tasker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.yttasker')),
            ],
        ),
    ]
