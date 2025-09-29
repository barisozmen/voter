from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from django_filters.views import FilterView
from braces.views import LoginRequiredMixin, MessageMixin
from .models import Poll, Choice
from .forms import VoteForm, PollForm
from .filters import PollFilter


class PollListView(FilterView):
    model = Poll
    template_name = 'polls/poll_list.html'
    context_object_name = 'polls'
    paginate_by = 10
    filterset_class = PollFilter
    
    def get_queryset(self):
        return Poll.objects.filter(is_active=True).select_related('created_by').prefetch_related('tags')


class PollDetailView(DetailView):
    model = Poll
    template_name = 'polls/poll_detail.html'
    context_object_name = 'poll'
    
    def get_queryset(self):
        return Poll.objects.filter(is_active=True).prefetch_related('choices')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.object
        
        if self.request.user.is_authenticated:
            context['vote_form'] = VoteForm(poll=poll, user=self.request.user)
            context['user_vote'] = poll.user_vote(self.request.user)
        
        context['results'] = poll.get_results()
        return context


class PollCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Poll
    form_class = PollForm
    template_name = 'polls/poll_create.html'
    success_url = reverse_lazy('polls:list')
    
    def form_valid(self, form):
        self.object = form.save(user=self.request.user)
        self.messages.success("Poll created successfully!")
        return redirect(self.object.get_absolute_url())


class VoteView(LoginRequiredMixin, MessageMixin, View):
    def post(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk, is_active=True)
        form = VoteForm(poll=poll, user=request.user, data=request.POST)
        
        if form.is_valid():
            choice = form.cleaned_data['choice']
            
            # Clear any existing votes for this poll by this user
            for poll_choice in poll.choices.all():
                if poll_choice.votes.exists(request.user):
                    poll_choice.votes.delete(request.user)
            
            # Cast new vote
            choice.votes.up(request.user)
            
            self.messages.success(f"Vote cast for '{choice.text}'!")
            
            # AJAX response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                results_html = render_to_string(
                    'polls/components/poll_results.html',
                    {'poll': poll, 'results': poll.get_results()},
                    request=request
                )
                return JsonResponse({
                    'success': True,
                    'message': f"Vote cast for '{choice.text}'!",
                    'results_html': results_html
                })
        else:
            self.messages.error("There was an error with your vote.")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        
        return redirect('polls:detail', pk=pk)


def poll_results_ajax(request, pk):
    """AJAX endpoint for live poll results"""
    poll = get_object_or_404(Poll, pk=pk)
    results_html = render_to_string(
        'polls/components/poll_results.html',
        {'poll': poll, 'results': poll.get_results()},
        request=request
    )
    return JsonResponse({
        'results_html': results_html,
        'total_votes': poll.total_votes
    })