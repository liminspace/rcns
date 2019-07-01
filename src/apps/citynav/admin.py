from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy, gettext as _
from django.views.generic import TemplateView
from .forms import ImportRoutesForm
from .models import Landmark, Route


@admin.register(Landmark)
class LandmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'x', 'y', 'name')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_x', 'start_y', 'end_x', 'end_y')
    readonly_fields = ('start_x', 'start_y', 'end_x', 'end_y')
    fieldsets = (
        (None, {
            'fields': (('start_x', 'start_y'), ('end_x', 'end_y'), 'instructions'),
        }),
    )

    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns.insert(0, path(
            'import/',
            self.admin_site.admin_view(ImportRoutesView.as_view(admin=self)),
            name='citynav_import_routes',
        ))
        return urlpatterns


class ImportRoutesView(TemplateView):
    template_name = 'admin/citynav/import_routes.html'
    admin = None
    form = None

    def dispatch(self, request, *args, **kwargs):
        self.form = ImportRoutesForm(request.POST or None, request.FILES or None)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': capfirst(_('import routes')),
            'form_url': reverse('admin:citynav_import_routes'),
            'is_popup': (IS_POPUP_VAR in self.request.POST or
                         IS_POPUP_VAR in self.request.GET),

            'has_view_permission': self.request.user.has_perm('view', Route),
            **self.admin.admin_site.each_context(self.request),
            'form': self.form,
            'errors': dict(self.form.errors.items()),
            'non_field_errors': self.form.non_field_errors(),
            'has_file_field': True,
        })
        context['opts'] = Route._meta
        context['add'] = False
        context['is_popup'] = False
        context['user'] = self.request.user
        context['request'] = self.request
        return context

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            try:
                r = Route.import_from_json(self.form.get_routes_data())
            except ValueError as e:
                msg = _('Could not import the file: {}').format(e)
                messages.error(request, msg)
            else:
                msg = _('File imported successfully. '
                        'Added/updated {added_routes}/{updated_routes} route(s) '
                        'and {added_landmarks}/{updated_landmarks} landmark(s).').format(**r)
                messages.success(request, msg)
            return redirect(reverse(f'admin:{Route._meta.app_label}_{Route._meta.model_name}_changelist'))
        return self.get(request, *args, **kwargs)
