from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import User


class UploadedImage(models.Model):
    """
    Модель для хранения информации о спутниковых снимках, загруженных пользователями.
    """

    id = models.AutoField(primary_key=True)
    binary_image = models.FileField(upload_to="satellite_images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_images")
    upload_date = models.DateTimeField(auto_now_add=True)
    sea_type = models.CharField(
        max_length=50,
        choices=[("ЧЕРНОЕ", "Черное Море"), ("АЗОВСКОЕ", "Азовское Море")],
    )

    def __str__(self):
        return f"Изображение {self.id} загружено {self.user.username}"


class ProcessedImage(models.Model):
    """
    Модель для хранения обработанных изображений с результатами обнаружения загрязнений
    """

    id = models.AutoField(primary_key=True)
    binary_image = models.FileField(upload_to="processed_images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="processed_images")
    uploaded_image = models.ForeignKey(
        UploadedImage, on_delete=models.CASCADE, related_name="processed_versions"
    )
    area_of_pollution = models.FloatField(
        help_text="Площадь загрязнения в квадратных километрах"
    )
    degree_of_pollution = models.FloatField(
        help_text="Степень уверенности модели в обнаружении (0-100)"
    )
    processing_date = models.DateTimeField(auto_now_add=True)

    # Форма загрязнения (реализация на GeoDjango)
    geometry = gis_models.PolygonField(
        srid=4326, null=True, blank=True, help_text="Полигональная форма загрязнения"
    )

    def __str__(self):
        return f"Обработанное изображение {self.id} с площадью загрязнения {self.area_of_pollution} км²"
