from django.contrib import admin
from .models import User, UploadedImage, ProcessedImage, AnalysisRequest, Report


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
    search_fields = ("username", "email")


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


@admin.register(AnalysisRequest)
class AnalysisRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "get_image_id",
        "status",
        "created_at",
        "completed_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    date_hierarchy = "created_at"

    def get_image_id(self, obj):
        return f"Image #{obj.uploaded_image.id}"

    get_image_id.short_description = "Image"


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "sea_type",
        "created_at",
        "start_date",
        "end_date",
    )
    list_filter = ("sea_type", "created_at")
    search_fields = ("title", "user__username")
    date_hierarchy = "created_at"
    filter_horizontal = ("processed_images",)
