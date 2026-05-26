from django.db import models
import re

# ========== РАСШИРЕННЫЕ СЛОВАРИ ТОНАЛЬНОСТИ ==========

positive_words = {
    'хороший', 'хорошо', 'хорошая', 'хорошие', 'отличный', 'отлично', 'отличная',
    'прекрасный', 'прекрасно', 'замечательный', 'замечательно', 'великолепный', 'великолепно',
    'восхитительный', 'блестящий', 'превосходный', 'чудесный', 'чудесно', 'радостный',
    'удобный', 'быстро', 'качественный', 'качественно', 'вежливый', 'вежливо',
    'приветливый', 'вкусный', 'вкусно', 'свежий', 'чистый', 'чисто', 'аккуратный', 'аккуратно',
    'профессиональный', 'компетентный', 'грамотный', 'внимательный', 'отзывчивый', 'честный',
    'порядочный', 'надёжный', 'безопасный', 'современный', 'красивый', 'красиво',
    'уютный', 'комфортный', 'просторный', 'светлый', 'тихий', 'спокойный',
    'дешёвый', 'недорогой', 'доступный', 'выгодный', 'экономный',
    'пунктуальный', 'точный', 'оперативный', 'своевременный',
    'доволен', 'довольна', 'довольны', 'счастлив', 'восторг', 'наслаждение', 'удовольствие',
    'понравился', 'понравилась', 'понравилось', 'нравится', 'люблю', 'обожаю',
    'рекомендую', 'советую', 'спасибо', 'благодарю', 'благодарность',
    'супер', 'класс', 'клёво', 'шикарно', 'потрясающе', 'обалденно', 'зашибись', 'отпад',
    'круто', 'здорово', 'прелестно', 'изумительно', 'роскошно', 'божественно', 'неповторимо',
    'безупречно', 'идеально', 'надежно', 'отзывчивый', 'душевно', 'уютненько',
    'сносно', 'сносный'
}

negative_words = {
    'плохой', 'плохо', 'плохая', 'плохие', 'ужасный', 'ужасно', 'ужасная',
    'кошмарный', 'кошмарно', 'отвратительный', 'отвратительно', 'мерзкий', 'мерзко',
    'гнусный', 'подлый', 'скверный', 'дурной', 'негодный',
    'долгий', 'долго', 'медленный', 'медленно', 'некачественный', 'некачественно',
    'грубый', 'грубо', 'невкусный', 'невкусно', 'грязный', 'грязно',
    'неаккуратный', 'неаккуратно', 'непрофессиональный', 'невнимательный', 'невнимательно',
    'некомпетентный', 'безграмотный', 'хамский', 'наглый', 'нагло', 'жадный',
    'нечестный', 'мошеннический', 'опасный', 'несовременный', 'уродливый', 'уродливо',
    'неуютный', 'некомфортный', 'тесный', 'темный', 'шумный', 'душный',
    'дорогой', 'дорого', 'завышенный', 'недоступный', 'невыгодный', 'расточительный',
    'непунктуальный', 'опаздывает', 'неоперативный', 'просроченный',
    'разочарован', 'расстроен', 'злой', 'раздражён', 'возмущён', 'недоволен', 'недовольна',
    'обижен', 'оскорблён', 'обманут', 'обворован',
    'жалоба', 'возмущение', 'ругаться', 'проклинать', 'ненавижу',
    'кошмар', 'ужас', 'позор', 'безобразие', 'беда', 'проблема',
    'отстой', 'фигня', 'ерунда', 'чушь', 'халтура', 'брак', 'барахло',
    'неудачный', 'никакой', 'унылый', 'тоскливый', 'депрессивный',
    'отвратно', 'отвратительно', 'невыносимо', 'уныние', 'провал', 'провально',
    'катастрофа', 'беспредел', 'разгильдяйство', 'непрофессионализм', 'хамство',
    'неудобно', 'неудобный', 'ломаный', 'сломанный', 'битый', 'глючный', 'убитый'
}

