from django.db import models
from datetime import timedelta

class Employee(models.Model):
    telegram_user_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)

    def total_duration(self):
        if self.check_in and self.check_out:
            return self.check_out - self.check_in
        return None

    def formatted_duration(self):
        duration = self.total_duration()
        if duration:
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = (remainder // 60)
            return f"{hours} hrs {minutes} mins"
        return "-"


    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"
