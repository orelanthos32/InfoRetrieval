# Generated by Django 3.1.7 on 2021-03-15 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reddit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Term', models.CharField(max_length=100)),
                ('Company_Name', models.CharField(max_length=100)),
                ('Last_Sale', models.IntegerField(max_length=20)),
                ('Net_Change', models.IntegerField(max_length=20)),
                ('Percent_Change', models.IntegerField(max_length=20)),
                ('Market_Cap', models.IntegerField(max_length=20)),
                ('Country', models.CharField(max_length=100)),
                ('IPO_Year', models.IntegerField(max_length=20)),
                ('Volume', models.IntegerField(max_length=20)),
                ('Sector', models.CharField(max_length=100)),
                ('Industry', models.CharField(max_length=100)),
                ('Frequency', models.IntegerField(max_length=20)),
            ],
        ),
    ]
