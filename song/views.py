from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from .models import Song


# Create your views here.

class SongListView(ListView):
    model = Song
    template_name = 'song/songs_list.html'
    songs = Song.published.all()
    context_object_name = 'songs'

    # paginate_by = 50

    def get_queryset(self):
        queryset = self.model.published.all()
        queryset = queryset.order_by('index')
        search_term = self.request.GET.get('search', '')
        if search_term:

            if search_term.isdigit():
                queryset = queryset.filter(
                    Q(number__exact=search_term)
                )
            else:
                queryset = queryset.filter(
                    Q(title__icontains=search_term) |
                    Q(body__icontains=search_term) |
                    Q(slug__icontains=search_term)
                )

            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(number__icontains=search_term) |
                Q(body__icontains=search_term) |
                Q(slug__icontains=search_term)
            )


        category = self.kwargs.get('category', None)  # Get the category from the URL kwargs
        if category:
            queryset = queryset.filter(category=category)  # Filter by category if present
        return queryset


class SongDetailView(DetailView):
    model = Song
    template_name = 'song/songs_lyrics.html'
    context_object_name = 'song'

    def get_object(self):
        song_Number = self.kwargs.get("number")
        slug = self.kwargs.get("slug")

        post = get_object_or_404(Song, number=song_Number, slug=slug)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_song_number = self.get_object().number
        context['next_song'] = Song.objects.filter(number__gt=current_song_number, status=Song.Status.PUBLISHED).order_by('number').first()
        context['prev_song'] = Song.objects.filter(number__lt=current_song_number, status=Song.Status.PUBLISHED).order_by('-number').first()
        return context


class SongUpdateView(UpdateView):
    model = Song
    fields = '__all__'
    template_name = 'song/song_edit.html'


class SongDeleteView(DeleteView):
    model = Song
    template_name = 'song/song_delete.html'
    success_url = '/'


class SongCreateView(CreateView):
    model = Song
    fields = '__all__'
    template_name = 'song/song_add.html'
    success_url = '/'


def category_list(request):
    categories = Song.CATEGORY_CHOICES
    return render(request, 'song/category.html', {'categories': categories})


class DraftListView(ListView):
    model = Song
    template_name = 'song/draft_list.html'
    context_object_name = 'draft_songs'

    def get_queryset(self):
        queryset = self.model.objects.filter(status=Song.Status.DRAFT)
        queryset = queryset.order_by('index')


        return queryset


class ContactTemplateView(TemplateView):
    template_name = 'details/contact.html'

class PrefaceTemplateView(TemplateView):
    template_name = 'details/preface.html'



