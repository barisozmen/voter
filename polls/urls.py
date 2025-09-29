from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.PollListView.as_view(), name='list'),
    path('create/', views.PollCreateView.as_view(), name='create'),
    path('poll/<int:pk>/', views.PollDetailView.as_view(), name='detail'),
    path('vote/<int:pk>/', views.VoteView.as_view(), name='vote'),
    path('results/<int:pk>/', views.poll_results_ajax, name='results_ajax'),
]
