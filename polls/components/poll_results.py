from django_components import component


@component.register("poll_results")
class PollResultsComponent(component.Component):
    template_name = "polls/components/poll_results.html"
    
    def get_context_data(self, poll, results=None, **kwargs):
        return {
            "poll": poll,
            "results": results or poll.get_results(),
            "total_votes": poll.total_votes,
        }
