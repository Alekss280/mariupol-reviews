from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def index(request):
    """Главная страница со списком отзывов (последние сверху)"""
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/index.html', {'reviews': reviews})

def add_review(request):
    """Страница добавления анонимного отзыва"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')   # после сохранения перенаправляем на главную
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})