from django.db import models


class TimestampModel(models.Model):
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Products(TimestampModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name + ": " + self.description


class Offers(models.Model):
    offer_id = models.IntegerField()
    price = models.IntegerField()
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return "Offer id: " + self.offer_id.__str__() + " price: " + self.price.__str__() + " in stock: " + self.items_in_stock.__str__()
