# Generated by Django 3.0.7 on 2021-11-16 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20211107_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(blank=True, max_length=50, null=True)),
                ('lname', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.TextField(max_length=500)),
            ],
        ),
    ]
