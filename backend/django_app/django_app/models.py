from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
import uuid


class Image(models.Model):
    """
    Модель для хранения информации о спутниковых снимках.
    Изображения будут анализироваться для обнаружения разливов нефти.
    """

    class Meta:
        verbose_name = "Спутниковое изображение"
        verbose_name_plural = "Спутниковые изображения"
        ordering = ["-capture_date"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=255, help_text="Название или идентификатор изображения"
    )
    source = models.CharField(
        max_length=255,
        help_text="Источник изображения (например, MODIS от NASA, Copernicus от ESA, и т.д.)",
    )
    capture_date = models.DateField(
        help_text="Дата фиксации изображения", db_index=True
    )
    upload_date = models.DateTimeField(
        auto_now_add=True, help_text="Дата, когда изображение было загружено в систему"
    )
    file_path = models.FileField(
        upload_to="satellite_images/",
        blank=True,
        null=True,
        help_text="Путь к сохраненному файлу изображения",
    )

    processed = models.BooleanField(
        default=False, help_text="Было ли изображение обработано моделью"
    )

    # Метаданные для фильтрации и поиска
    location = models.CharField(
        max_length=255,
        help_text="Описание общего местоположения на изображении (например, Черное Море, восточная часть)",
    )
    sea_type = models.CharField(
        max_length=50,
        choices=[("ЧЕРНОЕ", "Черное Море"), ("АЗОВСКОЕ", "Азовское Море")],
        help_text="Название моря, запечатленного на изображении",
    )

    # Параметры изображения
    resolution = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Разрешение изображения в метрах на пиксель",
    )
    spectral_channels = models.IntegerField(
        blank=True, null=True, help_text="Количество спектральных каналов в изображении"
    )
    cloud_coverage = models.FloatField(
        blank=True, null=True, help_text="Процент облачности на изображении (0-100)"
    )

    def __str__(self):
        return f"{self.title} ({self.capture_date})"


class OilSpill(models.Model):
    """
    Модель для хранения информации об обнаруженных нефтяных пятнах.
    Каждое нефтяное пятно связано с конкретным изображением, на котором оно было обнаружено.
    """

    class Meta:
        verbose_name = "Нефтяное пятно"
        verbose_name_plural = "Нефтяные пятна"
        ordering = ["-detection_date"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="oil_spills",
        help_text="Изображение, на котором было обнаружено нефтяное загрязнение",
    )

    # Информация о нефтяном разливе
    area = models.FloatField(help_text="Площадь загрязнения в квадратных километрах")
    confidence = models.FloatField(
        help_text="Уровень уверенности модели в обнаружении (0-100)"
    )
    detection_date = models.DateTimeField(
        auto_now_add=True, help_text="Дата обнаружения загрязнения моделью"
    )

    # географические координаты (реализация на GeoDjango)
    location = gis_models.PointField(
        srid=4326, help_text="Географическое местоположение центра загрязнения"
    )
    geometry = gis_models.PolygonField(
        srid=4326, null=True, blank=True, help_text="Полигональная форма загрязнения"
    )

    # Дополнительные метаданные
    spill_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Тип загрязнения, если его возможно идентифицировать",
    )
    notes = models.TextField(
        blank=True, null=True, help_text="Дополнительные заметки или наблюдения"
    )

    def __str__(self):
        return f"Загрязнение в ({self.location}, {self.geometry}) обнаружено {self.detection_date.date()}"


class AnalysisRequest(models.Model):
    """
    Модель для отслеживания запросов пользователей на анализ изображений.
    Помогает логировать действия пользователя.
    """

    class Meta:
        verbose_name = "Запрос на анализ"
        verbose_name_plural = "Запросы на анализ"
        ordering = ["-created_at"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="analysis_requests",
        help_text="Пользователь, запросивший анализ",
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analysis_requests",
        help_text="Изображение для анализа",
    )

    # Информация о запросе
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания запроса"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, help_text="Дата завершения анализа"
    )

    # Состояние запроса
    STATUS_CHOICES = [
        ("ОЖИДАНИЕ", "Ожидание"),
        ("ОБРАБОТКА", "Обработка"),
        ("ЗАВЕРШЕНО", "Завершено"),
        ("ОШИБКА", "Ошибка"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ОЖИДАНИЕ",
        help_text="Текущий статус запроса на анализ",
    )

    # Параметры для анализа
    parameters = models.JSONField(
        default=dict, blank=True, help_text="Параметры анализа в формате JSON"
    )

    def __str__(self):
        return f"Анализ запрошен пользователем {self.user.username}, дата: {self.created_at.date()}"


class Report(models.Model):
    """
    Модель для хранения сгенерированных отчетов.
    """

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date")),
                name="valid_report_date_range",
            )
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports",
        help_text="Пользователь, создавший отчет",
    )

    # Метаданные отчета
    title = models.CharField(max_length=255, help_text="Report title")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата создания отчета"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Дата последнего обновления отчета"
    )

    # Параметры отчета
    start_date = models.DateField(
        help_text="Дата начала отчетного периода"
    )  # Эти даты указывают временной диапазон, за
    end_date = models.DateField(
        help_text="Дата окончания отчетного периода"
    )  # За который собирается информация в отчете
    sea_type = models.CharField(
        max_length=50,
        choices=[("ЧЕРНОЕ", "Черное Море"), ("АЗОВСКОЕ", "Азовское Море")],
        help_text="Море, описываемое в отчете",
    )

    # Общая информация в отчете
    summary = models.TextField(
        blank=True, null=True, help_text="Выводы о полученной информации"
    )
    file_path = models.FileField(
        upload_to="reports/",
        blank=True,
        null=True,
        help_text="Файл с отчетом (PDF/CSV)",
    )

    # Взаимосвязь отчета с проанализированными изображениями и обнаруженными разливами
    images = models.ManyToManyField(
        Image,
        related_name="reports",
        blank=True,
        help_text="Изображения, включенные в данный отчет",
    )
    oil_spills = models.ManyToManyField(
        OilSpill,
        related_name="reports",
        blank=True,
        help_text="Нефтяные разливы, включенные в данный отчет",
    )

    def __str__(self):
        return f"{self.title} ({self.created_at.date()})"
