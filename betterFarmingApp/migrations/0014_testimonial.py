# Generated by Django 5.1.4 on 2024-12-16 07:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betterFarmingApp', '0013_delete_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer', models.CharField(default='Anonymous', max_length=100)),
                ('reviewerid', models.IntegerField(blank=True, null=True)),
                ('content', models.TextField()),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile_image', models.ImageField(blank=True, default='./static/img/noProfile.png', null=True, upload_to='profile_image/')),
            ],
        ),
    ]
