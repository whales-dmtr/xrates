from django.db import models
from django.contrib.auth.models import User


class ConverterHistory(models.Model):
    convert_time = models.DateTimeField(auto_now=True)
    uah_amount = models.FloatField()
    converted_value = models.FloatField()
    converted_currency = models.CharField()
    rate = models.FloatField()
    user_id = models.ForeignKey(User, models.CASCADE)