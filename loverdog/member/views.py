from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login  # login 함수의 이름을 변경

from .forms import SignUpForm
from .models import UserProfile


# Create your views here.


def index(request):
    return render(request, 'member/loginOrJoin.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile_picture = form.cleaned_data['profile_picture']
            UserProfile.objects.create(user=user, profile_picture=profile_picture)
            auth_login(request, user)  # 변경된 login 함수명으로 수정
            return redirect('/member/home')  # 회원가입 후 리다이렉션할 URL
    else:
        form = SignUpForm()
    return render(request, 'member/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # 변경된 login 함수명으로 수정
            return redirect('/member/home')  # 로그인 후 리다이렉션할 URL
    else:
        form = AuthenticationForm()
    return render(request, 'member/login.html', {'form': form})


# def home(request):
#     return render(request, 'member/home.html')

@login_required
def home(request):
    profile = request.user.userprofile  # 로그인한 사용자의 프로필 정보 가져오기
    return render(request, 'member/home.html', {'profile': profile})
