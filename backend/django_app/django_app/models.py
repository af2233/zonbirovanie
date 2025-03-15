from django.db import models
from django.contrib.gis.db import models as gis_models


class User(models.Model):
    """
    Модель пользователя
    """

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class UploadedImage(models.Model):
    """
    Модель для хранения информации о спутниковых снимках, загруженных пользователями.
    """

    id = models.AutoField(primary_key=True)
    binary_image = models.FileField(upload_to="satellite_images/")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="uploaded_images"
    )
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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="processed_images"
    )
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


class AnalysisRequest(models.Model):
    """
    Модель для отслеживания запросов пользователей на анализ изображений.
    Помогает логировать действия пользователя.
    """

    STATUS_CHOICES = [
        ("ОЖИДАНИЕ", "Ожидание"),
        ("ОБРАБОТКА", "Обработка"),
        ("ЗАВЕРШЕНО", "Завершено"),
        ("ОШИБКА", "Ошибка"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="analysis_requests"
    )
    uploaded_image = models.ForeignKey(
        UploadedImage, on_delete=models.CASCADE, related_name="analysis_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ОЖИДАНИЕ")

    def __str__(self):
        return f"Analysis request {self.id} by {self.user.username} - {self.status}"


class Report(models.Model):
    """
    Модель для хранения сгенерированных отчетов.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    sea_type = models.CharField(
        max_length=50,
        choices=[("ЧЕРНОЕ", "Черное Море"), ("АЗОВСКОЕ", "Азовское Море")],
    )
    file_path = models.FileField(upload_to="reports/", null=True, blank=True)
    processed_images = models.ManyToManyField(
        ProcessedImage, related_name="reports", blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="valid_report_date_range",
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.created_at.date()})"
