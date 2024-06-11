from django.shortcuts import render, redirect
from main.forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout

from django.contrib.auth import views as auth_views
# Create your views here.


def index(request):
    context = {

    }
    # return redirect('ecp:index')
    return render(request, 'pages/index.html', context)


def profile(request):
    context = {
        'parent': 'pages',
        'segment': 'profile'
    }
    return render(request, 'pages/examples/profile.html', context)
# Authentication


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Учетная запись создана успешно!')
            return redirect('/accounts/login/')
        else:
            print("Ошибки при регистрации!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'


class UserPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/forgot-password.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/recover-password.html'
    form_class = UserSetPasswordForm


def user_logout_view(request):
    logout(request)
    return redirect('/accounts/login/')
