import django_tables2 as tables
from .models import Movie
from django.urls import reverse
from django.conf.urls import url
import views

class MovieTable(tables.Table):
	edit = tables.TemplateColumn('<a href="{% url \'tommymovies:edit\' record.id %}">+</a>', orderable=False, empty_values=())
	delete = tables.TemplateColumn('<a href="{% url \'tommymovies:delete\' record.id %}">-</a>', orderable=False, empty_values=())
	toggle_watched  = tables.TemplateColumn('<a href="{% url \'tommymovies:toggle_watched\' record.id %}">x</a>', orderable=False, empty_values=())
	name = tables.Column(verbose_name= 'Movie' )
	year = tables.Column(verbose_name= 'Year' )
	watched = tables.Column(verbose_name= 'Watched?' )
	watch_date = tables.Column(verbose_name= 'Date Watched' )
	p_rating = tables.Column(verbose_name= 'Personal Rating' )
	imdb_rating = tables.Column(verbose_name= 'IMDB' )
	rt_rating = tables.Column(verbose_name= 'RT' )
	categories = tables.Column(verbose_name= 'Genre')

	class Meta:
		model = Movie
		attrs = {'class': 'paleblue'}

	def render_categories(self, record):
		if record.categories is not None:
			return ', '.join([categories.genre for categories in record.categories.all()])
		return '-'

