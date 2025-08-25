from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Movie, Newsletter
import matplotlib.pyplot as plt
import io
import matplotlib
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Paola Vallejo'})

    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')


def signup(request):
    """Vista que renderiza el template signup.html y procesa el formulario"""
    if request.method == 'POST':
        email = request.GET.get('email')
        # Aquí procesas el email (guardarlo en base de datos, enviar confirmación, etc.)
        # Por ahora solo renderizamos el template con el email
        return render(request, 'signup.html', {'email': email})
    
    # Si es GET, solo mostrar el template
    return render(request, 'signup.html')


def statistics_view(request):
    matplotlib.use('Agg')
    
    # Obtener todas las películas
    all_movies = Movie.objects.all()
    
    # Crear un diccionario para almacenar la cantidad de películas por año
    movie_counts_by_year = {}
    
    # Filtrar las películas por año y contar la cantidad de películas por año
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1
    
    # Crear la gráfica de barras por año
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Gráfica por año
    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))
    
    ax1.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')
    ax1.set_title('Movies per year', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of movies')
    ax1.set_xticks(bar_positions)
    ax1.set_xticklabels(movie_counts_by_year.keys(), rotation=45)
    
    # Crear un diccionario para almacenar la cantidad de películas por género
    movie_counts_by_genre = {}
    
    # Filtrar las películas por género (solo el primer género)
    for movie in all_movies:
        # Asumiendo que el campo de género se llama 'genre' y puede contener múltiples géneros separados por comas
        if hasattr(movie, 'genre') and movie.genre:
            # Tomar solo el primer género (antes de la primera coma)
            first_genre = movie.genre.split(',')[0].strip()
            if first_genre in movie_counts_by_genre:
                movie_counts_by_genre[first_genre] += 1
            else:
                movie_counts_by_genre[first_genre] = 1
        else:
            # Si no tiene género, categorizarlo como "Unknown"
            if "Unknown" in movie_counts_by_genre:
                movie_counts_by_genre["Unknown"] += 1
            else:
                movie_counts_by_genre["Unknown"] = 1
    
    # Gráfica por género
    genre_positions = range(len(movie_counts_by_genre))
    colors = plt.cm.Set3(range(len(movie_counts_by_genre)))  # Colores variados para cada género
    
    ax2.bar(genre_positions, movie_counts_by_genre.values(), width=bar_width, align='center', color=colors)
    ax2.set_title('Movies per genre', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Genre')
    ax2.set_ylabel('Number of movies')
    ax2.set_xticks(genre_positions)
    ax2.set_xticklabels(movie_counts_by_genre.keys(), rotation=45, ha='right')
    
    # Ajustar el espaciado entre las subgráficas
    plt.tight_layout()
    
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    plt.close()
    
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {
        'graphic': graphic,
        'year_data': movie_counts_by_year,
        'genre_data': movie_counts_by_genre
    })