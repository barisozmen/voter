from django.contrib import admin
from .models import Poll, Choice
from .voting import Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    readonly_fields = ('vote_count_display',)
    
    def vote_count_display(self, obj):
        return obj.vote_count if obj.pk else 0
    vote_count_display.short_description = 'Votes'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'total_votes', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'tags']
    search_fields = ['title', 'description']
    inlines = [ChoiceInline]
    date_hierarchy = 'created_at'
    readonly_fields = ('total_votes', 'created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by during creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'vote_count_display', 'created_at']
    list_filter = ['poll', 'created_at']
    search_fields = ['text', 'poll__title']
    readonly_fields = ('vote_count_display', 'created_at')
    
    def vote_count_display(self, obj):
        return obj.vote_count
    vote_count_display.short_description = 'Votes'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_object', 'content_type', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ('content_object', 'created_at')
    
    def has_add_permission(self, request):
        # Prevent manual vote creation through admin
        return False