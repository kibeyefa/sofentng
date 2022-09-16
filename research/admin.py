from django.contrib import admin
from .models import ResearchDocument

# Register your models here.
# admin.site.register(ResearchDocument)


@admin.register(ResearchDocument)
class ResearchDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'filesize', 'created_on')
    search_fields = ('name',)
    list_max_show_all = 100
