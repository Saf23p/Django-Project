from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Distance, Tfcargo


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789-_ '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    # title = forms.CharField(max_length=255,
    #                         min_length=5,
    #                         label='Заголовок',
    #                         validators=[
    #                             RussianValidator()
    #                         ],
    #                         error_messages={
    #                             'min_length': 'Надо больше символов!!!',
    #                             'required': 'Нормально пиши бля'
    #                         },
    #                         widget=forms.TextInput(attrs={'class': 'form_input'}))
    # slug = forms.SlugField(max_length=255,
    #                        label='URL',
    #                        validators=[
    #                            MinLengthValidator(5, message='Минимум 5 символов'),
    #                            MaxLengthValidator(120),
    #                        ]
    #                        )
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    # is_published = forms.BooleanField(required=False, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Категория не выбрана', label='Категории')
    distance = forms.ModelChoiceField(queryset=Distance.objects.all(),
                                      required=False,
                                      empty_label='Выбрать длину',
                                      label='Расстояние')

    class Meta:
        model = Tfcargo #связка формы с моделью
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'row': 5})
        }
        labels = {
            'slug': 'URL'
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Файл')