from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EmployeeDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    fullName = models.CharField(max_length=100, null=True)
    phonenumber = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    doj = models.DateField(null=True)
    empID = models.CharField(max_length=20, null=True)
    empDept = models.CharField(max_length=20, null=True)
    designation = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    password = models.CharField(max_length=100, null=True)  

    def __str__(self):
        return self.empID


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Day(models.Model):
    WEEKDAYS = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    ]
    day_of_week = models.CharField(max_length=3, choices=WEEKDAYS, null=True)

    def __str__(self):
        return self.get_day_of_week_display()


class Schedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    work_description = models.CharField(max_length=255, null=True)  

    def __str__(self):
        return f"{self.day} - {self.time_slot}"
    
class EmployeeWorkDetail(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    project = models.CharField(max_length=100)
    assigned_on = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    def is_completed(self):
        return self.completion_date is not None

    def __str__(self):
        return self.name

