from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Poll, Choice


class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None
    )
    
    def __init__(self, poll, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.user = user
        self.fields['choice'].queryset = poll.choices.all()
        
        # Check if user has already voted
        existing_vote = poll.user_vote(user)
        
        if existing_vote:
            self.fields['choice'].initial = existing_vote
            self.has_voted = True
        else:
            self.has_voted = False
            
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'choice',
            Submit('submit', 'Vote' if not self.has_voted else 'Change Vote', 
                  css_class='btn btn-primary')
        )
    
    def clean(self):
        cleaned_data = super().clean()
        if not self.poll.is_active:
            raise ValidationError("This poll is no longer active.")
        return cleaned_data


class PollForm(forms.ModelForm):
    choices = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Enter each choice on a new line"
    )
    
    class Meta:
        model = Poll
        fields = ['title', 'description', 'tags']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            'tags',
            'choices',
            Submit('submit', 'Create Poll', css_class='btn btn-success')
        )
    
    def save(self, user):
        poll = super().save(commit=False)
        poll.created_by = user
        poll.save()
        
        # Save tags
        self.save_m2m()
        
        # Create choices
        choices_text = self.cleaned_data['choices'].strip()
        for line in choices_text.split('\n'):
            line = line.strip()
            if line:
                Choice.objects.create(poll=poll, text=line)
        
        return poll