from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Курс", help_text="Укажите курс"
    )

    preview = models.ImageField(
        upload_to="materials/courses/previews/",
        verbose_name="Превью курса",
        blank=True,
        null=True,
        help_text="Загрузите превью курса",
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Добавьте описание курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="Урок", help_text="Укажите урок"
    )

    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
        help_text="Добавьте описание урока",
    )
    preview = models.ImageField(
        upload_to="materials/lessons/previews/",
        verbose_name="Превью урока",
        blank=True,
        null=True,
        help_text="Загрузите превью урока",
    )

    video_reference = models.URLField(
        max_length=100,
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Укажите ссылку на видео",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        related_name="lessons",
        help_text="Укажите ссылку",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
