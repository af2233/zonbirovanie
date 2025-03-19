from django.contrib import admin
from .models import UploadedImage, ProcessedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "upload_date", "sea_type")
    list_filter = ("sea_type", "upload_date")
    search_fields = ("user__username",)
    date_hierarchy = "upload_date"


@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_original_image",
        "user",
        "area_of_pollution",
        "degree_of_pollution",
        "processing_date",
    )
    list_filter = ("processing_date",)
    search_fields = ("user__username",)
    date_hierarchy = "processing_date"

    def get_original_image(self, obj):
        return f"Original Image #{obj.uploaded_image.id}"

    get_original_image.short_description = "Original Image"
    get_original_image.admin_order_field = "uploaded_image__id"
