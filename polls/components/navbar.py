from django_components import component


@component.register("navbar")
class NavbarComponent(component.Component):
    template_name = "polls/components/navbar.html"
    
    def get_context_data(self, user=None, request=None):
        return {
            "user": user or (request.user if request else None),
            "request": request,
        }