neutral_words = {
    'нормально', 'сносный', 'терпимо', 'удовлетворительно', 'приемлемо', 'неплохо',
    'средне', 'посредственно', 'ничего', 'так себе', 'более-менее', 'норм', 'угу',
    'ага', 'неплохой', 'недурно', 'недурной'
}

intensifiers = {
    'очень', 'слишком', 'абсолютно', 'крайне', 'чрезвычайно', 'весьма', 'сильно',
    'реально', 'действительно', 'просто', 'вовсе', 'нисколько', 'невероятно',
    'нереально', 'жутко', 'безумно', 'необычайно', 'особенно', 'предельно'
}

negations = {
    'не', 'ни', 'нет', 'неочень', 'неслишком', 'ниразу', 'несовсем', 'отнюдь',
    'нельзя', 'не стоит', 'не надо', 'не следует', 'не буду', 'не хочу'
}

positive_phrases = [
    'всё отлично', 'всё хорошо', 'всё супер', 'без нареканий',
    'на высшем уровне', 'на высоком уровне', 'всё понравилось',
    'спасибо большое', 'огромное спасибо', 'благодарю вас',
    'очень доволен', 'полностью доволен', 'в восторге',
    'рекомендую всем', 'обязательно вернусь', 'лучший в городе',
    'от души', 'душевно', 'классно провёл время', 'всё чётко'
]

negative_phrases = [
    'всё ужасно', 'полный отстой', 'сплошной обман', 'не рекомендую',
    'больше не приду', 'больше никогда', 'ни в коем случае',
    'к сожалению', 'разочарован полностью', 'очень жаль',
    'ужасное обслуживание', 'отвратительное качество', 'кошмар полный',
    'испортили настроение', 'жалею о потраченном времени', 'зря потратил деньги'
]

# ========== УЛУЧШЕННАЯ ФУНКЦИЯ ТОНАЛЬНОСТИ ==========

