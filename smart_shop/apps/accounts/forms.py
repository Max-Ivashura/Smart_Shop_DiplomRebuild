import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from apps.accounts.models import CustomUser


class LoginForm(AuthenticationForm):
    """Форма входа с кастомизацией под новую модель"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин или Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с email как обязательным полем"""
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Логин',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для всех полей
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class CustomUserForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'birth_date',
            'avatar'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (___) ___-__-__',
                'data-mask': '+7 (999) 999-99-99'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',  # Важно для HTML5-календаря
                'class': 'form-control'
            },
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'address': 'Адрес',
            'avatar': 'Аватар',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and avatar.size > 2 * 1024 * 1024:  # 2MB
            raise forms.ValidationError("Максимальный размер файла - 2 МБ")
        return avatar

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Старая логика форматирования
            phone = re.sub(r'\D', '', phone)
            if len(phone) == 11 and phone.startswith(('7', '8')):
                return f'+7{phone[1:]}'
            elif len(phone) == 10 and phone.startswith('9'):
                return f'+7{phone}'
            else:
                raise forms.ValidationError("Номер должен быть в формате +7XXXXXXXXXX")
        return phone
