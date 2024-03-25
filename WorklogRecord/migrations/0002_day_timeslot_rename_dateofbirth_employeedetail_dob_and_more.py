# Generated by Django 5.0.3 on 2024-03-15 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorklogRecord', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.RenameField(
            model_name='employeedetail',
            old_name='dateOfBirth',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='employeedetail',
            old_name='joiningDate',
            new_name='doj',
        ),
        migrations.RemoveField(
            model_name='employeedetail',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='employeedetail',
            name='user',
        ),
        migrations.AddField(
            model_name='employeedetail',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='employeedetail',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employeedetail',
            name='phonenumber',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='employeedetail',
            name='designation',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employeedetail',
            name='empDept',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employeedetail',
            name='empID',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employeedetail',
            name='fullName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employeedetail',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorklogRecord.day')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WorklogRecord.timeslot')),
            ],
        ),
    ]
