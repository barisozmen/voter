from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from polls.models import Poll, Choice
from polls.voting import Vote
import random


class Command(BaseCommand):
    help = 'Seed the database with sample polls and votes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            # Clear votes through custom voting system
            Vote.objects.all().delete()
            Choice.objects.all().delete()
            Poll.objects.all().delete()
            
        # Create or get admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user: admin/admin123')

        # Create some regular users
        users = []
        for i in range(1, 6):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'email': f'user{i}@example.com',
                    'first_name': f'User',
                    'last_name': f'{i}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Sample poll data
        polls_data = [
            {
                'title': 'What\'s your favorite programming language?',
                'description': 'Help us understand what programming languages developers prefer in 2024.',
                'tags': ['programming', 'technology', 'development'],
                'choices': ['Python', 'JavaScript', 'Java', 'Go', 'Rust', 'TypeScript']
            },
            {
                'title': 'Best time for daily standup meetings?',
                'description': 'When do you think daily standup meetings are most effective for team productivity?',
                'tags': ['work', 'productivity', 'meetings'],
                'choices': ['9:00 AM', '10:00 AM', '11:00 AM', '2:00 PM', 'End of day']
            },
            {
                'title': 'Preferred remote work setup',
                'description': 'What\'s your ideal remote work environment? Share your preferences!',
                'tags': ['remote-work', 'productivity', 'lifestyle'],
                'choices': ['Home office', 'Coffee shop', 'Co-working space', 'Hybrid (office + home)', 'Outdoor spaces']
            },
            {
                'title': 'Most important factor when choosing a restaurant',
                'description': 'When you\'re deciding where to eat, what matters most to you?',
                'tags': ['food', 'lifestyle', 'dining'],
                'choices': ['Food quality', 'Price', 'Location', 'Atmosphere', 'Service', 'Reviews/Ratings']
            },
            {
                'title': 'Preferred streaming platform for movies',
                'description': 'Which streaming service do you use most for watching movies?',
                'tags': ['entertainment', 'movies', 'streaming'],
                'choices': ['Netflix', 'Amazon Prime', 'Disney+', 'HBO Max', 'Apple TV+', 'Hulu']
            },
            {
                'title': 'Best day of the week to start a project',
                'description': 'When do you feel most productive to kick off new projects?',
                'tags': ['productivity', 'planning', 'work'],
                'choices': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            }
        ]

        created_polls = []
        
        # Create polls
        for poll_data in polls_data:
            # Randomly assign creator
            creator = random.choice([admin_user] + users)
            
            poll = Poll.objects.create(
                title=poll_data['title'],
                description=poll_data['description'],
                created_by=creator
            )
            
            # Add tags
            for tag_name in poll_data['tags']:
                poll.tags.add(tag_name)
            
            # Create choices
            choices = []
            for choice_text in poll_data['choices']:
                choice = Choice.objects.create(
                    poll=poll,
                    text=choice_text
                )
                choices.append(choice)
            
            created_polls.append((poll, choices))
            self.stdout.write(f'Created poll: {poll.title}')

        # Create some votes using custom voting system
        all_users = [admin_user] + users
        total_votes = 0
        
        for poll, choices in created_polls:
            # Random number of voters (50-90% of users)
            num_voters = random.randint(len(all_users) // 2, int(len(all_users) * 0.9))
            voters = random.sample(all_users, num_voters)
            
            for voter in voters:
                # Random choice
                choice = random.choice(choices)
                # Use custom voting system to create the vote
                choice.votes.up(voter)
                total_votes += 1
            
            self.stdout.write(f'Added {num_voters} votes to: {poll.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Successfully seeded database with:\n'
                f'   • {len(created_polls)} polls\n'
                f'   • {User.objects.count()} users\n'
                f'   • {total_votes} votes (using elegant custom voting system)\n\n'
                f'🔑 Login Credentials:\n'
                f'   Admin: admin/admin123\n'
                f'   Users: user1-user5/password123\n\n'
                f'🚀 Ready to run: python manage.py runserver'
            )
        )