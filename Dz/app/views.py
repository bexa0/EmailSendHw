import random

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.models import Key


# Create your views here.
def index(request):
    return render(request, 'index.html')

class SignUp(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().get(request, *args, **kwargs)


class LoginForm(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('index')

def user_logout(request):
    logout(request)
    return redirect('index')



def enter_your_ligin(request):
    if request.method == 'POST':
        if User.objects.get(username=request.POST['login']):
            return redirect('send_message', username=request.POST['login'])
        else:
            return redirect('some_error_occurred')
    return render(request, 'enter_your_login.html')


def send_message(request, username):
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z',
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    key = ''.join(str(i) for i in [random.choice(keys) for i in range(8)])

    user = User.objects.get(username=username)
    if user:
        Key.objects.create(user=user, key=key)
        email = EmailMessage(
            f"hi",
            f"{Key.objects.filter(user=user)}",
            "from@example.com",
            [user.email],
            ["bcc@example.com"],
            reply_to=["another@example.com"],
            headers={"Message-ID": "foo"},
        )
        email.send()
        return redirect('confirm_page', username=username)
    else:
        return redirect('some_error_occurred')

def confrim_page(request, username):
    user = User.objects.get(username=username)
    if request.method == "POST":
        if request.POST['key'] in [i.key for i in Key.objects.filter(user=user)]:
            Key.objects.filter(user=user).delete()
            return redirect('repassword', username=username)
        else:
            return redirect('index')
    return render(request, 'confrim_page.html')

def repassword(request, username):
    if request.method == "POST":
        if request.POST['pass1'] == request.POST['pass2']:
            user = User.objects.get(username=username)
            user.set_password(request.POST['pass1'])
            user.save()
            return redirect('login')
        else:
            return redirect('some_error_occurred')
    return render(request, 'repassword.html')


def some_error_occurred(request):
    return render(request, 'error_page.html')