# Generated by Django 5.1.1 on 2024-09-18 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pieces', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interaction_type', models.CharField(choices=[('comment', 'Comment'), ('rating', 'Rating'), ('follow', 'Follow')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to=settings.AUTH_USER_MODEL)),
                ('piece', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pieces.piece')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification_receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
