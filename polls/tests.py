from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Poll, Choice
from .voting import Vote


class PollModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.poll = Poll.objects.create(
            title='Test Poll',
            description='Test Description',
            created_by=self.user
        )
        self.choice1 = Choice.objects.create(poll=self.poll, text='Choice 1')
        self.choice2 = Choice.objects.create(poll=self.poll, text='Choice 2')
    
    def test_poll_str(self):
        self.assertEqual(str(self.poll), 'Test Poll')
    
    def test_poll_get_absolute_url(self):
        url = reverse('polls:detail', kwargs={'pk': self.poll.pk})
        self.assertEqual(self.poll.get_absolute_url(), url)
    
    def test_poll_total_votes(self):
        self.assertEqual(self.poll.total_votes, 0)
        
        # Use custom voting system to create a vote
        self.choice1.votes.up(self.user)
        self.assertEqual(self.poll.total_votes, 1)
    
    def test_choice_vote_count(self):
        self.assertEqual(self.choice1.votes.count(), 0)
        
        # Use django-vote to create a vote
        self.choice1.votes.up(self.user)
        self.assertEqual(self.choice1.votes.count(), 1)
    
    def test_poll_user_vote(self):
        # User hasn't voted yet
        self.assertIsNone(self.poll.user_vote(self.user))
        
        # User votes for choice1
        self.choice1.votes.up(self.user)
        self.assertEqual(self.poll.user_vote(self.user), self.choice1)


class CustomVotingSystemTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.poll = Poll.objects.create(
            title='Test Poll',
            description='Test Description',
            created_by=self.user1
        )
        self.choice1 = Choice.objects.create(poll=self.poll, text='Choice 1')
        self.choice2 = Choice.objects.create(poll=self.poll, text='Choice 2')
    
    def test_voting_system_functionality(self):
        # User1 votes for choice1
        vote1 = self.choice1.votes.up(self.user1)
        self.assertIsInstance(vote1, Vote)
        self.assertTrue(self.choice1.votes.exists(self.user1))
        self.assertEqual(self.choice1.votes.count(), 1)
        
        # User2 votes for choice2  
        vote2 = self.choice2.votes.up(self.user2)
        self.assertIsInstance(vote2, Vote)
        self.assertTrue(self.choice2.votes.exists(self.user2))
        self.assertEqual(self.choice2.votes.count(), 1)
        
        # User1 changes vote to choice2
        self.choice1.votes.delete(self.user1)
        self.choice2.votes.up(self.user1)
        
        self.assertFalse(self.choice1.votes.exists(self.user1))
        self.assertTrue(self.choice2.votes.exists(self.user1))
        self.assertEqual(self.choice1.votes.count(), 0)
        self.assertEqual(self.choice2.votes.count(), 2)
    
    def test_vote_uniqueness(self):
        # User can vote once
        vote1 = self.choice1.votes.up(self.user1)
        vote2 = self.choice1.votes.up(self.user1)  # Should not create duplicate
        
        # Should return the same vote object
        self.assertEqual(vote1.pk, vote2.pk)
        self.assertEqual(self.choice1.votes.count(), 1)
    
    def test_vote_model_methods(self):
        # Test django-vote methods
        self.assertEqual(self.choice1.votes.count(), 0)
        self.assertFalse(self.choice1.votes.exists(self.user1))
        
        # Cast a vote
        self.choice1.votes.up(self.user1)
        
        self.assertEqual(self.choice1.votes.count(), 1)
        self.assertTrue(self.choice1.votes.exists(self.user1))


class PollViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.poll = Poll.objects.create(
            title='Test Poll',
            description='Test Description',
            created_by=self.user
        )
        self.choice = Choice.objects.create(poll=self.poll, text='Test Choice')
    
    def test_poll_list_view(self):
        response = self.client.get(reverse('polls:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Poll')
    
    def test_poll_detail_view(self):
        response = self.client.get(reverse('polls:detail', kwargs={'pk': self.poll.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Poll')
    
    def test_vote_requires_login(self):
        response = self.client.post(reverse('polls:vote', kwargs={'pk': self.poll.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_voting_process(self):
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('polls:vote', kwargs={'pk': self.poll.pk}),
            {'choice': self.choice.pk}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after vote
        # Check that the vote was registered using custom voting system
        self.assertTrue(self.choice.votes.exists(self.user))
        
    def test_vote_change(self):
        """Test that users can change their votes"""
        # Create another choice
        choice2 = Choice.objects.create(poll=self.poll, text='Choice 2')
        
        self.client.login(username='testuser', password='testpass123')
        
        # First vote
        self.client.post(
            reverse('polls:vote', kwargs={'pk': self.poll.pk}),
            {'choice': self.choice.pk}
        )
        self.assertTrue(self.choice.votes.exists(self.user))
        
        # Change vote
        self.client.post(
            reverse('polls:vote', kwargs={'pk': self.poll.pk}),
            {'choice': choice2.pk}
        )
        self.assertFalse(self.choice.votes.exists(self.user))
        self.assertTrue(choice2.votes.exists(self.user))