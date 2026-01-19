from django.core.management.base import BaseCommand
from octofit_tracker import models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data in correct order to avoid FK and unhashable errors
        for model in [models.Leaderboard, models.Activity, models.Workout, models.User, models.Team]:
            try:
                model.objects.all().delete()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Could not delete {model.__name__}: {e}"))


        # Create Teams
        marvel = models.Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = models.Team.objects.create(name='DC', description='DC superheroes')

        # Create Users (team is a CharField, so use team name)
        tony = models.User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel.name)
        steve = models.User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel.name)
        bruce = models.User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc.name)
        clark = models.User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc.name)

        from datetime import date
        today = date.today()

        # Create Activities (use correct field names)
        models.Activity.objects.create(user=tony, activity_type='Run', duration=30, date=today)
        models.Activity.objects.create(user=steve, activity_type='Swim', duration=45, date=today)
        models.Activity.objects.create(user=bruce, activity_type='Bike', duration=60, date=today)
        models.Activity.objects.create(user=clark, activity_type='Yoga', duration=50, date=today)

        # Create Workouts (add difficulty field)
        models.Workout.objects.create(name='Avengers HIIT', description='High intensity interval training for Marvel heroes', difficulty='Hard')
        models.Workout.objects.create(name='Justice League Strength', description='Strength training for DC heroes', difficulty='Medium')

        # Create Leaderboard
        models.Leaderboard.objects.create(user=tony, score=1000)
        models.Leaderboard.objects.create(user=steve, score=900)
        models.Leaderboard.objects.create(user=bruce, score=950)
        models.Leaderboard.objects.create(user=clark, score=980)

        self.stdout.write(self.style.SUCCESS('Successfully populated octofit_db with test data'))
