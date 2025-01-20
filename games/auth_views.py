# games/auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Otomatik olarak UserProfile oluştur
            UserProfile.objects.create(
                user=user,
                nickname=user.username
            )
            # Kullanıcıyı otomatik olarak giriş yaptır
            login(request, user)
            messages.success(request, 'Kayıt başarılı! Hoş geldiniz!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.success(request, 'Başarıyla giriş yaptınız!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Kullanıcı adı veya şifre hatalı!')
        else:
            messages.error(request, 'Lütfen kullanıcı adı ve şifre giriniz!')
            
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    #messages.info(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')