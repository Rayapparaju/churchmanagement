from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegisterForm, ChurchInfoForm
from .models import ChurchInfo
from members.models import Member
from attendance.models import Attendance
from offerings.models import Offering
from events_app.models import Event
from sermons.models import Sermon
from prayers.models import PrayerRequest
from notices.models import Notice
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Grace Community Church, {user.username}!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def church_info_view(request):
    info = ChurchInfo.get_info()
    return render(request, 'accounts/church_info.html', {'info': info})


@login_required
def church_info_edit(request):
    info = ChurchInfo.get_info()
    if request.method == 'POST':
        form = ChurchInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Church information updated successfully.')
            return redirect('church_info')
    else:
        form = ChurchInfoForm(instance=info)
    return render(request, 'accounts/church_info_form.html', {'form': form, 'info': info})


@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    context = {
        'total_members': Member.objects.count(),
        'total_events': Event.objects.filter(date__gte=today).count(),
        'total_offerings': Offering.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_sermons': Sermon.objects.count(),
        'recent_members': Member.objects.order_by('-created_at')[:5],
        'upcoming_events': Event.objects.filter(date__gte=today).order_by('date', 'time')[:5],
        'recent_offerings': Offering.objects.order_by('-date')[:5],
        'pending_prayers': PrayerRequest.objects.filter(status='pending').count(),
        'active_notices': Notice.objects.filter(is_active=True).count(),
        'weekly_attendance': Attendance.objects.filter(date__gte=week_ago).count(),
        'weekly_offerings': Offering.objects.filter(date__gte=week_ago).aggregate(Sum('amount'))['amount__sum'] or 0,
        'role': profile.role,
    }

    if profile.role == 'admin':
        template = 'accounts/admin_dashboard.html'
    elif profile.role == 'pastor':
        template = 'accounts/pastor_dashboard.html'
    elif profile.role == 'staff':
        template = 'accounts/staff_dashboard.html'
    else:
        template = 'accounts/member_dashboard.html'

    return render(request, template, context)
