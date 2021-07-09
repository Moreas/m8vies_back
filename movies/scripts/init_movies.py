import os, sys, http.client, json

# This is so Django knows where to find stuff.
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "french_movies_back.settings")

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from movies.models import Movie, Genre

movies = Movie.objects.all()
for movie in movies:
  movie.delete()
conn = http.client.HTTPSConnection('api.themoviedb.org')
conn.request("GET", "/3/movie/top_rated?api_key=916148434132d657d3384d37192fcb41")
res = conn.getresponse()
data = res.read()
items = json.loads(data)
pages = range(int(items['total_pages']))
for page in pages:
  conn.request("GET", "/3/movie/top_rated?api_key=916148434132d657d3384d37192fcb41&page="+str(page + 1))
  res = conn.getresponse()
  data = res.read()
  items = json.loads(data)
  for item in items["results"]:
    title = item['title']
    tmdb_id = int(item['id'])
    adult = item['adult']
    poster_url = item['poster_path']
    movie = Movie(title=title,tmdb_id=tmdb_id,adult=adult,poster_url=poster_url)
    movie.save()
