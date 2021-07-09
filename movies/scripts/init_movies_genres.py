import os, sys, http.client, json

# This is so Django knows where to find stuff.
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "french_movies_back.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from movies.models import Movie, Genre

movies = Movie.objects.all()
print(movies.count())
for movie in movies:
  id = str(movie.tmdb_id)
  conn = http.client.HTTPSConnection('api.themoviedb.org')
  conn.request("GET", "/3/movie/"+id+"?api_key=916148434132d657d3384d37192fcb41")
  res = conn.getresponse()
  data = res.read()
  items = json.loads(data)
  for genre in items["genres"]:
    movie_genre = Genre.objects.get(tmdb_id=genre["id"])
    movie.genres.add(movie_genre)
    movie.save()