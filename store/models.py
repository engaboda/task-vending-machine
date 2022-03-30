from utils.time_stamp_model import TimeStampedModel
from django.db import models


class Product(TimeStampedModel):
    amountAvailable = models.IntegerField()
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    productName = models.CharField(max_length=255)
    seller = models.ForeignKey('account.User', related_name='products', on_delete=models.CASCADE)
