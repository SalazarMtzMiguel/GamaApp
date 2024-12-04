# Generated by Django 5.1.3 on 2024-12-03 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamaApp', '0008_alter_simulation_file_project_simulation_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='simulations', to='GamaApp.project'),
        ),
    ]
