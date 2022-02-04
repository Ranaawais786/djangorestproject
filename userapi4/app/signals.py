from .models import Employee
from django.db.models.signals import post_delete
from django.dispatch import receiver
@receiver(post_delete,sender=Employee)
def delele_related_user(sender,instance,**kwargs):
    instance.user.delete()