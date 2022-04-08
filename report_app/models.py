from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Report(models.Model):
    report_name = models.CharField("REPORT NAME", max_length=50)
    assigned_to = models.ManyToManyField(User)

    def __str__(self):
        return self.report_name
