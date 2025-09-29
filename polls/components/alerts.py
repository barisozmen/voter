from django_components import component


@component.register("alerts")
class AlertsComponent(component.Component):
    template_name = "polls/components/alerts.html"
    
    def get_context_data(self, messages=None, **kwargs):
        return {
            "messages": messages,
        }
