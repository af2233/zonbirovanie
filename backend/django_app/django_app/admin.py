from django.contrib import admin
from .models import Image, OilSpill, AnalysisRequest, Report


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("title", "source", "capture_date", "sea_type", "processed")
    list_filter = ("sea_type", "processed", "source")
    search_fields = ("title", "location")
    date_hierarchy = "capture_date"


@admin.register(OilSpill)
class OilSpillAdmin(admin.ModelAdmin):
    list_display = ("get_image_title", "area", "confidence", "detection_date")
    list_filter = ("detection_date", "spill_type")
    search_fields = ("image__title", "notes")
    date_hierarchy = "detection_date"

    def get_image_title(self, obj):
        return obj.image.title

    get_image_title.short_description = "Image"
    get_image_title.admin_order_field = "image__title"


@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "get_image_title", "status", "created_at", "completed_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "image__title")
    date_hierarchy = "created_at"

    def get_image_title(self, obj):
        return obj.image.title if obj.image else "No image"

    get_image_title.short_description = "Image"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "sea_type", "created_at", "updated_at")
    list_filter = ("sea_type", "created_at")
    search_fields = ("title", "user__username", "summary")
    date_hierarchy = "created_at"
    filter_horizontal = ("images", "oil_spills")
