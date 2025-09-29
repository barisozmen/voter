from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from .voting import VotableMixin, VotableManager


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls')
    is_active = models.BooleanField(default=True)
    
    # Tags using django-taggit
    tags = TaggableManager(blank=True)
    
    objects = models.Manager()
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'pk': self.pk})
        
    @property
    def total_votes(self):
        """Return total votes across all choices"""
        return sum(choice.vote_count for choice in self.choices.all())
        
    def get_results(self):
        """Return choices with vote counts and percentages"""
        total = self.total_votes
        results = []
        for choice in self.choices.all():
            count = choice.vote_count
            percentage = (count / total * 100) if total > 0 else 0
            results.append({
                'choice': choice,
                'count': count,
                'percentage': round(percentage, 1)
            })
        return results
    
    def user_vote(self, user):
        """Get the choice that the user voted for, if any"""
        if not user.is_authenticated:
            return None
        
        for choice in self.choices.all():
            if choice.has_user_voted(user):
                return choice
        return None


class Choice(VotableMixin, models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = VotableManager()
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f"{self.poll.title} - {self.text}"