from django.db import models


class Dealer(models.Model):
    title = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=50)
    area = models.CharField(max_length=40, blank=True)
    rating = models.FloatField(max_length=40, blank=True)


class Car(models.Model):
    dealer = models.ForeignKey(
            'Dealer',
               null=False,
               on_delete=models.PROTECT,
               verbose_name='Дилер'
    )
    firm = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.IntegerField()
    power = models.IntegerField()
    color = models.CharField(max_length=20)
    price = models.IntegerField()


