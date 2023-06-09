# Generated by Django 4.1.7 on 2023-03-27 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passwords', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(verbose_name='User action')),
                ('note', models.TextField(null=True, verbose_name='Note for the action')),
                ('ip_address', models.TextField(verbose_name='IP address from which the action was performed')),
                ('danger_level', models.PositiveSmallIntegerField(default=0, verbose_name='The level of danger of the action')),
                ('execution_at', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passwords.profile', verbose_name='Profile')),
            ],
        ),
    ]
