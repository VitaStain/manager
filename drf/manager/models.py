from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .categories import standard_categories

# Create your models here.


class Profile(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']


class Category(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Profile, related_name='categories', on_delete=models.CASCADE)


class Balance(models.Model):
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    user = models.OneToOneField(Profile, related_name='balance', on_delete=models.CASCADE)


class Transaction(models.Model):
    ACTION_CHOICES = [
        ('debit', 'db'),
        ('replenish', 'rp'),
    ]

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    summa = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(Profile, related_name='transaction', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, default='200')


@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
        for category in standard_categories:
            Category.objects.create(name=category, user=instance)
