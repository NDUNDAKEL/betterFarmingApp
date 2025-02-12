# Generated by Django 5.1.4 on 2024-12-14 20:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betterFarmingApp', '0006_delete_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('Profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image/')),
            ],
        ),
    ]
