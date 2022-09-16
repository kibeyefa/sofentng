from email.policy import default
import re
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.forms import UUIDField
from uuid import uuid4 as v4
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel


User = get_user_model()
# Create your models here.
class DonateItem(TitleSlugDescriptionModel, TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=v4, unique=True)
  donator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True ,related_name='donator')
  collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collector', default=None)

  class Meta:
    ordering = ('created',)

  @property
  def image_set_urls(self):
    return [image.image.url for image in self.images.all()]

  @property
  def first_image_url(self):
    return self.images.all().first().image.url

  def __str__(self) -> str:
    return f'{self.title} from {self.donator.email}'

class DonateItemImage(models.Model):
  donate_item = models.ForeignKey(DonateItem, on_delete=models.CASCADE, related_name='images', related_query_name='images')
  image = models.FileField(upload_to='donate/images/')

  def count(self):
    all_images = [image for image in DonateItemImage.objects.complex_filter(Q(donate_item = self.donate_item))]
    return all_images.index(self)