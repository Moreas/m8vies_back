import os, sys, http.client, json

# This is so Django knows where to find stuff.
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "french_movies_back.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from movies.models import Movie, Country

movies = Movie.objects.all()
countries = Country.objects.all()
for country in countries:
  country.delete()
print(movies.count())
for movie in movies:
  id = str(movie.tmdb_id)
  conn = http.client.HTTPSConnection('api.themoviedb.org')
  conn.request("GET", "/3/movie/"+id+"?api_key=916148434132d657d3384d37192fcb41")
  res = conn.getresponse()
  data = res.read()
  items = json.loads(data)
  for country in items["production_countries"]:
    print(country)
    if Country.objects.filter(iso_code=country["iso_3166_1"]).exists():
      movie_country = Country.objects.get(iso_code=country["iso_3166_1"])
    else:
      movie_country = Country(iso_code=country["iso_3166_1"],name=country["name"])
      movie_country.save()
    movie.countries.add(movie_country)
    movie.save()