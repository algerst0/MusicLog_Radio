import csv
from django.core.management.base import BaseCommand
from logs.models import MusicLog
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Import music logs from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    timestamp = parse_datetime(row['Timestamp'])
                    if not timestamp:
                        self.stdout.write(self.style.ERROR(f"Invalid date format in row: {row}"))
                        continue
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
                    self.stdout.write(self.style.ERROR(f"Error in row {row}: {str(e)}"))
