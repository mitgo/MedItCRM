from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    )
    password2 = forms.CharField(
        label=_("Подтверждение"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пользователь'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пользователь'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Новый пароль'
    }), label="Новый пароль")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение'
    }), label="Подтверждение")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Старый пароль'
    }), label='Старый пароль')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Новый пароль'
    }), label="Новый пароль")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение'
    }), label="Подтверждение")