from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Review, Category, Enterprise
from .forms import ReviewForm
from django.db.models import Count, Avg
import json

def index(request):
    # 1. Получаем все отзывы, упорядоченные по дате (новые сверху)
    reviews_list = Review.objects.all().order_by('-created_at')

    # 2. Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        reviews_list = reviews_list.filter(enterprise__category_id=category_id)

    # 3. Фильтрация по предприятию
    enterprise_id = request.GET.get('enterprise')
    if enterprise_id:
        reviews_list = reviews_list.filter(enterprise_id=enterprise_id)

    # 4. Пагинация (10 отзывов на страницу)
    paginator = Paginator(reviews_list, 10)   # 10 отзывов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 5. Передаём в шаблон также списки категорий и предприятий для выпадающих списков
    categories = Category.objects.all()
    enterprises = Enterprise.objects.all()

    context = {
        'page_obj': page_obj,               # объект страницы для пагинации
        'categories': categories,
        'enterprises': enterprises,
        'selected_category': int(category_id) if category_id else None,
        'selected_enterprise': int(enterprise_id) if enterprise_id else None,
    }
    return render(request, 'reviews/index.html', context)

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})

def stats(request):
    # Общее количество отзывов
    total_reviews = Review.objects.count()
    # Средний рейтинг
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        avg_rating = round(avg_rating, 2)
    else:
        avg_rating = 0
    
    # Распределение оценок (1-5)
    rating_distribution = []
    for i in range(1, 6):
        count = Review.objects.filter(rating=i).count()
        rating_distribution.append({'rating': i, 'count': count})
    
    # Распределение тональностей
    sentiments = ['positive', 'neutral', 'negative']
    sentiment_data = []
    for s in sentiments:
        count = Review.objects.filter(sentiment=s).count()
        sentiment_data.append({'sentiment': s, 'count': count})
    
    # Топ-5 предприятий по количеству отзывов
    top_enterprises = Review.objects.values('enterprise__name').annotate(
        total=Count('id'), 
        avg_rating=Avg('rating')
    ).order_by('-total')[:5]
    
    context = {
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': json.dumps(rating_distribution),
        'sentiment_data': json.dumps(sentiment_data),
        'top_enterprises': top_enterprises,
    }
    return render(request, 'reviews/stats.html', context)

def enterprise_detail(request, enterprise_id):
    enterprise = get_object_or_404(Enterprise, id=enterprise_id)
    # Все отзывы этого предприятия
    reviews_list = enterprise.reviews.all().order_by('-created_at')
    
    # Пагинация (10 отзывов на страницу)
    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Статистика по предприятию
    total_reviews = reviews_list.count()
    avg_rating = reviews_list.aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        avg_rating = round(avg_rating, 2)
    else:
        avg_rating = 0
    
    # Распределение оценок
    rating_distribution = []
    for i in range(1, 6):
        count = reviews_list.filter(rating=i).count()
        rating_distribution.append({'rating': i, 'count': count})
    
    # Распределение тональностей
    sentiment_data = []
    for s in ['positive', 'neutral', 'negative']:
        count = reviews_list.filter(sentiment=s).count()
        sentiment_data.append({'sentiment': s, 'count': count})
    
    context = {
        'enterprise': enterprise,
        'page_obj': page_obj,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': json.dumps(rating_distribution),
        'sentiment_data': json.dumps(sentiment_data),
    }
    return render(request, 'reviews/enterprise_detail.html', context)