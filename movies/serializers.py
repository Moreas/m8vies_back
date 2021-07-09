from rest_framework import serializers
from movies.models import Genre, Movie, User

class GenreSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Genre
    fields='__all__'

class MoviesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields=('id', 'title', 'poster_url_small', 'genres_list', 'vote_average')

class MovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields=('id', 'title', 'poster_url_large', 'genres_list', 'overview','year', 'duration', 'tmdb_id', 'trailer_key', 'vote_average')

class FeaturedMovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields=('id', 'title', 'backdrop_url')

class FavMovieSerializer(serializers.ModelSerializer):
  class Meta:
    model = Movie
    fields=('id',)

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=('username','fav_movies_list')