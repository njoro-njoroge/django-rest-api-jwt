from django.db import models
from django.db.models import UniqueConstraint, Q
from django.db.models.functions import Lower


class Client(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    store_name = models.CharField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return (f'{self.first_name} {self.last_name}, {self.phone_number}, '
                f'{self.email}, {self.store_name}')
