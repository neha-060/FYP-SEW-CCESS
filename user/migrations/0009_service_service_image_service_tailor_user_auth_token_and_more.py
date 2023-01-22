# Generated by Django 4.0.3 on 2023-01-21 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_password2'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='service_image',
            field=models.ImageField(null=True, upload_to='service_imgs/'),
        ),
        migrations.AddField(
            model_name='service',
            name='tailor',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.tailor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='auth_token',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
