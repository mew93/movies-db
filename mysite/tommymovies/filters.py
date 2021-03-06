import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
	#name__icontains = django_filters.CharFilter(label='Weaea')
	class Meta:
		model = Movie
		fields = {
			'name': ['icontains'],
			'year': ['gte', 'lte'],
			'p_rating': ['gte', 'lte'],
			'imdb_rating': ['gte', 'lte'],
			'rt_rating': ['gte', 'lte'],
			'watch_date': ['gte', 'lte'],
			'id': ['exact','gte', 'lte'],
			'categories': ['exact','icontains']
		}

	def __init__(self, *args, **kwargs):
		super(MovieFilter, self).__init__(*args, **kwargs)
		self.filters['name__icontains'].label = 'Name'
		self.filters['year__gte'].label = 'Year >='
		self.filters['year__lte'].label = 'Year <='
		self.filters['p_rating__gte'].label = 'Personal >='
		self.filters['p_rating__lte'].label = 'Personal <='
		self.filters['imdb_rating__gte'].label = 'IMDB >='
		self.filters['imdb_rating__lte'].label = 'IMDB <='
		self.filters['rt_rating__gte'].label = 'RT >='
		self.filters['rt_rating__lte'].label = 'RT <='
		self.filters['watch_date__gte'].label = 'Date Watched >='
		self.filters['watch_date__lte'].label = 'Date Watched <='
		self.filters['id'].label = 'ID'
		self.filters['id__gte'].label = 'ID >='
		self.filters['id__lte'].label = 'ID <='
		self.filters['categories__icontains'].label = 'Genre 1'
		self.filters['categories'].label = 'Genre 2'
