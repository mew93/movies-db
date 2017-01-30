from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Movie, Category
from forms import MovieForm, CategoryForm
from django_datatables_view.base_datatable_view import BaseDatatableView
from django_tables2 import RequestConfig
from tables import MovieTable
from .filters import MovieFilter
from .forms import MovieTableFormHelper
from utils import PagedFilteredTableView

class WatchHistoryView(generic.ListView):
	template_name = 'tommymovies/history.html'
	context_object_name = 'movie_list'
	form_class = CategoryForm

	def get_form(self):
		form = self.form_class()
		return form
	def get_context_data(self, **kwargs):
		context = super(WatchHistoryView, self).get_context_data(**kwargs)
		context.update({
		'category_form': self.get_form(),})
		return context

	def get_queryset(self):
		return Movie.objects.order_by('id')

#class ToWatchListView(generic.ListView):

class MovieDetailView(generic.DetailView):
	model = Movie
	template_name = 'tommymovies/movie.html'
	def get_object(self):
		return get_object_or_404(Movie, pk=self.kwargs['movie_id'])

class MovieEditView(generic.DetailView):
	model = Movie
	template_name = 'tommymovies/edit.html'
	form_class = CategoryForm
	def get_form(self):
		form = self.form_class(instance=self.object)
		return form
	def get_context_data(self, **kwargs):
		context = super(MovieEditView, self).get_context_data(**kwargs)
		context.update({
		'category_form': self.get_form(),
		'object_name':self.object.name, })
		return context
	def get_object(self):
		return get_object_or_404(Movie, pk=self.kwargs['movie_id'])

def add(request):
	if request.method == "POST":
		form = MovieForm(request.POST)
		if form.is_valid():
			new_movie = Movie.objects.create_movie(**form.cleaned_data)
			try:
				genre_id=request.POST.get('genre','')
				new_category = get_object_or_404(Category, id=genre_id)
				new_movie.categories.add(new_category)
			except:
				pass
			new_movie.save()

			return HttpResponseRedirect(reverse('tommymovies:history'))
	else:
		form = MovieForm()

	return render(request, 'tommymovies/add.html', {'form': form })

def delete(request, movie_id):
	movie = get_object_or_404(Movie, id=movie_id)
	try:
		movie.delete()
	except(KeyError, Movie.DoesNotExist):
		return HttpResponseRedirect(reverse('tommymovies:history'))
	else:
		#return HttpResponseRedirect(reverse('tommymovies:history'))
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		
def toggle_watched(request, movie_id):
	movie = get_object_or_404(Movie, id=movie_id)
	if(movie.watched == 0):
		movie.watched = 1
	else:
		movie.watched = 0
	movie.save()
	#return HttpResponseRedirect(reverse('tommymovies:history'))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def edit_submit(request, movie_id):
	movie = get_object_or_404(Movie, id=movie_id)
	if request.method == "POST":
		form = MovieForm(request.POST)
		listgenres= request.POST.getlist('categories')
		for genre in movie.categories.all():
			movie.categories.remove(genre)
		for genre in listgenres:
			try:
				category = get_object_or_404(Category, genre=genre)
			except:
				pass	
			else:
				if genre not in movie.categories.all():
					movie.categories.add(category)
		try:
			genre_id=request.POST.get('genre','')
			new_category = get_object_or_404(Category, id=genre_id)
			movie.categories.add(new_category)
			movie.save()
		except:
			pass

		if form.is_valid():
			movie.name = form.cleaned_data['name']
			movie.year = form.cleaned_data['year']
			movie.watched = form.cleaned_data['watched']
			movie.watch_date = form.cleaned_data['watch_date']
			movie.p_rating = form.cleaned_data['p_rating']
			movie.imdb_rating = form.cleaned_data['imdb_rating']
			movie.rt_rating = form.cleaned_data['rt_rating']
			movie.save()
			return render(request, 'tommymovies/movie.html', {'movie': movie })
	else:
		form = MovieForm(instance=movie)
	#return render(request, 'tommymovies/movie.html', {'movie': movie })
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#table_movie_history replaced by MovieTableView
def table_movie_history(request):
	if request.GET.get('per_page'):
		per_page = request.POST.get('per_page')
	else:
		per_page = 25

	table = MovieTable(Movie.objects.filter(watched=1).order_by('-watch_date'))
	RequestConfig(request,paginate={'per_page': per_page}).configure(table)
	title = 'Movie Watch History'
	return render(request, 'tommymovies/table.html', {'table': table, 'title': title})

#table_to_watch replaced by MovieTableView
def table_to_watch(request):
	if request.GET.get('per_page'):
		per_page = request.POST.get('per_page')
	else:
		per_page = 25

	table = MovieTable(Movie.objects.filter(watched=0).order_by('id'))
	RequestConfig(request,paginate={'per_page': per_page}).configure(table)
	title = 'Movies to Watch'
	return render(request, 'tommymovies/table.html', {'table': table, 'title': title})

class MovieTableView(PagedFilteredTableView):
	title= ''
	watched = ''
	model = Movie
	table_class = MovieTable
	template_name = 'tommymovies/table.html'
	filter_class = MovieFilter
	formhelper_class = MovieTableFormHelper

	def get_queryset(self, **kwargs):
		title = self.title
		qs = super(PagedFilteredTableView, self).get_queryset().filter(watched=self.watched).order_by('id')
		self.filter = self.filter_class(self.request.GET, queryset=qs)
		self.filter.form.helper = self.formhelper_class()
		return self.filter.qs

	def get_context_data(self, **kwargs):
		context = super(PagedFilteredTableView, self).get_context_data()
		context[self.context_filter_name] = self.filter
		context['title'] = self.title
		return context

def addMovie(request):
	movie_form = MovieForm()
	movie_form.fields.pop('categories')
	category_form = CategoryForm()
	return render(request, 'tommymovies/addMovie.html',{'movie_form': movie_form, 'category_form':category_form })

def addMovieSubmit(request):
	if request.method == "POST":
		form = MovieForm(request.POST)
		genre_id=request.POST.get('genre','')
		category = get_object_or_404(Category, id=genre_id)
		if form.is_valid():
			new_movie = Movie.objects.create_movie(form.cleaned_data['name'], form.cleaned_data['year'], form.cleaned_data['watched'], form.cleaned_data['watch_date'], form.cleaned_data['p_rating'], form.cleaned_data['imdb_rating'], form.cleaned_data['rt_rating'])
			new_movie.categories.add(category)
			new_movie.save()
			return HttpResponseRedirect(reverse('tommymovies:history'))
	else:
		form = MovieForm()

	return render(request, 'tommymovies/addMovie.html', {'movie_form': movie_form, 'category_form': category_form })


def addCategory(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			new_category = Category.objects.create(**form.cleaned_data)
			return HttpResponseRedirect(reverse('tommymovies:history'))
	else:
		form = CategoryForm()

	return render(request, 'tommymovies/addCategory.html', {'form': form })

def categorize_form(request):
	form = CategoryForm()
	return render(request, 'tommymovies/categorize.html',{'form': form })

def categorize(request):
	name=request.POST.get('name','')
	genre_id=request.POST.get('genre','')
	movie = get_object_or_404(Movie, name=name)
	category = get_object_or_404(Category, id=genre_id)
	movie.categories.add(category)
	movie.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


		
