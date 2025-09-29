from django_components import component


@component.register("poll_card")
class PollCardComponent(component.Component):
    template_name = "polls/components/poll_card.html"
    
    def get_context_data(self, poll, show_actions=True, **kwargs):
        return {
            "poll": poll,
            "show_actions": show_actions,
            "total_votes": poll.total_votes,
        }
