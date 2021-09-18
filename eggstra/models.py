from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class EggsAvailable(models.Model): 
    amount = models.IntegerField('Gather amount')
    notes = models.CharField(max_length=256, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
        verbose_name="Created by",
        related_name="Egg_posts",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.created_on}: {self.amount} ({self.notes})"
    
    class Meta:
        ordering = ['-created_on']

    @property
    def time_from_gather_date(self): 
        td = timezone.now() - self.created_on
        td_str = str(td).split('.')[0]

        return f"Age: {td_str}"
