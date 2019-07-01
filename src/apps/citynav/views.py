from django.views.generic import TemplateView
from .models import Route
from .forms import RouteRequestForm


class HomeView(TemplateView):
    template_name = 'home.html'
    form = None
    route = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['route'] = self.route
        return context

    def get(self, request, *args, **kwargs):
        self.form = RouteRequestForm(request.GET or None)
        if self.form.is_valid():
            start_point = self.form.get_start_point()
            end_point = self.form.get_end_point()
            self.route = Route.objects.filter(
                start_x=start_point[0], start_y=start_point[1],
                end_x=end_point[0], end_y=end_point[1],
            ).first()
        return super().get(request, *args, **kwargs)
