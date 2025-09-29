"""
Elegant voting system for Django 5.x
Inspired by django-vote but compatible with modern Django
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VoteManager(models.Manager):
    """Manager for Vote model with elegant API"""
    
    def for_object(self, obj):
        """Get all votes for a specific object"""
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=content_type, object_id=obj.pk)
    
    def by_user(self, user, obj=None):
        """Get votes by a specific user, optionally for a specific object"""
        queryset = self.filter(user=user)
        if obj:
            content_type = ContentType.objects.get_for_model(obj)
            queryset = queryset.filter(content_type=content_type, object_id=obj.pk)
        return queryset
    
    def exists_for_user(self, user, obj):
        """Check if user has voted for an object"""
        return self.by_user(user, obj).exists()


class Vote(models.Model):
    """Simple, elegant vote model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = VoteManager()
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} voted for {self.content_object}"


class VotableManager(models.Manager):
    """Manager for votable objects"""
    
    def with_vote_counts(self):
        """Annotate queryset with vote counts"""
        from django.db.models import Count
        content_type = ContentType.objects.get_for_model(self.model)
        return self.annotate(
            vote_count=Count(
                'vote',
                filter=models.Q(
                    vote__content_type=content_type
                )
            )
        )


class VotableMixin:
    """Mixin to add voting capabilities to any model"""
    
    @property
    def votes(self):
        """Return vote manager for this object"""
        return VoteProxy(self)
    
    @property
    def vote_count(self):
        """Return total vote count"""
        return Vote.objects.for_object(self).count()
    
    def user_vote(self, user):
        """Get vote by specific user, if any"""
        if not user.is_authenticated:
            return None
        return Vote.objects.by_user(user, self).first()
    
    def has_user_voted(self, user):
        """Check if user has voted"""
        return Vote.objects.exists_for_user(user, self)


class VoteProxy:
    """Elegant proxy for vote operations on an object"""
    
    def __init__(self, obj):
        self.obj = obj
        self.content_type = ContentType.objects.get_for_model(obj)
    
    def count(self):
        """Return vote count"""
        return Vote.objects.for_object(self.obj).count()
    
    def exists(self, user):
        """Check if user has voted"""
        return Vote.objects.exists_for_user(user, self.obj)
    
    def up(self, user):
        """Cast a vote (elegant upvote)"""
        vote, created = Vote.objects.get_or_create(
            user=user,
            content_type=self.content_type,
            object_id=self.obj.pk,
            defaults={'content_object': self.obj}
        )
        return vote
    
    def delete(self, user):
        """Remove a vote"""
        return Vote.objects.by_user(user, self.obj).delete()
    
    def all(self):
        """Return all votes for this object"""
        return Vote.objects.for_object(self.obj)
    
    def users(self):
        """Return all users who voted"""
        return User.objects.filter(
            votes__content_type=self.content_type,
            votes__object_id=self.obj.pk
        )
