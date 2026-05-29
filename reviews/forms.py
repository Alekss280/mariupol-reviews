from django import forms
from .models import Review, Enterprise
from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha.widgets import MathCaptchaWidget

class ReviewForm(forms.ModelForm):
    # Параметры капчи передаём в виджет
    captcha = MathCaptchaField(
        widget=MathCaptchaWidget(
            question_tmpl="Решите пример: %(num1)i %(operator)s %(num2)i = ?",
        ),
        error_messages={
            'invalid': 'Пожалуйста, решите пример правильно.',
            'invalid_number': 'Пожалуйста, введите целое число.'
        }
    )

    class Meta:
        model = Review
        fields = ['enterprise', 'text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Напишите ваш отзыв...'}),
            'enterprise': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'{i} звезд') for i in range(1, 6)]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сортируем предприятия по названию (алфавит)
        self.fields['enterprise'].queryset = Enterprise.objects.order_by('name')