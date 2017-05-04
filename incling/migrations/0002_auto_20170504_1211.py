# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(help_text='True if student has not graduated, left, or been expelled', default=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='is_suspended',
            field=models.BooleanField(help_text='True if student is currently on suspension', default=False),
        ),
    ]