def advanced_sentiment(text):
    """
    Определяет тональность текста (positive/neutral/negative) на основе правил,
    расширенных словарей, учёта иронии, риторических вопросов, эмодзи и смешанных конструкций.
    """
    text_low = text.lower()
    original = text  # для анализа регистра и эмодзи

    # --- 0. Эмодзи (простейший детектор) ---
    # Позитивные эмодзи
    if re.search(r'[😊😄😁😂😍🥰👍😋😎🌟🎉]', original):
        # если есть позитивное эмодзи, но в тексте также есть явные негативные слова – не перебиваем, увеличиваем скор позже
        positive_emoji = True
    else:
        positive_emoji = False
    # Негативные эмодзи
    if re.search(r'[😞😔😟😠😡👎😭💩😤]', original):
        negative_emoji = True
    else:
        negative_emoji = False

    # --- 1. Ирония через кавычки (слова в кавычках, которые обычно позитивны) ---
    # Если встречаются слова «лучший», «отличный», «прекрасный», «приятный», «доступный» в кавычках – скорее негатив
    if re.search(r'«(лучш[а-я]+|отличн[а-я]+|прекрасн[а-я]+|приятн[а-я]+|доступн[а-я]+)»', text_low):
        return 'negative'

    # --- 2. Риторические негативные вопросы ---
    negative_questions = [
        r'где тут (качество|обслуживание|порядок)',
        r'разве это (называется|можно назвать)',
        r'это что, шутка',
        r'зачем сюда идти',
        r'как можно так плохо',
        r'что за (ужас|безобразие)',
        r'ну и как вам такое',
        r'что это такое',
        r'вы серьезно',
        r'это нормально\?',
        r'почему так плохо',
        r'когда это исправят',
        r'за что платить'
    ]
    for q in negative_questions:
        if re.search(q, text_low):
            return 'negative'

    # --- 3. Саркастические конструкции "отлично, но ..." ---
    if re.search(r'(отлично|прекрасно|супер|класс|здорово|великолепно).*?(но|однако|только не здесь|а вот|при этом)', text_low):
        return 'negative'

    # --- 4. Устойчивые фразы (приоритет) ---
    for phrase in positive_phrases:
        if phrase in text_low:
            return 'positive'
    for phrase in negative_phrases:
        if phrase in text_low:
            return 'negative'

    # --- 5. Специальные замены слов с "не" ---
    text_low = re.sub(r'\bнеплох[а-я]*\b', 'хорошо', text_low)
    text_low = re.sub(r'\bнедурн[а-я]*\b', 'хорошо', text_low)
    text_low = re.sub(r'\bнеплохо\b', 'хорошо', text_low)
    text_low = re.sub(r'\bне фонтан\b', 'плохо', text_low)
    text_low = re.sub(r'\bне айс\b', 'плохо', text_low)

    # --- 6. Разбивка на слова (с дефисами) ---
    words = re.findall(r'\b[а-яё]+(?:-[а-яё]+)?\b', text_low)

    score = 0
    i = 0
    n = len(words)

    while i < n:
        w = words[i]
        # Пропускаем короткие слова, кроме значимых
        if len(w) <= 2 and w not in negations and w not in intensifiers:
            i += 1
            continue

        # Обработка "не очень", "не слишком"
        if w == 'не' and i+1 < n and words[i+1] in intensifiers:
            i += 2
            if i < n:
                nxt = words[i]
                if nxt in positive_words:
                    score -= 1
                elif nxt in negative_words:
                    score += 1
            continue

        # Обработка "ни разу не", "нисколько не", "вовсе не"
        if w in {'ни', 'вовсе'} and i+2 < n and words[i+1] == 'не':
            i += 2
            if i < n:
                nxt = words[i]
                if nxt in positive_words:
                    score -= 2    # сильное отрицание
                elif nxt in negative_words:
                    score += 2
            continue

        # Обработка "очень даже" (усиление)
        if w == 'очень' and i+1 < n and words[i+1] == 'даже':
            i += 2
            if i < n:
                nxt = words[i]
                if nxt in positive_words:
                    score += 2
                elif nxt in negative_words:
                    score -= 2
            continue

        # Простое отрицание
        if w in negations:
            i += 1
            if i < n:
                nxt = words[i]
                weight = 1
                if nxt in intensifiers and i+1 < n:
                    weight = 2
                    i += 1
                    nxt = words[i]
                if nxt in positive_words:
                    score -= weight
                elif nxt in negative_words:
                    score += weight
            continue

        # Усилители без отрицания
        weight = 1
        if w in intensifiers and i+1 < n:
            weight = 2
            i += 1
            w = words[i]

        # Нейтральные слова
        if w in neutral_words:
            i += 1
            continue

        # Позитив/негатив
        if w in positive_words:
            score += weight
        elif w in negative_words:
            score -= weight

        i += 1

    # --- 7. Учёт эмодзи (независимо от скора) ---
    if positive_emoji and not negative_emoji:
        score += 1
    elif negative_emoji and not positive_emoji:
        score -= 1

    # --- 8. Учёт восклицательных знаков (усиление) ---
    exclam = text.count('!')
    if re.search(r'[:;]-?[)d]', text):
        exclam += 1
    if re.search(r'[:;]-?[(]', text):
        exclam -= 1
    if score != 0 and exclam != 0:
        score += score * 0.2 * exclam

    # --- 9. Финальное решение ---
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        # Проверка на наличие только позитивных или только негативных слов
        has_pos = any(w in positive_words for w in words)
        has_neg = any(w in negative_words for w in words)
        if has_pos and not has_neg:
            return 'positive'
        elif has_neg and not has_pos:
            return 'negative'
        else:
            return 'neutral'

# ========== МОДЕЛИ ==========

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Enterprise(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название предприятия")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="enterprises")
    address = models.TextField(blank=True, verbose_name="Адрес")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"

class Review(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, verbose_name="Предприятие", related_name="reviews")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка (1-5)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    sentiment = models.CharField(max_length=10, blank=True, null=True, verbose_name="Тональность",
                                 choices=[('positive', 'Позитивный'), ('neutral', 'Нейтральный'), ('negative', 'Негативный')])
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено")

    def save(self, *args, **kwargs):
        if not self.sentiment:
            self.sentiment = advanced_sentiment(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв о {self.enterprise.name} - {self.rating}★"
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']