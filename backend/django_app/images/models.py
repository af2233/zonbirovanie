from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()


class UploadedImage(models.Model):
    """
    Модель для хранения информации о спутниковых снимках, загруженных пользователями.
    """

    image = models.ImageField(upload_to="uploaded/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class ProcessedImage(models.Model):
    """
    Модель для хранения обработанных изображений с результатами обнаружения загрязнений.
    """

    image = models.ImageField(upload_to="processed/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE)
    area_of_pollution = models.FloatField(null=True)
    degree_of_pollution = models.FloatField(null=True)

    def __str__(self):
        return self.image.name


class FileArchive(models.Model):
    """
    Модель для архива изображений.
    """

    uploaded_file = models.FileField(upload_to="uploaded/")
    processed_file = models.FileField(upload_to="processed/", default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.UUIDField(unique=True, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archive #{self.id} - {self.uploaded_file.name}"
