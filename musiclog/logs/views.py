import csv
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_datetime
from rest_framework import generics
from .models import MusicLog
from .serializers import MusicLogSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SongListView(generics.ListAPIView):
    queryset = MusicLog.objects.all()
    serializer_class = MusicLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['artist', 'program', 'dj', 'timestamp']
    search_fields = ['song_title', 'artist']


class SongDetailView(generics.RetrieveAPIView):
    queryset = MusicLog.objects.all()
    serializer_class = MusicLogSerializer
    lookup_field = 'id'


class ProgramSongsView(generics.ListAPIView):
    serializer_class = MusicLogSerializer

    def get_queryset(self):
        program_name = self.kwargs['program_name']
        queryset = MusicLog.objects.filter(program=program_name)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        return queryset


class DJSongsView(generics.ListAPIView):
    serializer_class = MusicLogSerializer

    def get_queryset(self):
        dj_name = self.kwargs['dj_name']
        queryset = MusicLog.objects.filter(dj=dj_name)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        return queryset


class ArtistSongsView(generics.ListAPIView):
    serializer_class = MusicLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        artist_name = self.kwargs['artist_name']
        queryset = MusicLog.objects.filter(artist=artist_name)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        return queryset


def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return render(request, 'logs/upload.html', {'error': 'This is not a CSV file'})

        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            try:
                timestamp = parse_datetime(row['Timestamp'])
                if not timestamp:
                    return render(request, 'logs/upload.html', {'error': f"Invalid date format in row: {row}"})
                MusicLog.objects.create(
                    timestamp=timestamp,
                    song_title=row['Song Title'],
                    artist=row['Artist'],
                    album=row['Album'],
                    duration=row['Duration'],
                    isrc=row['ISRC'],
                    program=row['Program'],
                    dj=row['DJ']
                )
            except Exception as e:
                return render(request, 'logs/upload.html', {'error': f"Error in row {row}: {str(e)}"})

        return redirect('song-list')  # Redirect to song list after upload success

    return render(request, 'logs/upload.html')


def song_list(request):
    songs = MusicLog.objects.all()

    # Get filter parameters from GET request
    artist = request.GET.get('artist')
    program = request.GET.get('program')
    dj = request.GET.get('dj')
    timestamp = request.GET.get('timestamp')

    # Apply filters if they exist
    if artist:
        songs = songs.filter(artist__icontains=artist)
    if program:
        songs = songs.filter(program__icontains=program)
    if dj:
        songs = songs.filter(dj__icontains=dj)
    if timestamp:
        songs = songs.filter(timestamp__date=timestamp)

    return render(request, 'logs/song_list.html', {'songs': songs})


def dj_songs(request):
    dj_name = request.GET.get('dj')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if dj_name:
        songs = MusicLog.objects.filter(dj__icontains=dj_name)

        # Apply date range filtering if specified
        if start_date and end_date:
            songs = songs.filter(timestamp__range=[start_date, end_date])

        return render(request, 'logs/dj_songs.html', {'songs': songs})

    return render(request, 'logs/dj_songs.html', {'songs': []})
