from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import AudioBook


def home_view(request):
    audio_files = AudioBook.objects.all()

    return render(request, 'core/home.html', {
        'audio_files': audio_files,
        'mix_range': range(1, 11),
    })

def search_page(request):
    query = request.GET.get('q', '')
    selected_genres = request.GET.getlist('genre')
    selected_languages = request.GET.getlist('language')

    books = AudioBook.objects.all()

    if query:
        books = books.filter(title__icontains=query)
    if selected_genres:
        books = books.filter(genre__in=selected_genres)
    if selected_languages:
        books = books.filter(language__in=selected_languages)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('partials/search_results.html', {'books': books})
        return JsonResponse({'html': html})

    genre_choices = dict(AudioBook.GENRE_CHOICES).items()
    language_choices = AudioBook.objects.values_list('language', flat=True).distinct()

    return render(request, 'search.html', {
        'books': books,
        'query': query,
        'selected_genres': selected_genres,
        'selected_languages': selected_languages,
        'genre_choices': genre_choices,
        'language_choices': language_choices,
    })



def live_search(request):
    query = request.GET.get('q', '')
    genres = request.GET.getlist('genre')

    results = AudioBook.objects.filter(title__istartswith=query)
    if genres:
        results = results.filter(genre__in=genres)

    books = [{
        'audiobook_id': book.id,
        'title': book.title,
        'artist': book.artist,
        'image': book.image.url
    } for book in results]

    return JsonResponse({'books': books})
