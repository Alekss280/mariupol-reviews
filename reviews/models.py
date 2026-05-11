from django.db import models

class Category(models.Model):
    """Категория услуг: Общественное питание, Торговля, Бытовые услуги и т.д."""
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Enterprise(models.Model):
    """Предприятие сферы услуг (ресторан, магазин и т.д.)"""
    name = models.CharField(max_length=200, verbose_name="Название предприятия")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория",
        related_name="enterprises"
    )
    address = models.TextField(blank=True, verbose_name="Адрес")
    # Для карты (пока оставим пустыми, заполним позже)
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"


def simple_sentiment(text):
    """Примитивная функция определения тональности по ключевым словам"""
    positive_words = ['хорошо', 'отлично', 'спасибо', 'быстро', 'качественно', 'рекомендую', 'понравилось', 'вежливый']
    negative_words = ['плохо', 'ужасно', 'кошмар', 'долго', 'недоволен', 'ужас', 'невозможно', 'грубый']
    
    text_low = text.lower()
    pos = sum(1 for w in positive_words if w in text_low)
    neg = sum(1 for w in negative_words if w in text_low)
    
    if pos > neg:
        return 'positive'
    elif neg > pos:
        return 'negative'
    else:
        return 'neutral'


class Review(models.Model):
    """Отзыв о предприятии (анонимный)"""
    enterprise = models.ForeignKey(
        Enterprise, 
        on_delete=models.CASCADE, 
        verbose_name="Предприятие",
        related_name="reviews"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], 
        verbose_name="Оценка (1-5)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    sentiment = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        verbose_name="Тональность",
        choices=[('positive', 'Позитивный'), ('neutral', 'Нейтральный'), ('negative', 'Негативный')]        
    )
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    def save(self, *args, **kwargs):
        # Автоматически определяем тональность, если она не задана
        if not self.sentiment:
            self.sentiment = simple_sentiment(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв о {self.enterprise.name} - {self.rating}★"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']  # новые отзывы сверху