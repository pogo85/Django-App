from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.category

    def two_decimals(self):
        self.amount = float("{:.2f}".format(self.amount))
        self.save()

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering: ['-name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name




