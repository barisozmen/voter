"""
Minimal, elegant voting system for Django 5.x
Inspired by django-vote but ultra-minimal
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]


class VoteModel(models.Model):
    """Minimal mixin - just inherit and use .votes"""
    
    class Meta:
        abstract = True
    
    @property 
    def votes(self):
        return VoteProxy(self)


class VoteProxy:
    """Ultra-minimal vote proxy"""
    
    def __init__(self, obj):
        self.obj = obj
        self.ct = ContentType.objects.get_for_model(obj)
    
    def up(self, user):
        vote, _ = Vote.objects.get_or_create(
            user=user, content_type=self.ct, object_id=self.obj.pk
        )
        return vote
    
    def delete(self, user):
        return Vote.objects.filter(
            user=user, content_type=self.ct, object_id=self.obj.pk
        ).delete()
    
    def exists(self, user):
        return Vote.objects.filter(
            user=user, content_type=self.ct, object_id=self.obj.pk
        ).exists()
    
    def count(self):
        return Vote.objects.filter(
            content_type=self.ct, object_id=self.obj.pk
        ).count()
