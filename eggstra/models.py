from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import User
# Create your models here.

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
