from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
User = get_user_model()

DAILY = 'DA'
WEEKLY = 'WE'
MONTHLY = 'MO'
YEARLY = 'YE'

REMINDER_INTERVAL_CHOICES = [
    (DAILY, 'Daily'),
    (WEEKLY, 'Weekly'),
    (MONTHLY, 'Monthly'),
    (YEARLY, 'Yearly'),
]

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    reminder_interval = models.CharField(max_length=2, choices=REMINDER_INTERVAL_CHOICES, default=MONTHLY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
