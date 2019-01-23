from django.db import models
from django.contrib.auth.models import User

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')
    phone_number = models.CharField(max_length=20)
    shipping_address = models.TextField()
    activation_key = models.UUIDField(editable=False)

    def __str__(self):
        return self.user.username

        