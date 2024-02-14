from django.urls import path
from .views import SongListView, SongDetailView, SongUpdateView, SongDeleteView, SongCreateView, category_list, DraftListView, ContactTemplateView, PrefaceTemplateView

urlpatterns = [
    path('', SongListView.as_view(), name='song_list'),
    path('', SongListView.as_view(), name='home'),
    path('<int:number>/<slug:slug>', SongDetailView.as_view(), name='song_detail'),
    path('<int:number>/<slug:slug>/edit', SongUpdateView.as_view(), name='song_update'),
    path('new/', SongCreateView.as_view(), name='song_create'),
    path('<int:number>/<slug:slug>/delete', SongDeleteView.as_view(), name='song_delete'),
    path('categories/', category_list, name='category_list'),  # Path for listing categories
    path('category/<category>/', SongListView.as_view(), name='songs_by_category'),  # Path for filtered song list
    path('drafts/', DraftListView.as_view(), name='draft_list'),  # Path for listing drafts



    # Details
    path('contact/', ContactTemplateView.as_view(), name='contact'),
    path('preface/', PrefaceTemplateView.as_view(), name='preface'),

]

