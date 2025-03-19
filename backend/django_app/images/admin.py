from django.contrib import admin

from images.models import UploadedImage, ProcessedImage


admin.site.register(UploadedImage)
admin.site.register(ProcessedImage)
