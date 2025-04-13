import json
import random
import string
import datetime

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from core.models import AudioBook
from users.forms import ProfileForm
from .models import Profile
from .forms import EditProfileForm

User = get_user_model()

pending_2fa = {}

def authentication_page(request):
    return render(request, 'users/authenticate.html')

@csrf_exempt
def authenticate_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        next_url = request.session.get('next', '/')

        if action == 'login':
            return JsonResponse({'success': False, 'error': 'Use the "Send Code" button first.'})

        elif action == 'send_2fa_code':
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                code = ''.join(random.choices(string.digits, k=6))
                request.session['2fa_user_id'] = user.id
                request.session['2fa_code'] = code
                request.session['2fa_time'] = str(timezone.now())
                request.session['next'] = request.META.get('HTTP_REFERER', '/')
                print(f'[2FA CODE for {user.username}]: {code}')
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Invalid credentials.'})

        elif action == 'verify_2fa':
            user_id = request.session.get('2fa_user_id')
            code_sent = request.session.get('2fa_code')
            code_input = data.get('code')

            if str(code_input).strip() == str(code_sent).strip():
                user = User.objects.filter(id=user_id).first()
                if user:
                    login(request, user)
                    next_url = request.session.pop('next', '/')
                    request.session.pop('2fa_user_id', None)
                    request.session.pop('2fa_code', None)
                    request.session.pop('2fa_time', None)
                    return JsonResponse({'success': True, 'next': next_url})
                return JsonResponse({'success': False, 'error': 'User not found.'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid 2FA code.'})

        elif action == 'register':
            username = data.get('username')
            email = data.get('email')
            password1 = data.get('password1')
            password2 = data.get('password2')

            if password1 != password2:
                return JsonResponse({'success': False, 'error': 'Passwords do not match.'})
            if len(password1) < 8:
                return JsonResponse({'success': False, 'error': 'Password must be at least 8 characters.'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'error': 'Username already exists.'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email already registered.'})

            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            next_url = request.session.pop('next', '/')
            return JsonResponse({'success': True, 'next': next_url})

    # Store referrer when GET is accessed
    request.session['next'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'users/login_register.html')


def logout_view(request):
    next_url = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return redirect(next_url)


def format_time(seconds):
    return str(datetime.timedelta(seconds=seconds))


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    total_listening_time = profile.total_listening_time

    hours = total_listening_time // 3600
    remaining_seconds = total_listening_time % 3600
    minutes = remaining_seconds // 60
    remaining_seconds = remaining_seconds % 60

    context = {
        'profile': profile,
        'hours': hours,
        'minutes': minutes,
        'seconds': remaining_seconds,
        'completed_audiobooks_count': profile.completed_audiobooks.count()
    }

    return render(request, 'users/profile.html', context)


@login_required
def get_completed_count(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    count = request.user.profile.completed_audiobooks.count()
    return JsonResponse({'count': count})


@login_required
def edit_profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = EditProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile_view': user_profile})


@csrf_exempt
def update_listening_time(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seconds = int(data.get('seconds', 0))
            audiobook_id = data.get('audiobook_id')

            print(f"Received update: {seconds} seconds, audiobook: {audiobook_id}")  # Debug log

            if request.user.is_authenticated:
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.total_listening_time += seconds
                profile.save()

                if audiobook_id:
                    try:
                        audiobook = AudioBook.objects.get(id=audiobook_id)
                        if not profile.completed_audiobooks.filter(id=audiobook_id).exists():
                            profile.completed_audiobooks.add(audiobook)
                            print(f"Added audiobook {audiobook_id} to completed list")  # Debug log
                        else:
                            print("Audiobook already in completed list")  # Debug log
                    except AudioBook.DoesNotExist:
                        print(f"Audiobook {audiobook_id} not found")  # Debug log

                new_count = profile.completed_audiobooks.count()
                print(f"New completed count: {new_count}")  # Debug log

                return JsonResponse({
                    'status': 'success',
                    'new_count': new_count
                })
            else:
                return JsonResponse({'status': 'unauthenticated'}, status=401)

        except Exception as e:
            print(f"Error in update_listening_time: {str(e)}")  # Debug log
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def user_library(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    completed_books = profile.completed_audiobooks.all()

    context = {
        'completed_books': completed_books,
    }
    return render(request, 'users/library.html', context)
