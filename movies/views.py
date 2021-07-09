from .models import User, Movie, Country, Genre
from .serializers import GenreSerializer, MovieSerializer, MoviesSerializer, FeaturedMovieSerializer, FavMovieSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
import random, json

class GenrePagination(PageNumberPagination):
  page_size=5


@api_view(['GET'])
def get_genres(request):
  if request.method == 'GET':
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_movies(request):
  if request.method == 'GET':
    category = request.GET.get('category', None)
    country = request.GET.get('country', None)
    sort = request.GET.get('sort', None)
    if category == None or category == 'null' or category == '' or category == 'rating_desc':
      movies = Movie.objects.all()
    else:
      genre = Genre.objects.get(name=category)
      movies = Movie.objects.filter(genres=genre)
    if country == "US":
      country = Country.objects.get(iso_code="US")
      movies = movies.filter(countries=country)
    if country == "UK":
      country = Country.objects.get(iso_code="GB")
      movies = movies.filter(countries=country)
    if country == "French":
      country = Country.objects.get(iso_code="FR")
      movies = movies.filter(countries=country)
    if country == "International":
      country_list = Country.objects.filter(iso_code__in=["US","FR","GB"]).values_list('id', flat=True)
      movies = movies.exclude(countries__in= country_list)
    if sort == None or sort == 'null' or sort == '' or sort == 'rating_desc':
      movies = movies.order_by('-vote_average','id')
    if sort == 'rating_asc':
      movies = movies.order_by('vote_average','id')
    if sort == 'date_asc':
      movies = movies.order_by('release_date','id')
    if sort == 'date_desc':
      movies = movies.order_by('-release_date','id')
    if sort == 'alpha_asc':
      movies = movies.order_by('title','id')
    if sort == 'alpha_desc':
      movies = movies.order_by('-title','id')
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(movies, request)
    serializer = MoviesSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_movie(request,id):
  if request.method == 'GET':
    movie = Movie.objects.get(id=id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_movies(request):
  if request.method == 'GET':
    text = request.GET.get('text', None)
    movies = Movie.objects.filter(title__icontains=text)
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(movies, request)
    serializer = MoviesSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_featured_movie(request):
  if request.method == 'GET':
    random_number = random.randint(0,30)
    movie = Movie.objects.filter(release_date__year=2021).filter(title__length__lt=25).order_by('-vote_average')[random_number]
    serializer = FeaturedMovieSerializer(movie)
    return Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fav_movie(request,id):
  if request.method == 'POST':
    username = json.loads(request.body)['username']
    user = User.objects.get(username=username)
    movie = Movie.objects.get(id=id)
    user.favorite_movies.add(movie)
    movies = Movie.objects.filter(followers__id=user.id)
    serializer = FavMovieSerializer(movies, many=True)
    return  Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def unfav_movie(request,id):
  if request.method == 'POST':
    username = json.loads(request.body)['username']
    user = User.objects.get(username=username)
    movie = Movie.objects.get(id=id)
    user.favorite_movies.remove(movie)
    movies = Movie.objects.filter(followers__id=user.id)
    serializer = FavMovieSerializer(movies, many=True)
    return  Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_user_token(request):
  if request.method == 'POST':
    token = json.loads(request.body)['token']
    try:
      user = Token.objects.get(key=token).user
      serializer = UserSerializer(user)
      return  Response(serializer.data)
    except Token.DoesNotExist:
      return  Response(status=status.HTTP_403_FORBIDDEN)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_auth(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        User.objects.create_user(username=serialized.initial_data['username'],password=serialized.initial_data['password'],email=serialized.initial_data['email'])
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_fav_movies_list(request):
  if request.method == 'POST':
    username = json.loads(request.body)['username']
    user = User.objects.get(username=username)
    movies = user.favorite_movies.all()
    serializer = FavMovieSerializer(movies, many=True)
    return  Response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def get_fav_movies(request):
  if request.method == 'POST':
    username = json.loads(request.body)['username']
    user = User.objects.get(username=username)
    movies = user.favorite_movies.all()
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(movies, request)
    serializer = MoviesSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
  else:
    return Response(status=status.HTTP_400_BAD_REQUEST)