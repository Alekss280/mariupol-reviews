from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count, Avg
import json
from .models import Review, Category, Enterprise
from .forms import ReviewForm

def index(request):
    # Только одобренные отзывы, новые сверху
    reviews_list = Review.objects.filter(is_approved=True).order_by('-created_at')

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        reviews_list = reviews_list.filter(enterprise__category_id=category_id)

    # Фильтрация по предприятию
    enterprise_id = request.GET.get('enterprise')
    if enterprise_id:
        reviews_list = reviews_list.filter(enterprise_id=enterprise_id)

    # Пагинация
    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    enterprises = Enterprise.objects.all()

    context = {
        'page_obj': page_obj,
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
            # Сохраняем отзыв (is_approved=False по умолчанию)
            form.save()
            messages.success(request, 'Спасибо! Ваш отзыв отправлен на модерацию и появится после проверки.')
            return redirect('index')
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})

def stats(request):
    # Работаем только с одобренными отзывами
    approved_reviews = Review.objects.filter(is_approved=True)

    total_reviews = approved_reviews.count()
    avg_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 2) if avg_rating else 0

    rating_distribution = []
    for i in range(1, 6):
        count = approved_reviews.filter(rating=i).count()
        rating_distribution.append({'rating': i, 'count': count})

    sentiment_data = []
    for s in ['positive', 'neutral', 'negative']:
        count = approved_reviews.filter(sentiment=s).count()
        sentiment_data.append({'sentiment': s, 'count': count})

    # ========== НОВАЯ ЧАСТЬ: сортировка топ-10 ==========
    sort_by = request.GET.get('sort', 'count')   # параметр из URL, по умолчанию 'count'

    top_queryset = approved_reviews.values(
        'enterprise__id',
        'enterprise__name',
        'enterprise__address'
    ).annotate(
        total=Count('id'),
        avg_rating=Avg('rating')
    )

    if sort_by == 'rating':
        top_enterprises = top_queryset.order_by('-avg_rating')[:10]
    else:
        top_enterprises = top_queryset.order_by('-total')[:10]

    context = {
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': json.dumps(rating_distribution),
        'sentiment_data': json.dumps(sentiment_data),
        'top_enterprises': top_enterprises,
        'current_sort': sort_by,   # для подсветки активной кнопки в шаблоне
    }
    return render(request, 'reviews/stats.html', context)

def enterprise_detail(request, enterprise_id):
    enterprise = get_object_or_404(Enterprise, id=enterprise_id)
    # Только одобренные отзывы этого предприятия
    reviews_list = enterprise.reviews.filter(is_approved=True).order_by('-created_at')

    paginator = Paginator(reviews_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_reviews = reviews_list.count()
    avg_rating = reviews_list.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 2) if avg_rating else 0

    rating_distribution = []
    for i in range(1, 6):
        count = reviews_list.filter(rating=i).count()
        rating_distribution.append({'rating': i, 'count': count})

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

def map_view(request):
    # Предприятия с координатами
    enterprises = Enterprise.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

    for enterprise in enterprises:
        # Считаем только одобренные отзывы
        reviews_qs = enterprise.reviews.filter(is_approved=True)
        avg_rating = reviews_qs.aggregate(Avg('rating'))['rating__avg']
        enterprise.avg_rating = round(avg_rating, 1) if avg_rating else 0
        enterprise.reviews_count = reviews_qs.count()

    context = {'enterprises': enterprises}
    return render(request, 'reviews/ya_map.html', context)