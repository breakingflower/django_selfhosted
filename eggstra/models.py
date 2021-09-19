from datetime import timedelta
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=64, blank=True) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class EggPost(models.Model): 
    amount = models.PositiveIntegerField('Gather amount', default=1, validators=[MinValueValidator(1)])
    notes = models.CharField(max_length=256, blank=True, null=True)

    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User,
        verbose_name="user",
        related_name="eggpost",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.date}: {self.amount} ({self.notes})"
    
    class Meta:
        ordering = ['-date']

    @property
    def days_from_gather_date(self) -> int:
        """
        Number of days between now and post date.
        """
        days = (timezone.now().date() - self.date).days
        return days

    @property
    def age(self) -> str: 
        """
        Formatter for days from_gather_date
        """
        days = self.days_from_gather_date
        if days == 0: 
            return f"vandaag"
        elif days == 1: 
            return f"{days} dag geleden"
        else: 
            return f"{days} dagen geleden"
