from django import forms
from .models import Review, Enterprise

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['enterprise', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Напишите ваш отзыв...'}),
            'enterprise': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} звезд') for i in range(1, 6)]),
        }
        labels = {
            'enterprise': 'Предприятие',
            'text': 'Текст отзыва',
            'rating': 'Оценка',
        }