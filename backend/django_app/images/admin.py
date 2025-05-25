from django.contrib import admin

from .models import UploadedImage, ProcessedImage, FileArchive


admin.site.register(UploadedImage)
admin.site.register(ProcessedImage)
admin.site.register(FileArchive)
