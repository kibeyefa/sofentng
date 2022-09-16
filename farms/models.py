from django.db import models
from django_extensions.db.fields import RandomCharField, CreationDateTimeField
# from django.

# Create your models here.


class FarmProduce(models.Model):
    name = models.CharField(max_length=255)
    price_per_unit = models.IntegerField()
    unit_name = models.CharField(max_length=255, blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class FarmProdudeOrder(models.Model):
    id = RandomCharField(unique=True, primary_key=True, length=10)
    produce = models.ForeignKey(FarmProduce, null=True, on_delete=models.SET_NULL,
                                related_name='farm_order', related_query_name='farm_order')
    price = models.BigIntegerField(blank=True, null=True)
    completed = models.BooleanField(null=True, blank=True, default=False)
    unit = models.BigIntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.TextField()
    phone_no = models.CharField(max_length=11)
    created = CreationDateTimeField()

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.id

    @property
    def total_price(self):
        return int(self.produce.price_per_unit * self.unit)

    def save(self, *args, **kwargs) -> None:
        self.price = self.total_price
        return super().save(*args, **kwargs)
