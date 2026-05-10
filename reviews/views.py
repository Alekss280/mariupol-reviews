from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Review, Category, Enterprise
from .forms import ReviewForm

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