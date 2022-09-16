from fileinput import filename
from django.db import models
from django_extensions.db.fields import AutoSlugField
from cloudinary_storage.storage import RawMediaCloudinaryStorage

# Create your models here.


def upload_and_rename_research_document(self, filename):
    print(filename)
    extension = filename.split('.')[-1]
    return f"research/{self.name}.{extension}"


class ResearchDocument(models.Model):
    name = models.CharField(max_length=2000)
    file = models.FileField(
        upload_to=upload_and_rename_research_document, storage=RawMediaCloudinaryStorage())
    slug = AutoSlugField(populate_from=['name', 'id'])
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name

    @property
    def filesize(self):
        x = self.file.size
        y = 512000
        if x < y:
            value = round(x/1000, 2)
            ext = ' kb'
        elif x < y*1000:
            value = round(x/1000000, 2)
            ext = ' Mb'
        else:
            value = round(x/1000000000, 2)
            ext = ' Gb'
        return str(value)+ext

    @property
    def get_absolute_url(self):
        return str(self.file.url)
