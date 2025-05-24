from django.db import models

from users.models import User


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
