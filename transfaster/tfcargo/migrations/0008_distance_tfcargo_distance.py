# Generated by Django 4.2.1 on 2024-10-14 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tfcargo', '0007_alter_tfcargo_is_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('time', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='tfcargo',
            name='distance',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tfcargo', to='tfcargo.distance'),
        ),
    ]
