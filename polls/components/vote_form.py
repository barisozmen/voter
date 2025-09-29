from django_components import component


@component.register("vote_form")
class VoteFormComponent(component.Component):
    template_name = "polls/components/vote_form.html"
    
    def get_context_data(self, form, poll, user_vote=None, **kwargs):
        return {
            "form": form,
            "poll": poll,
            "user_vote": user_vote,
            "has_voted": user_vote is not None,
        }
