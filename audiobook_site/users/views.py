import json
import random
import string
from django.utils import timezone

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

User = get_user_model()

# Store 2FA codes in memory (use cache/db in production)
pending_2fa = {}

def authentication_page(request):
    return render(request, 'users/authenticate.html')

@csrf_exempt
def authenticate_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'login':
            # fallback, requires code
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
                    # Cleanup session
                    del request.session['2fa_user_id']
                    del request.session['2fa_code']
                    del request.session['2fa_time']
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'error': 'User not found.'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid 2FA code.'})

    return render(request, 'users/login_register.html')


def logout_view(request):
    logout(request)
    return redirect('home')
