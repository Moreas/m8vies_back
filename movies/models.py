from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models import CharField
from django.db.models.functions import Length

CharField.register_lookup(Length, 'length')

class Genre(models.Model):
  name = models.CharField(max_length=50, null=True)
  tmdb_id = models.IntegerField(null=True)

class Country(models.Model):
  name = models.CharField(max_length=50, null=True)
  iso_code = models.CharField(max_length=10, null=True)

class Movie(models.Model):
  title = models.CharField(max_length=200, null=True)
  tmdb_id = models.IntegerField(null=True, unique=True)
  countries = models.ManyToManyField(Country, default=None)
  adult = models.BooleanField(default=False)
  poster_url = models.CharField(max_length=50, null=True)
  genres = models.ManyToManyField(Genre, default=None)
  release_date = models.DateField(null=True)
  vote_average = models.DecimalField(max_digits=4,decimal_places=1, null=True)
  vote_count = models.IntegerField(null=True)
  video = models.BooleanField(default=False)
  overview = models.CharField(max_length=5000, null=True)
  original_language = models.CharField(max_length=20, null=True)
  popularity = models.DecimalField(max_digits=10,decimal_places=2, null=True)
  duration = models.IntegerField(null=True)
  backdrop_url = models.CharField(max_length=50, null=True)
  trailer_key = models.CharField(max_length=50, null=True)

  @property
  def genres_list(self):
    genres = self.genres.first().name
    first = self.genres.first().id
    for genre in self.genres.exclude(id=first):
      genres += ", " + genre.name
    return genres

  @property
  def poster_url_small(self):
    return "https://image.tmdb.org/t/p/w154"+ self.poster_url

  @property
  def poster_url_large(self):
    return "https://image.tmdb.org/t/p/w780"+ self.poster_url

  @property
  def year(self):
    return int(self.release_date.strftime('%Y'))


class User(AbstractUser):
  favorite_movies = models.ManyToManyField(Movie, default=None, related_name='followers')

  @property
  def fav_movies_list(self):
    list = []
    for movie in self.favorite_movies.all():
      list.append(movie.id)
    return list



