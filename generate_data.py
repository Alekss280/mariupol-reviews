import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Настройка Django-окружения для доступа к моделям
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mariupol_portal.settings')
django.setup()

from reviews.models import Category, Enterprise, Review

# ---------- Шаблоны отзывов (чтобы были разными) ----------
# Каждый шаблон содержит {}, куда подставится название предприятия

positive_templates = [
    "{} — отлично! Всё понравилось, особенно обслуживание.",
    "{} работает великолепно. Рекомендую всем.",
    "Спасибо {} за качество! Буду обращаться ещё.",
    "В {} быстро и профессионально. Очень доволен.",
    "{} — лучший в Мариуполе! Так держать."
]

neutral_templates = [
    "{} нормально, без восторгов. В целом удовлетворительно.",
    "В {} всё стандартно. Ничего особенного.",
    "{} — средненько. Могло быть и лучше, но приемлемо.",
    "Первый раз в {}. Впечатление среднее."
]

negative_templates = [
    "{} ужасно. Очень долгое ожидание и грубый персонал.",
    "{} разочаровал. Больше туда ни ногой.",
    "В {} всё плохо: грязно, дорого и невкусно.",
    "Не советую {}. Качество услуг низкое, цены завышены.",
    "{} — отстой. Деньги на ветер."
]

# Список оценок с весами (чтобы чаще попадались хорошие и средние)
ratings_with_weights = [
    (5, 40),   # 5 звёзд с весом 40%
    (4, 30),   # 4 звезды с весом 30%
    (3, 15),   # 3 звезды с весом 15%
    (2, 10),   # 2 звезды с весом 10%
    (1, 5)     # 1 звезда с весом 5%
]

# Функция для выбора оценки с учётом весов
def get_weighted_rating():
    values, weights = zip(*ratings_with_weights)
    return random.choices(values, weights=weights)[0]

# Получаем все предприятия из БД (нужно, чтобы они уже были добавлены в админке)
enterprises = list(Enterprise.objects.all())
if not enterprises:
    print("❌ Нет ни одного предприятия! Сначала добавьте предприятия через админку.")
    exit(1)

print(f"✅ Найдено предприятий: {len(enterprises)}")

# Количество генерируемых отзывов
NUM_REVIEWS = 500   # Можно поставить 200-500

print(f"🔄 Начинаем генерацию {NUM_REVIEWS} синтетических отзывов...")

reviews_created = 0
for _ in range(NUM_REVIEWS):
    enterprise = random.choice(enterprises)
    rating = get_weighted_rating()
    
    # Выбираем шаблон в зависимости от оценки
    if rating >= 4:
        template = random.choice(positive_templates)
    elif rating == 3:
        template = random.choice(neutral_templates)
    else:  # rating 1–2
        template = random.choice(negative_templates)
    
    text = template.format(enterprise.name)
    
    # Случайная дата отзыва — за последние 90 дней
    days_ago = random.randint(0, 90)
    hours_ago = random.randint(0, 23)
    created_at = timezone.now() - timedelta(days=days_ago, hours=hours_ago)
    
    # Создаём отзыв (sentiment рассчитается автоматически при save)
    try:
        review = Review(
            enterprise=enterprise,
            text=text,
            rating=rating,
            created_at=created_at
        )
        review.save()   # здесь сработает метод save модели, который вычислит тональность
        reviews_created += 1
    except Exception as e:
        print(f"⚠️ Ошибка при создании отзыва: {e}")

print(f"Готово! Создано {reviews_created} синтетических отзывов.")