from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        marvel_team = {'name': 'Team Marvel'}
        dc_team = {'name': 'Team DC'}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        activities = [
            {'user_id': user_ids[0], 'activity': 'Running', 'duration': 30},
            {'user_id': user_ids[1], 'activity': 'Cycling', 'duration': 45},
            {'user_id': user_ids[2], 'activity': 'Swimming', 'duration': 60},
            {'user_id': user_ids[3], 'activity': 'Yoga', 'duration': 50},
        ]
        db.activities.insert_many(activities)

        leaderboard = [
            {'user_id': user_ids[0], 'score': 100},
            {'user_id': user_ids[1], 'score': 90},
            {'user_id': user_ids[2], 'score': 110},
            {'user_id': user_ids[3], 'score': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        workouts = [
            {'name': 'Full Body Workout', 'difficulty': 'Medium'},
            {'name': 'Cardio Blast', 'difficulty': 'Hard'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
